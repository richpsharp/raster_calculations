"""These calculations are for the Critical Natural Capital paper."""
import glob
import sys
import os
import logging
import multiprocessing
import datetime
import subprocess
import raster_calculations_core
from osgeo import gdal
from osgeo import osr
import taskgraph
import pygeoprocessing

gdal.SetCacheMax(2**30)

WORKSPACE_DIR = 'CNC_workspace'
NCPUS = multiprocessing.cpu_count()
try:
    os.makedirs(WORKSPACE_DIR)
except OSError:
    pass

logging.basicConfig(
    level=logging.DEBUG,
    format=(
        '%(asctime)s (%(relativeCreated)d) %(levelname)s %(name)s'
        ' [%(funcName)s:%(lineno)d] %(message)s'),
    stream=sys.stdout)
LOGGER = logging.getLogger(__name__)


def main():
    """Write your expression here."""

    # CNC calculations

    single_expression = {
        'expression': '(raster1>2)*raster2',
        'symbol_to_path_map': {
            'raster1': r"C:\Users\Becky\Documents\cnc_project\optimization\prioritiz-2km-country\cntr_2km_nocarb.tif",
            'raster2': r"C:\Users\Becky\Documents\cnc_project\Total_C_v10_2km_optimization_output_2020_08_18\optimal_mask_0.65.tif"
        },
        'target_nodata': -9999,
        'target_pixel_size': (0.021319, 0.021319),
        'resample_method': 'average',
        'target_raster_path': "ctr90_C65_2km.tif",
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return
    
    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)    

    single_expression = {
        'expression': '(raster2>-9999)*raster1',
        'symbol_to_path_map': {
            #'raster1': r"C:\Users\Becky\Documents\cnc_project\optimization\output_2km_masks\solution_111_tar_90_res_2km_carbon_0.tif",
            'raster1': r"C:\Users\Becky\Documents\cnc_project\optimization\output_2km_masks\solution_222_tar_90_res_2km.tif",
            'raster2': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_e_source_abs_ann_mean.tif"
        },
        'target_nodata': -9999,
        'default_nan': -9999,
        'target_sr_wkt': wgs84_srs.ExportToWkt(),
        'target_pixel_size': (1.495833333333333348,1.5092592592592593),
        'resample_method': 'mode',
        #'target_raster_path': "solution_111_tar_90_res_2km_carbon_0_resampled15_mode.tif",
        'target_raster_path': "solution_222_tar_90_res_2km_resampled15_mode.tif",
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    single_expression = {
        'expression': '(raster1>2)*raster2',
        'symbol_to_path_map': {
            'raster1': r"C:\Users\Becky\Documents\cnc_project\optimization\prioritiz-2km-country\cntr_2km_nocarb.tif",
            'raster2': r"C:\Users\Becky\Documents\cnc_project\Total_C_v10_2km_optimization_output_2020_08_18\optimal_mask_0.65.tif"
        },
        'target_nodata': -9999,
        'target_pixel_size': (0.021319, 0.021319),
        'resample_method': 'average',
        'target_raster_path': "ctr90_C65_2km.tif",
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    single_expression = {
        'expression': '(raster1>=0)*raster2',
        'symbol_to_path_map': {
            'raster1': r"C:\Users\Becky\Documents\cnc_project\optimization\prioritiz-2km-country\cntr_2km_nocarb.tif",
            'raster2': r"C:\Users\Becky\Documents\raster_calculations\Total_C_v10_300m.tif"
        },
        'target_nodata': -9999,
        'target_pixel_size': (0.021319, 0.021319),
        'resample_method': 'average',
        'target_raster_path': "Total_C_v10_2km.tif",
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    

    NNth_poll = 38
    Max_lang = 43 #original map did not exceed 43 languages per degree grid cell; higher than that must be an error
    LO = 0.001 # not contributing much below this point!
    LOth_ffish = 0.001 # Min values are regression artifacts. Should be cut off at 10-1 tons per grid cell (~100 sq km). That’s 1 kg per sq km
    NNth_ffish = 30 # Max cut-off should be 3000 tons per grid cell. That’s 30 tons per sq km. (In between the 99 and 99.9th percentiles once small values are excluded)
    #Max_mfish = 400 #this one's different because even though it's higher than the 99th percentile, there are some realistic values of up to 346 kg /km2
    #NOTE: Rachel subsequently asked Reg Watson about this and he said it should NOT be clamped - if anything his upper values (of a few thousand) are underestimates
    LOth_MM = 0.001

    clamped_service_list = [ #some services just have crazy high values that throw the whole percentiles off so we're clamping them to the 99th percentile
        {
            'expression': f'(service>{NNth_poll})*({NNth_poll})+(service<={NNth_poll})*(service>={LO})*service + 0*(service<{LO})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_pollination_nathab30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_pollination_nathab30s_clamped.tif",
        },
        {
            'expression': f'(service>{Max_lang})*(128) + (service<={Max_lang})*service', 
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_cultural_language_nathab30s.tif",
            },
            'target_nodata': 128,
            'target_raster_path': "realized_cultural_language_nathab30s_clamped.tif",
        },
        {
            'expression': f'(service>{NNth_ffish})*{NNth_ffish} + (service<={NNth_ffish})*(service>={LOth_ffish})*service + 0*(service<{LOth_ffish})', 
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_fwfish_nathab30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fwfish_per_km2_30s_clamped.tif",
        },
    #    {
    #        'expression': f'(service>{Max_mfish})*({Max_mfish})+(service<={Max_mfish})*(service>={LO})*service+ 0*(service<{LO})', 
    #        'symbol_to_path_map': {
    #            'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_marinefish_watson_2010_2014_30s.tif",
    #        },
    #        'target_nodata': -9999,
    #        'target_raster_path': "realized_marinefish_watson_2010_2014_30s_clamped.tif",
    #    },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_commercialtimber_forest30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_commercialtimber_forest30s_clamped.tif",
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_domestictimber_forest30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_domestictimber_forest30s_clamped.tif",
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_flood_nathab30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_flood_nathab30s_clamped.tif",
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_fuelwood_forestshrub30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fuelwood_forest30s_clamped.tif",
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_grazing_natnotforest30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_grazing_natnotforest30s_clamped.tif",
        },
        {
            'expression': f'(service>{LO})*service + 0*(service<={LO})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_natureaccess10_nathab30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess10_nathab30s_clamped.tif",
        },
        {
            'expression': f'(service>{LO})*service + 0*(service<={LO})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\resampled_30s\realized_natureaccess100_nathab30s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess100_nathab30s_clamped.tif",
        },
    ]

    for calculation in clamped_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    masked_service_list = [
        {
            'expression': 'service*mask + 128*(1-mask)', #this sets all values not in the mask to nodata (in this case, 128)
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\half_degree_grid_langa_19_dslv_density.tif",
            },
            'target_nodata': 128,
            'target_raster_path': "realized_cultural_language_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_sedimentdeposition_nathab_clamped_md5_30d4d6ac5ff4bca4b91a3a462ce05bfe.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_sedimentdeposition_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_pollination_md5_443522f6688011fd561297e9a556629b.tif"
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_pollination_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_nitrogenretention_downstream3s_10s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_nitrogenretention_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': '((service<0)*(-9999)+(service>=0)*service)*mask + -9999*(1-mask)', #this both sets all negative values to nodata AND sets anything outside the mask to nodata
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_e_source_ratio_ann_mean.tif",
            },
            'target_nodata': -9999,
            'default_nan': -9999, # this is necessary because there are apparently nans in this list!
            'target_raster_path': "realized_moisturerecycling_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\RealInflGStoragePop.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_flood_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
    ]

    for calculation in masked_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    masked_service_list = [
        {
            'expression': 'service*mask + 128*(1-mask)', #this sets all values not in the mask to nodata (in this case, 128)
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\half_degree_grid_langa_19_dslv_density.tif",
            },
            'target_nodata': 128,
            'target_raster_path': "realized_cultural_language_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': '((service<0)*(-9999)+(service>=0)*service)*mask + -9999*(1-mask)', #this both sets all negative values to nodata AND sets anything outside the mask to nodata
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_e_source_ratio_ann_mean.tif",
            },
            'target_nodata': -9999,
            'default_nan': -9999, # this is necessary because there are apparently nans in this list!
            'target_raster_path': "realized_moisturerecycling_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\RealInflGStoragePop.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_flood_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forest_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realised_commercial_timber_value.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_commercialtimber_forest30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forest_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realised_domestic_timber_value.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_domestictimber_forest30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forestshrub_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_fuelwood.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fuelwood_forestshrub30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_notforest_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_grazing_md5_19085729ae358e0e8566676c5c7aae72.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_grazing_natnotforest30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\total_pop_near_nature_10.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess10_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\total_pop_near_nature_100.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess100_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_pollination_md5_443522f6688011fd561297e9a556629b.tif"
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_pollination_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_nitrogenretention_downstream3s_10s.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_nitrogenretention_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_sedimentdeposition_nathab_clamped_md5_30d4d6ac5ff4bca4b91a3a462ce05bfe.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_sedimentdeposition_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015_30s.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\per_km_2_realized_fwfish_distrib_catch_md5_995d3d330ed5fc4462a47f7db44225e9.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fwfish_nathab30s.tif",
            'target_pixel_size': (0.008333333333333333218, -0.008333333333333333218),
            'resample_method': 'average',
        },
    ]

    for calculation in masked_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    single_expression = {
        'expression': 'service*pop',
        'symbol_to_path_map': {
            'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\need_processing\potential_nitrogenretention3s_10s_clamped.tif",
            'pop': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\need_processing\beneficiaries_downstream_nathab_md5_db1311d54c0174c932cc676bbd621643.tif",
        },
        'target_nodata': -9999,
        'default_nan': -9999,
        'target_raster_path': "realized_nitrogenretention_downstream3s_10s.tif",
        'target_pixel_size': (0.002777777777778, -0.002777777777778),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()

    single_expression = {
        'expression': '(service>=0)*(service<186)*service + (service>=186)*186 + (service<0)*0',
        'symbol_to_path_map': {
            'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\need_processing\potential_nitrogenretention3s_10s.tif",
        },
        'target_nodata': -9999,
        'default_nan': -9999,
        'target_raster_path': "potential_nitrogenretention3s_10s_clamped.tif",
        'target_pixel_size': (0.002777777777778, -0.002777777777778),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    single_expression = {
        'expression': 'load - export',
        'symbol_to_path_map': {
            'load': r"C:\Users\Becky\Documents\modified_load_n_baseline_napp_rate_global_md5_00d3e7f1abc5d6aee99d820cd22ef7da.tif",
            'export': r"C:\Users\Becky\Documents\n_export_baseline_napp_rate_global_md5_b210146a5156422041eb7128c147512f.tif",
        },
        'target_nodata': -9999,
        'default_nan': -9999,
        'target_raster_path': "potential_nitrogenretention3s_10s.tif",
        'target_pixel_size': (0.002777777777778, -0.002777777777778),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    # resampling of just one raster doesn't work in raster calculations, so just use pygeoprocessing directly
    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
        (30/3600, -30/3600), 'masked_all_nathab_esa2015_30s.tif',
        'mode'
    )

    TASK_GRAPH.join()

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_wstreams_esa2015.tif",
        (30/3600, -30/3600), 'masked_all_nathab_wstreams_esa2015_30s.tif',
        'mode'
    )

    TASK_GRAPH.join()

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forest_esa2015.tif",
        (30/3600, -30/3600), 'masked_nathab_forest_esa2015_30s.tif',
        'mode'
    )

    TASK_GRAPH.join()

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forestshrub_esa2015.tif",
        (30/3600, -30/3600), 'masked_nathab_forestshrub_esa2015_30s.tif',
        'mode'
    )

    TASK_GRAPH.join()

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_notforest_esa2015.tif",
        (30/3600, -30/3600), 'masked_nathab_notforest_esa2015_30s.tif',
        'mode'
    )

    TASK_GRAPH.join()

    #now doing all the layers that don't need to get masked by habitat (because they're already on the habitat or they can't be)
    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_coastalprotection_md5_b8e0ec0c13892c2bf702c4d2d3e50536.tif",
        (30/3600, -30/3600), 'realized_coastalprotection_30s.tif',
        'average'
    )

    TASK_GRAPH.join()

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\cnc_project\original_rasters\watson_2010_2014_catch_per_sqkm_AVG.tif",
        (30/3600, -30/3600), 'realized_marinefish_watson_2010_2014_30s.tif',
        'average'
    )

    TASK_GRAPH.join()

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_coastalprotection_barrierreef_md5_126320d42827adc0f7504d4693c67e18.tif",
        (30/3600, -30/3600), 'realized_coastalprotection_barrierreef_30s.tif',
        'average'
    )

    TASK_GRAPH.join()

    #this one's also in a different CRS so needs to be reprojected
    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)

    pygeoprocessing.warp_raster(
        r"C:\Users\Becky\Documents\cnc_project\original_rasters\Modelled_Total_Dollar_Value_of_Reef_Tourism_USD_per_km2.tif",
        (30/3600, -30/3600), 'realized_reeftourism_30s.tif',
        'average', target_sr_wkt=wgs84_srs.ExportToWkt()
    )

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return



    masker_list = [
        {
            # this is for masking out forest from natural habitat, for livestock production
            # this counts the >50% herbaceous / < 50% tree cover category as "not forest"; also includes lichens, mosses  and shrubland which maybe isn't totally edible by cattle either
            'expression': 'mask(raster, %s, invert=False)'%(str([x for x in range(100,154)]+[30]+[40]+[180])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_nathab_notforest_esa2015.tif",
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([x for x in range(30,111)]+[150]+[151]+[160]+[170])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_nathab_forest_esa2015.tif",
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([x for x in range(30,123)]+[150]+[151]+[152]+[160]+[170]+[180])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_nathab_forestshrub_esa2015.tif",
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(30,181)]+[210])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_all_nathab_wstreams_esa2015.tif",
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(30,181)])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_all_nathab_esa2015.tif",
        },
    ]
    for masker in masker_list:
       raster_calculations_core.evaluate_calculation(
            masker, TASK_GRAPH, WORKSPACE_DIR)


    TASK_GRAPH.join()
    TASK_GRAPH.close()

