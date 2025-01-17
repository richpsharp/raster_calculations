"""Align given rasters to given bounding box and projection."""
import logging
import multiprocessing
import os
import re
import shutil
import sys

from osgeo import gdal
from osgeo import osr
from ecoshard.geoprocessing import _create_latitude_m2_area_column
import ecoshard
import numpy
from ecoshard import geoprocessing
from ecoshard import taskgraph

gdal.SetCacheMax(2**27)

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(levelname)s %(name)s'
        ' [%(funcName)s:%(lineno)d] %(message)s'),
    stream=sys.stdout)
LOGGER = logging.getLogger(__name__)
logging.getLogger('taskgraph').setLevel(logging.WARN)

MASK_ECOSHARD_URL = ( #NOTE THIS IS JUST FOR DATA/NODATA MASKS, 1/0 DOESN'T MATTER
    'https://storage.googleapis.com/ecoshard-root/ci_global_restoration/results/global_people_access_population_2019_60.0m_md5_d264d371bd0d0a750b002a673abbb383.tif')

ECOSHARD_URL_PREFIX = 'https://storage.googleapis.com/ecoshard-root/ci_global_restoration/results/'


# Format of these are (ecoshard filename, mask(t/f), perarea(t/f), in wgs84 projection)
RASTER_LIST = [
    ('ESACCI-LC-L4-LCCS-Map-300m-P1Y-2020-v2.1.1_md5_2ed6285e6f8ec1e7e0b75309cc6d6f9f_hab_mask.tif', False, False),
    #('restoration_pnv0.0001_on_ESA2020_v2_md5_47613f8e4d340c92b2c481cc8080cc9d_hab_mask.tif', False, False),
    #('results/global_normalized_people_access_population_2019_60.0m_md5_6a3bf3ec196b3b295930e75d8808fa9c.tif', True, True, False),
    #('results/global_people_access_population_2019_60.0m_md5_d264d371bd0d0a750b002a673abbb383.tif', True, True, False),
    ]


WARPED_SUFFIX = '_WARPED'
MASKED_SUFFIX = '_MASKED'
PERAREA_SUFFIX = '_PERAREA'
RESCALED_VALUE_SUFFIX = '_AREA_SCALED_VALUE'
RESAMPLE_MODE = 'near'

WORKSPACE_DIR = 'align_to_mask_workspace'
PERAREA_DIR = os.path.join(WORKSPACE_DIR, 'per_area_rasters')
ECOSHARD_DIR = os.path.join(WORKSPACE_DIR, 'ecoshards')
MASK_DIR = os.path.join(WORKSPACE_DIR, 'mask')
WARPED_DIR = os.path.join(WORKSPACE_DIR, 'warped')

for dir_path in [
        WORKSPACE_DIR, PERAREA_DIR, ECOSHARD_DIR, MASK_DIR, WARPED_DIR]:
    os.makedirs(dir_path, exist_ok=True)


def warp_raster(base_raster_path, mask_raster_path, resample_mode, target_raster_path):
    """Warp raster to exemplar's bounding box, cell size, and projection."""
    base_projection_wkt = geoprocessing.get_raster_info(
        base_raster_path)['projection_wkt']
    if base_projection_wkt is None:
        # assume its wgs84 if not defined
        LOGGER.warn(
            f'{base_raster_path} has undefined projection, assuming WGS84')
        base_projection_wkt = osr.SRS_WKT_WGS84_LAT_LONG
    mask_raster_info = geoprocessing.get_raster_info(mask_raster_path)
    geoprocessing.warp_raster(
        base_raster_path, mask_raster_info['pixel_size'],
        target_raster_path, resample_mode,
        base_projection_wkt=base_projection_wkt,
        target_bb=mask_raster_info['bounding_box'],
        target_projection_wkt=mask_raster_info['projection_wkt'])


def copy_and_rehash_final_file(base_raster_path, target_dir):
    """Copy base to target and replace hash with current hash."""
    target_md5_free_path = os.path.join(
        target_dir,
        re.sub('(.*)md5_[0-9a-f]+_(.*)', r"\1\2", os.path.basename(
            base_raster_path)))
    shutil.copyfile(base_raster_path, target_md5_free_path)
    try:
        ecoshard.hash_file(target_md5_free_path, rename=True)
    except OSError:
        LOGGER.exception(
            'hash file failed, possibly because file exists but that is okay '
            'since it is the same hash')


def mask_raster(base_raster_path, mask_raster_path, target_raster_path):
    """Mask base by mask setting nodata to nodata otherwise passthrough."""
    mask_nodata = geoprocessing.get_raster_info(
        mask_raster_path)['nodata'][0]
    base_raster_info = geoprocessing.get_raster_info(base_raster_path)
    base_nodata = base_raster_info['nodata'][0]

    def _mask_op(base_array, mask_array):
        result = numpy.copy(base_array)
        nodata_mask = numpy.isclose(mask_array, mask_nodata)
        result[nodata_mask] = base_nodata
        return result

    geoprocessing.raster_calculator(
        [(base_raster_path, 1), (mask_raster_path, 1)], _mask_op,
        target_raster_path, base_raster_info['datatype'], base_nodata)


def _convert_to_density(
        base_raster_path, wgs84_flag, target_density_raster_path):
    base_raster_info = geoprocessing.get_raster_info(
        base_raster_path)
    if wgs84_flag:
        ## xmin, ymin, xmax, ymax
        _, lat_min, _, lat_max = base_raster_info['bounding_box']
        _, n_rows = base_raster_info['raster_size']
        m2_area_col = _create_latitude_m2_area_column(lat_min, lat_max, n_rows)
    else:
        pixel_area = base_raster_info['pixel_size'][0]**2

    nodata = base_raster_info['nodata'][0]

    def _div_by_area_op(base_array, m2_area_array):
        result = numpy.empty(base_array.shape, dtype=base_array.dtype)
        if nodata is not None:
            valid_mask = ~numpy.isclose(base_array, nodata)
            result[:] = nodata
        else:
            valid_mask = numpy.ones(base_array.shape, dtype=bool)

        if wgs84_flag:
            result[valid_mask] = (
                base_array[valid_mask] / m2_area_array[valid_mask])
        else:
            result[valid_mask] = (
                base_array[valid_mask] / m2_area_array)
        return result

    if wgs84_flag:
        geoprocessing.raster_calculator(
            [(base_raster_path, 1), m2_area_col], _div_by_area_op,
            target_density_raster_path, base_raster_info['datatype'],
            nodata)
    else:
        geoprocessing.raster_calculator(
            [(base_raster_path, 1), (pixel_area, 'raw')], _div_by_area_op,
            target_density_raster_path, base_raster_info['datatype'],
            nodata)


def _wgs84_density_to_value(base_raster_path, target_value_raster_path):
    base_raster_info = geoprocessing.get_raster_info(
        base_raster_path)

    # xmin, ymin, xmax, ymax
    _, lat_min, _, lat_max = base_raster_info['bounding_box']
    _, n_rows = base_raster_info['raster_size']
    m2_area_col = _create_latitude_m2_area_column(lat_min, lat_max, n_rows)
    nodata = base_raster_info['nodata'][0]

    def _mult_by_area_op(base_array, m2_area_array):
        result = numpy.empty(base_array.shape, dtype=base_array.dtype)
        if nodata is not None:
            valid_mask = ~numpy.isclose(base_array, nodata)
            result[:] = nodata
        else:
            valid_mask = numpy.ones(base_array.shape, dtype=bool)

        result[valid_mask] = (
            base_array[valid_mask] * m2_area_array[valid_mask])
        return result

    geoprocessing.raster_calculator(
        [(base_raster_path, 1), m2_area_col], _mult_by_area_op,
        target_value_raster_path, base_raster_info['datatype'],
        nodata)