#    single_expression = {
#        'expression': '(raster3 > 0) + (raster4 > 0) + (raster5 > 0) + (raster6 > 0) + (raster7 > 0) + (raster11 > 0) + (raster12 > 0) + (raster13 > 0) + (raster15 > 0)',
#        'symbol_to_path_map': {
#            #'raster1': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_coastalprotection_barrierreef_md5_126320d42827adc0f7504d4693c67e18.tif",
#            #'raster2': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_coastalprotection_md5_b8e0ec0c13892c2bf702c4d2d3e50536.tif",
#            'raster3': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_commercialtimber_forest_clamped0_md5_24844213f0f65a6c0bedfebe2fbd089e.tif",
#            'raster4': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_cultural_language_nathab_md5_8e517eaa7db482d1446be5b82152c79b.tif",
#            'raster5': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_domestictimber_forest_clamped0_md5_dca99ceb7dd9f96d54b3fcec656d3180.tif",
#            'raster6': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_flood_nathab_clamped0_md5_eb8fd58621e00c6aeb80f4483da1b35c.tif",
#            'raster7': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_fuelwood_forest_clamped0_md5_4ee236f5400ac400c07642356dd358d1.tif",
#            #'raster8': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_fwfish_per_km2_clamped_1e-3_30_md5_0b4455185988a9e2062a39b27910eb8b.tif",
#            #'raster9': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_grazing_natnotforest_clamped0_md5_8eeb02139f0fabf552658f7641ab7576.tif",
#            #'raster10': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_marinefish_watson_2010_2014_clamped_md5_167448a2c010fb2f20f9727b024efab8.tif",
#            'raster11': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_natureaccess10_nathab_md5_af07e76ecea7fb5be0fa307dc7ff4eed.tif",
#            'raster12': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_nitrogenretention_nathab_clamped_md5_fe63ffd7c6633f336c91241bbd47bddd.tif",
#            'raster13': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_pollination_nathab_clamped_md5_c9486d6c8d55cea16d84ff4e129b005a.tif",
#            #'raster14': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_reeftourism_Modelled_Total_Dollar_Value_md5_171a993b8ff40d0447f343dd014c72e0.tif",
#            'raster15': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\realized_sedimentdeposition_nathab_clamped_md5_30d4d6ac5ff4bca4b91a3a462ce05bfe.tif"
#        },
#        'target_nodata': -9999,
#        'default_nan': -9999,
#        'target_raster_path': "zeroes_in_forest.tif"
#    }
#
#    raster_calculations_core.evaluate_calculation(
#        single_expression, TASK_GRAPH, WORKSPACE_DIR)
#
#    TASK_GRAPH.join()
#    TASK_GRAPH.close()
#
#    return


    wgs84_srs = osr.SpatialReference()
    wgs84_srs.ImportFromEPSG(4326)

    single_expression = {
        'expression': 'mask*raster',
        #'expression': '(service>=0)*(service<101)*service + (service>=101)*101 + (service<0)*0',
        'symbol_to_path_map': {
            'mask': r"C:\Users\Becky\Dropbox\NatCap\projects\NASA GEOBON\data\CR_intersecting_wsheds_26917.tif",
            #'raster': r"C:\Users\Becky\Documents\ESACCI_LC_L4_LCCS_borrelli_sed_export_compressed_md5_19cd746cdeb63bd0ced4815071b252bf.tif",
            #'raster': r"C:\Users\Becky\Documents\n_export_baseline_napp_rate_global_md5_b210146a5156422041eb7128c147512f.tif"
            #'raster': r"C:\Users\Becky\Documents\cnc_project\original_rasters\potential_nitrogenretention3s_10s_clamped.tif"
            #'raster': r"C:\Users\Becky\Documents\cnc_project\original_rasters\potential_sedimentdeposition_md5_aa9ee6050c423b6da37f8c2723d9b513.tif"
            #'service':r"C:\Users\Becky\Documents\raster_calculations\ESA_sed_retention_CR.tif",
            'raster': r"C:\Users\Becky\Documents\cnc_project\original_rasters\cv_service_sum_md5_0f86665de086aba2e16dca68ac859428.tif",
        },
        'target_nodata': -9999,
        'default_nan': -9999,
        #'target_raster_path': "ESA_sed_export_CR.tif",
        #'target_raster_path': "ESA_n_export_CR.tif",
        #'target_raster_path': "ESA_n_retention_CR.tif",
        #'target_raster_path': "ESA_sed_retention_CR.tif",
        'target_raster_path': "ESA_WCMC_coastal_protection_CR.tif",
        'target_sr_wkt': wgs84_srs.ExportToWkt(),
        'target_pixel_size': (0.002777777777778, -0.002777777777778),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    Max_mfish = 400 #this one's different because even though it's higher than the 99th percentile, there are some realistic values of up to 346 kg /km2
    clamped_service_list = [ #some services just have crazy high values that throw the whole percentiles off so we're clamping them to the 99th percentile
        {
            'expression': f'(service>{Max_mfish})*({Max_mfish})+(service<={Max_mfish})*service',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\watson_2010_2014_catch_per_sqkm_AVG.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_marinefish_watson_2010_2014_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
    ]

    for calculation in clamped_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    single_expression = {
        'expression': 'service * pop',
        'symbol_to_path_map': {
            'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\need_processing\reefs\barrier_reef_service_average_raster_md5_e12c2928e16bdbad45ce4220d18a5889.tif",
            'pop': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\need_processing\reefs\barrier_reef_pop_average_raster_md5_8387777dc970a55e7b5f5949791cf1ef.tif",
        },
        'target_nodata': -9999,
        'default_nan': -9999,
        'target_raster_path': "realized_coastalprotection_barrierreef.tif",
        'target_pixel_size': (0.002777777777778, -0.002777777777778),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    single_expression = {
        'expression': 'service * pop',
        'symbol_to_path_map': {
            'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\cv_pop_sum_md5_954b755a9300ceb03a284197672b3656.tif",
            'pop': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\cv_service_sum_md5_0f86665de086aba2e16dca68ac859428.tif",
        },
        'target_nodata': -9999,
        'target_raster_path': "realized_coastalprotection.tif",
        'target_pixel_size': (0.002777777777778, -0.002777777777778),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    calculation_list = [
        {
            'expression': 'service*pop',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\potential_nitrogenretention_nathab_clamped_md5_bf6ce40d6d9e8c8c1b2774b375b85b8a.tif",
                'pop':r"C:\Users\Becky\Documents\cnc_project\masked_rasters\beneficiaries_downstream_nathab_md5_db1311d54c0174c932cc676bbd621643.tif"
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_nitrogenretention_nathab_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*pop',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\potential_sedimentdeposition_nathab_clamped_md5_1d826c8885c6479b6307bc345b95d8bf.tif",
                'pop':r"C:\Users\Becky\Documents\cnc_project\masked_rasters\beneficiaries_downstream_nathab_md5_db1311d54c0174c932cc676bbd621643.tif"
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_sedimentdeposition_nathab_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*pop',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\cv_service_sum_bin_raster_md5_bc04cd7112c865fc12f8229ad4757af5.tif",
                'pop':r"C:\Users\Becky\Documents\cnc_project\masked_rasters\cv_pop_sum_bin_raster_md5_27be87e1a0c5a789c82d84122ebf61b8.tif"
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_coastalprotectionbin.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service * pop / 10',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\barrier_reef_service_average_raster_md5_e12c2928e16bdbad45ce4220d18a5889_eez__GLOBAL_bin_nodata0_raster_md5_c271e54f1b04174d3e620df344a52bd9.tif",
                'pop': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\barrier_reef_pop_average_raster_md5_8387777dc970a55e7b5f5949791cf1ef_eez__GLOBAL_bin_nodata0_raster_md5_b36485a7d4f837804982e5e9272d34fe.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_coastalprotectionbin_barrierreef.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
            'resample_method': 'average'
        }

    ]

    for calculation in calculation_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    masker_list = [
         {
            # the %s is a placeholder for the string we're passing it using this function that lists every number in the range and takes away the [] of the list and turns it into a string
            'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(50,181)])[1:-1]),
            #'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(10,200)]+[220])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_all_nathab_esa2015.tif",
        },
        {
            # this is for masking out forest from natural habitat, for livestock production
            # this counts the >50% herbaceous / < 50% tree cover category as "not forest"; also includes lichens, mosses  and shrubland which maybe isn't totally edible by cattle either
            'expression': 'mask(raster, %s, invert=False)'%(str([x for x in range(110,154)]+[180])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_nathab_notforest_esa2015.tif",
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([x for x in range(50,111)]+[150]+[151]+[160]+[170])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_nathab_forest_esa2015.tif",
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(50,181)]+[210])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "masked_all_nathab_wstreams_esa2015.tif",
        },
        {
           'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(10,31)])[1:-1]),
            'symbol_to_path_map': {
                'raster': r"C:\Users\Becky\Documents\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "agmask_esa2015.tif",
        },
    ]
    for masker in masker_list:
       raster_calculations_core.evaluate_calculation(
            masker, TASK_GRAPH, WORKSPACE_DIR)


    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    masked_service_list = [
        {
            'expression': 'service*mask + 128*(1-mask)', #this sets all values not in the mask to nodata (in this case, 128)
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\half_degree_grid_langa_19_dslv_density.tif",
            },
            'target_nodata': 128,
            'target_raster_path': "realized_cultural_language_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': '((service<0)*(-9999)+(service>=0)*service)*mask + -9999*(1-mask)', #this both sets all negative values to nodata AND sets anything outside the mask to nodata
            'symbol_to_path_map': {
                'mask': r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_e_source_ratio_ann_mean.tif",
            },
            'target_nodata': -9999,
            'default_nan': -9999, # this is necessary because there are apparently nans in this list!
            'target_raster_path': "realized_moisturerecycling_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\RealInflGStoragePop.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_flood_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forest_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\realised_commercial_timber_value.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_commercialtimber_forest.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forest_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\realised_domestic_timber_value.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_domestictimber_forest.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_forest_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\realized_fuelwood.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fuelwood_forest.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_nathab_notforest_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\realized_grazing_md5_19085729ae358e0e8566676c5c7aae72.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_grazing_natnotforest.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\total_pop_near_nature_10.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess10_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\total_pop_near_nature_100.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess100_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\potential_nitrogenretention_md5_286c51393042973f71884ddc701be03d.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "potential_nitrogenretention_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\potential_sedimentdeposition_md5_aa9ee6050c423b6da37f8c2723d9b513.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "potential_sedimentdeposition_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\downstream_beneficiaries_md5_68495f4bbdd889d7aaf9683ce958a4fe.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "beneficiaries_downstream_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\original_rasters\realized_pollination_md5_443522f6688011fd561297e9a556629b.tif"
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_pollination_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\realized_nitrogenretention_downstream_md5_82d4e57042482eb1b92d03c0d387f501.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_nitrogenretention_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'service*mask + -9999*(1-mask)',
            'symbol_to_path_map': {
                'mask':  r"C:\Users\Becky\Documents\raster_calculations\masked_all_nathab_esa2015.tif",
                'service': r"C:\Users\Becky\Documents\cnc_project\realized_sedimentdeposition_downstream_md5_1613b12643898c1475c5ec3180836770.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_sedimentdeposition_nathab.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
    ]

    for calculation in masked_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    NNth_nit = 322
    NNth_sed = 161
    NNth_poll = 982
    NNth_ffish = 75
    LOth_ffish = 0.001 # Min values are regression artifacts. Should be cut off at 10-1 tons per grid cell (~100 sq km). That’s 1 kg per sq km
    NNth_ffish = 30 # Max cut-off should be 3000 tons per grid cell. That’s 30 tons per sq km. (In between the 99 and 99.9th percentiles once small values are excluded)
    Max_mfish = 400 #this one's different because even though it's higher than the 99th percentile, there are some realistic values of up to 346 kg /km2
    LOth_MM = 0.00001
    clamped_service_list = [ #some services just have crazy high values that throw the whole percentiles off so we're clamping them to the 99th percentile
        {
            'expression': f'(service>{NNth_nit})*{NNth_nit} + (service<={NNth_nit})*(service>=0)*service + -9999*(service<0)', #sets anything above the 99th percentile value to that value, anything negative to nodata
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\potential_nitrogenretention_nathab_md5_95b25783b6114b63738f8d6b20d2af51.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "potential_nitrogenretention_nathab_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{NNth_sed})*({NNth_sed})+(service<={NNth_sed})*(service>=0)*service + -9999*(service<0)',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\potential_sedimentdeposition_nathab_md5_1a0dd289bee1fe09c30453ab80f9ddf4.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "potential_sedimentdeposition_nathab_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{NNth_poll})*({NNth_poll})+(service<={NNth_poll})*(service>=0)*service + -9999*(service<0)',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\realized_pollination_nathab_md5_feab479b3d6bf25a928c355547c9d9ab.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_pollination_nathab_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{NNth_ffish})*{NNth_ffish} + (service<={NNth_ffish})*(service>={LOth_ffish})*service + -9999*(service<{LOth_ffish})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\per_km_2_realized_fwfish_distrib_catch_md5_995d3d330ed5fc4462a47f7db44225e9.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fwfish_per_km2_clamped_3e-2_13.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{Max_mfish})*({Max_mfish})+(service<={Max_mfish})*service',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\needed_clamping\realized_marinefish_watson_2015_catch_Ind_Non_Ind_Rprt_IUU_md5_61e08ed60006e9ad23b74bcd44c61548.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_marinefish_watson_2015_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\realized_commercialtimber_forest_md5_99153e7a8177fd7ed6bb75a5fdc426e5.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_commercialtimber_forest_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\realized_domestictimber_forest_md5_3ee8a15ce8ed38b0710b8f6d74640b70.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_domestictimber_forest_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\realized_flood_nathab_md5_bf277802945a0a7067d2a90941e355e1.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_flood_nathab_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\realized_fuelwood_forest_md5_e86706b0ebe0d296acac30db78f2c284.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fuelwood_forest_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>{LOth_MM})*service + 0*(service<={LOth_MM})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\masked_rasters\needed_clamping\realized_grazing_natnotforest_md5_fbc4907814187d1be75b35932617af65.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_grazing_natnotforest_clamped.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
    ]

    for calculation in clamped_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    N90 = 7.3
    S90 = 9.8
    P90 = 8.4
    FF90 = 9.5
    MF90 =  9.3
    CT90 = 4.2
    DT90 = 5.8
    FW90 = 6.2
    F90 = 7.9
    G90 = 4.9
    CL90 = 6.1
    MR90 = 4.4
    NA90 = 8.2
    RT90 = 3.9
    CP90 = 2.7

    top_values_list = [
        {
            'expression': f'(service>={N90}) + 0*(service<{N90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_nitrogenretention_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_nitrogenretention_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={S90}) + 0*(service<{S90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_sedimentdeposition_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_sedimentdeposition_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={P90}) + 0*(service<{P90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_pollination_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_pollination_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={FF90}) + 0*(service<{FF90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_fwfish_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fwfish_per_km2_top90_3e-2_13.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={MF90}) + 0*(service<{MF90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_marinefish_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_marinefish_watson_2015_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={CT90}) + 0*(service<{CT90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_commercialtimber_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_commercialtimber_forest_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={DT90}) + 0*(service<{DT90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_domestictimber_binf.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_domestictimber_forest_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={F90}) + 0*(service<{F90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_flood_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_flood_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={FW90}) + 0*(service<{FW90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_fuelwood_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_fuelwood_forest_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={G90}) + 0*(service<{G90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_grazing_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_grazing_natnotforest_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={CL90}) + 0*(service<{CL90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_cultural_language_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_cultural_language_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={MR90}) + 0*(service<{MR90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_moisturerecycling_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_moisturerecycling_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={NA90}) + 0*(service<{NA90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_natureaccess10_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_natureaccess10_nathab_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={RT90}) + 0*(service<{RT90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_reeftourism_bin.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_reeftourism_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': f'(service>={CP90}) + 0*(service<{CP90})',
            'symbol_to_path_map': {
                'service': r"C:\Users\Becky\Documents\cnc_project\binned_services_global\realized_coastalprotectionbin_plusbarrierreefs_md5_a3f43a2e60e5976799d257ad9561731f.tif",
            },
            'target_nodata': -9999,
            'target_raster_path': "realized_coastalprotection_top90.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
    ]

    for calculation in top_values_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    #loop to set thresholds

    for base_raster_path, threshold, target_raster_path in [
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_pollination_md5_06f52f2854ae1c584742d587b1c31359.tif", 0.06, "top04_pollination.tif"),
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_flood_md5_f1237e76a41039e22629abb85963ba16.tif", 0.05, "top30_flood.tif"),
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_grazing_md5_d03b584dac965539a77bf96cba3f8096_masked_md5_db038b499342efa926c3c5815c822fe3.tif", 0.1, "top15_grazing.tif"),
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_nitrogen_downstream_md5_437e1759b0f994b47add4baf76509bbe_masked_md5_ac82368cedcfc692b0440b0cc0ed7fdb.tif", 0.06, "top25_nitrogen.tif"),
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_nwfp_masked_md5_754ba4d8cd0c54399fd816748a9e0091_masked_md5_f48ada73cb74cd59726b066db2f03855.tif", 0.05, "top10_nwfp.tif"),
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_sediment_downstream_md5_daa86f70232c5e1a8a0efaf0b2653db2_masked_md5_6e9050a9fcf3f08925343a48208aeab8.tif", 0.09, "top05_sediment.tif"),
            #(r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace\normalized_realized_timber_masked_md5_fc5ad0ff1f4702d75f204267fc90b33f_masked_md5_68df861a8e4c5cbb0e800f389690a792.tif", 0.13, "top15_timber.tif"),
            (r"C:\Users\Becky\Documents\raster_calculations\aggregate_realized_ES_score_nspwogf_md5_0ab07f38ed0290fea6142db188ae51f8.tif", 0.30, "top40_nspwogf.tif"),
            ]:

        mask_expr_dict = {
            'expression': 'raster > %f' % threshold,
            'symbol_to_path_map': {
                'raster': base_raster_path,
            },
            'target_nodata': -1,
            'target_raster_path': target_raster_path,
        }

        raster_calculations_core.evaluate_calculation(
            mask_expr_dict, TASK_GRAPH, WORKSPACE_DIR)


    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return

    #looping the same mask over a bunch of rasters

    base_directory = r"C:\Users\Becky\Documents\raster_calculations\CNC_workspace"

    masked_workspace_dir = 'masked_workspace_dir'
    ecoshard_workspace_dir = 'ecoshard_dir'
    for dirname in [masked_workspace_dir, ecoshard_workspace_dir]:
        try:
            os.makedirs(dirname)
        except OSError:
            pass

    for path in glob.glob(os.path.join(base_directory, '*.tif')):
        path_root_name = os.path.splitext(os.path.basename(path))[0]
        target_raster_path = os.path.join(
            masked_workspace_dir, '%s_masked.tif' % (path_root_name))

        remasking_expression = {
                'expression': 'mask*service',
                'symbol_to_path_map': {
                    'mask': 'masked_nathab_esa_nodata_md5_7c9acfe052cb7bdad319f011e9389fb1.tif',
                    'service': path,
                },
                'target_nodata': -1,
                'target_raster_path': target_raster_path,
                 ###file name split off from its path and its ecoshard too because it will be re-ecosharded
                'target_pixel_size': (0.002777777777778, -0.002777777777778),
            }

        raster_calculations_core.evaluate_calculation(
            remasking_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    subprocess.check_call("python -m ecoshard ./masked_workspace_dir/*.tif --hash_file --rename --buildoverviews --interpolation_method average")

    TASK_GRAPH.join()
    TASK_GRAPH.close()



    clamping_service_list = [
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_potential_flood.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_potential_flood.tif",
        },
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_potential_moisture.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_potential_moisture.tif",
        },
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_realized_flood.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_realized_flood.tif",
        },
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_realized_moisture.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_realized_moisture.tif",
        },
    ]

    for calculation in clamping_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)


    TASK_GRAPH.join()
    TASK_GRAPH.close()


    return #terminates at this point


    # just build overviews
    raster_calculation_list = [
        {
            'expression': 'x',
            'symbol_to_path_map': {
                'x': '../nathab_potential_pollination.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "potential_pollination.tif",
            'build_overview': True,
        },
    ]

    for calculation in raster_calculation_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()



     #dasgupta calcs:

    raster_list = [
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4\prod_total_realized_en_10s_ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4\prod_total_potential_en_10s_ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'default_nan': -1, # this is necessary because divides by 0's; could also set them to 0 instead
            'target_raster_path': "percent_realized_current.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78\prod_total_realized_en_10s_lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78\prod_total_potential_en_10s_lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_bau.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182\prod_total_realized_en_10s_lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182\prod_total_potential_en_10s_lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_cons.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_mid\prod_total_realized_en_10s_lulc_WB_mid.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_mid\prod_total_potential_en_10s_lulc_WB_mid.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_mid.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4\prod_total_realized_va_10s_ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4\prod_total_potential_va_10s_ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_current_va.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78\prod_total_realized_va_10s_lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78\prod_total_potential_va_10s_lulc_WB_bau_esa_classes_md5_b411f14d7cff237e3415c5afa26d4b78.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_bau_va.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182\prod_total_realized_va_10s_lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182\prod_total_potential_va_10s_lulc_WB_cons_esa_classes_md5_8c150474406a3f230b992399429bd182.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_cons_va.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'total_realized /total_potential',
            'symbol_to_path_map': {
                'total_realized': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_mid\prod_total_realized_va_10s_lulc_WB_mid.tif",
                'total_potential': r"C:\Users\Becky\Documents\dasgupta\nci_ag_multi_lulc\lulc_WB_mid\prod_total_potential_va_10s_lulc_WB_mid.tif",
            },
            'target_nodata': -1,
            'default_nan': -1,
            'target_raster_path': "percent_realized_mid_va.tif",
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
    ]

    for calculation in raster_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return


    #NCI

    single_expression = {
        'expression': 'averageraster*mask - raster2*(mask>1)',
        'symbol_to_path_map': {
            'raster2': r"C:\Users\Becky\Documents\raster_calculations\fertilizers\NitrogenApplication_Rate_md5_caee837fa0e881be0c36c1eba1dea44e.tif",
            'averageraster': r"C:\Users\Becky\Documents\raster_calculations\fertilizer_average_raster.tif",
            'mask': r"C:\Users\Becky\Documents\raster_calculations\fertilizer_valid_count_raster.tif",
        },
        'target_nodata': -9999,
        'target_raster_path': "Intensified_NitrogenApplication_Rate_gapfilled.tif",
        'target_pixel_size': (0.08333333333333332871, -0.08333333333333332871),
        'resample_method': 'average'
    }

    raster_calculations_core.evaluate_calculation(
        single_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return



if __name__ == '__main__':
    TASK_GRAPH = taskgraph.TaskGraph(WORKSPACE_DIR, NCPUS, 5.0)
    main()