def main():
    """Entry point."""
    task_graph = taskgraph.TaskGraph(
        WORKSPACE_DIR, multiprocessing.cpu_count(), 5.0)
    mask_ecoshard_path = os.path.join(
        ECOSHARD_DIR, os.path.basename(MASK_ECOSHARD_URL))
    download_mask_task = task_graph.add_task(
        func=ecoshard.download_url,
        args=(MASK_ECOSHARD_URL, mask_ecoshard_path, True), #True is for skip_target_if_exists parameter
        target_path_list=[mask_ecoshard_path],
        task_name=f'download {mask_ecoshard_path}')

    #for ecoshard_base, mask_flag, per_area_flag in RASTER_LIST:
    for ecoshard_base, mask_flag, per_area_flag, wgs84_flag in RASTER_LIST:
        ecoshard_url = f'{ECOSHARD_URL_PREFIX}/{ecoshard_base}'
        target_path = os.path.join(ECOSHARD_DIR, ecoshard_base)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        LOGGER.debug(f'download {ecoshard_url} to {target_path}')
        last_task = task_graph.add_task(
            func=ecoshard.download_url,
            args=(ecoshard_url, target_path, True),
            target_path_list=[target_path],
            dependent_task_list=[download_mask_task],
            task_name=f'download {ecoshard_url} to {target_path}')
        if per_area_flag:
            wgs84_density_raster_path = os.path.join(
                PERAREA_DIR, f'%s{PERAREA_SUFFIX}%s' % os.path.splitext(
                    os.path.basename(target_path)))
            last_task = task_graph.add_task(
                func=_convert_to_density,
                args=(target_path, wgs84_flag, wgs84_density_raster_path),
                target_path_list=[wgs84_density_raster_path],
                task_name=f'convert to density: {wgs84_density_raster_path}',
                dependent_task_list=[last_task],
                )
            target_path = wgs84_density_raster_path
        warped_raster_path = os.path.join(
            WARPED_DIR,
            f'%s{WARPED_SUFFIX}_{RESAMPLE_MODE}%s' % os.path.splitext(
                os.path.basename(target_path)))

        last_task = task_graph.add_task(
            func=warp_raster,
            args=(
                target_path, mask_ecoshard_path, RESAMPLE_MODE,
                warped_raster_path),
            target_path_list=[warped_raster_path],
            task_name=f'warp raster {warped_raster_path}',
            dependent_task_list=[last_task])
        target_path = warped_raster_path
        if mask_flag:
            mask_raster_path = os.path.join(
                MASK_DIR,
                f'%s{MASKED_SUFFIX}%s' % os.path.splitext(os.path.basename(
                    warped_raster_path)))
            last_task = task_graph.add_task(
                func=mask_raster,
                args=(target_path, mask_ecoshard_path, mask_raster_path),
                target_path_list=[mask_raster_path],
                task_name=f'mask raster to {mask_raster_path}',
                dependent_task_list=[last_task])
            target_path = mask_raster_path

        task_graph.add_task(
            func=copy_and_rehash_final_file,
            args=(target_path, WORKSPACE_DIR),
            task_name=f'copy and reshash final target_path',
            dependent_task_list=[last_task])

        if per_area_flag:
            # convert the density to a count
            wgs84_value_raster_path = os.path.join(
                PERAREA_DIR, f'%s{RESCALED_VALUE_SUFFIX}%s' % os.path.splitext(
                    os.path.basename(target_path)))
            last_task = task_graph.add_task(
                func=_wgs84_density_to_value,
                args=(target_path, wgs84_value_raster_path),
                target_path_list=[wgs84_value_raster_path],
                task_name=f'convert from density to value: {wgs84_value_raster_path}',
                dependent_task_list=[last_task],
                )
            task_graph.add_task(
                func=copy_and_rehash_final_file,
                args=(wgs84_value_raster_path, WORKSPACE_DIR),
                task_name=f'copy and reshash final target_path',
                dependent_task_list=[last_task])

    task_graph.close()
    task_graph.join()


if __name__ == '__main__':
    main()
