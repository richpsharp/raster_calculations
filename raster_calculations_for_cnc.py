"""These calculations are for the Critical Natural Capital paper."""
import sys
import os
import logging
import multiprocessing

import raster_calculations_core
from osgeo import gdal
import taskgraph

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
    

    normalized_service_list = [
        {
            'expression': 'service/ percentile(service, 99)',
            'symbol_to_path_map': {
                'service': 'https://storage.googleapis.com/critical-natural-capital-ecoshards/realized_nitrogenretention_downstream_md5_82d4e57042482eb1b92d03c0d387f501.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "raw_normalized_realized_nitrogen_downstream.tif",
        },
        {
            'expression': 'service/ percentile(service, 99)',
            'symbol_to_path_map': {
                'service': 'https://storage.googleapis.com/critical-natural-capital-ecoshards/realized_sedimentdeposition_downstream_md5_1613b12643898c1475c5ec3180836770.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "raw_normalized_realized_sediment_downstream.tif",
        },
        {
            'expression': 'service/ percentile(service, 99)',
            'symbol_to_path_map': {
                'service': 'https://storage.googleapis.com/critical-natural-capital-ecoshards/realized_pollination_md5_8a780d5962aea32aaa07941bde7d8832.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "raw_normalized_realized_pollination.tif",
        },
        
    ]

    for calculation in normalized_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()

    clamping_service_list = [
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_realized_nitrogen_downstream.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_realized_nitrogen_downstream.tif",
        },
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_realized_sediment_downstream.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_realized_sediment_downstream.tif",
        },
        {
            'expression': '(val >= 0) * (val < 1) * val + (val >= 1)',
            'symbol_to_path_map': {
                'val': "raw_normalized_realized_pollination.tif",
            },
            'target_nodata': -1,
            'target_raster_path': "normalized_realized_pollination.tif",
        },
    ]

    for calculation in clamping_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)


    TASK_GRAPH.join()
    
    synthesis_index_expression = {
            'expression': 'nitrogen + sediment + pollination + nwfp + timber + grazing',
            'symbol_to_path_map': {
                'nitrogen': "normalized_realized_nitrogen_downstream.tif",
                'sediment': "normalized_realized_sediment_downstream.tif",
                'pollination': "normalized_realized_pollination.tif",
                'nwfp': 'https://storage.googleapis.com/critical-natural-capital-ecoshards/realized_nwfp_md5_f1cce72af652fd16e25bfa34a6bddc63.tif',
                'timber': 'https://storage.googleapis.com/critical-natural-capital-ecoshards/realized_timber_md5_5154151ebe061cfa31af2c52595fa5f9.tif',
                'grazing': 'https://storage.googleapis.com/critical-natural-capital-ecoshards/realized_grazing_md5_19085729ae358e0e8566676c5c7aae72.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "aggregate_realized_score_nspntg.tif",
    }

    raster_calculations_core.evaluate_calculation(
        synthesis_index_expression, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    return #terminates at this point


    masker_list = [
         {
            # the %s is a placeholder for the string we're passing it using this function that lists every number in the range and takes away the [] of the list and turns it into a string
            'expression': 'mask(raster, %s, invert=False)'%(str([]+[x for x in range(50,181)])[1:-1]),
            'symbol_to_path_map': {
                'raster': 'https://storage.googleapis.com/ipbes-ndr-ecoshard-data/ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif',
            },
            'target_nodata': -1,
            'target_raster_path': 'masked_nathab_esa.tif',
        },
        {
            'expression': 'mask(raster, %s, invert=False)'%(str([20,30]+[x for x in range(80,127)])[1:-1]),
            'symbol_to_path_map': {
                'raster': 'https://storage.googleapis.com/ecoshard-root/working-shards/coopernicus_landcover_discrete_compressed_md5_264bda5338a02e4a6cc10412b8edad9f.tif',
            },
            'target_nodata': -1,
            'target_raster_path': 'masked_nathab_copernicus.tif',
        },
        {
            # this is for masking out forest from natural habitat, for livestock production
            # this counts the >50% herbaceous / < 50% tree cover category as "not forest"; also includes lichens, mosses  and shrubland which maybe isn't totally edible by cattle either
            'expression': 'mask(raster, %s, invert=False)'%(str([x for x in range(110,154)]+[180])[1:-1]),
            'symbol_to_path_map': {
                'raster': 'https://storage.googleapis.com/ipbes-ndr-ecoshard-data/ESACCI-LC-L4-LCCS-Map-300m-P1Y-2015-v2.0.7_md5_1254d25f937e6d9bdee5779d377c5aa4.tif',
            },
            'target_nodata': -1,
            'target_raster_path': 'masked_nathab_notforest_esa.tif',
        },
    ]
    for masker in masker_list:
       raster_calculations_core.evaluate_calculation(
            masker, TASK_GRAPH, WORKSPACE_DIR)
    

    TASK_GRAPH.join()
    TASK_GRAPH.close()
       
    
    grazing_service_list = [
        {
            'expression': 'mask*service',
            'symbol_to_path_map': {
                'mask': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/masked_nathab_notforest_esa.tif',
                'service': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/potential_grazing_value.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "potential_grazing.tif",
            'build_overview': True,
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
            'resample_method': 'average'
        },
        {
            'expression': 'mask*service',
            'symbol_to_path_map': {
                'mask': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/masked_nathab_notforest_esa.tif',
                'service': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/realised_grazing_value.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "realized_grazing.tif",
            'build_overview': True,
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
            'resample_method': 'average'
        },
    ]

    for calculation in grazing_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()
    
    potential_service_list = [
        {
            'expression': 'mask*service',
            'symbol_to_path_map': {
                'mask': 'https://storage.googleapis.com/ecoshard-root/working-shards/masked_nathab_esa_md5_40577bae3ef60519b1043bb8582a07af.tif',
                'service': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/ESACCI_LC_L4_LCCS_borrelli_sediment_deposition_md5_3e0ccb34352269d7eb688dd488de002f.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "potential_sedimentdeposition.tif",
            'build_overview': True,
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
        },
        {
            'expression': 'mask*service',
            'symbol_to_path_map': {
                'mask': 'https://storage.googleapis.com/ecoshard-root/working-shards/masked_nathab_esa_md5_40577bae3ef60519b1043bb8582a07af.tif',
                'service': 'https://storage.googleapis.com/ipbes-natcap-ecoshard-data-for-publication/worldclim_esa_2015_n_retention_md5_d10a396b8f0fee70dd3bbd3524a6a97c.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "potential_nitrogenretention.tif",
            'build_overview': True,
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
            'resample_method': 'average'
        },
    ]

    for calculation in potential_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()

    realized_service_list = [
        {
            'expression': 'beneficiaries*service',
            'symbol_to_path_map': {
                'beneficiaries': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/downstream_beneficiaries_md5_68495f4bbdd889d7aaf9683ce958a4fe.tif',
                'service': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/potential_nitrogenretention.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "realized_nitrogenretention_downstream.tif",
            'build_overview': True,
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
            'resample_method': 'average'
        },
        {
            'expression': 'beneficiaries*service',
            'symbol_to_path_map': {
                'beneficiaries': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/downstream_beneficiaries_md5_68495f4bbdd889d7aaf9683ce958a4fe.tif',
                'service': 'C:/Users/Becky/Documents/raster_calculations/CNC_workspace/potential_sedimentdeposition.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "realized_sedimentdeposition_downstream.tif",
            'build_overview': True,
            'target_pixel_size': (0.002777777777778, -0.002777777777778),
            'resample_method': 'average'
        },
    ]

    for calculation in realized_service_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    TASK_GRAPH.join()
    TASK_GRAPH.close()


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

    #calculate people fed equivalents from individual nutrient data
    raster_calculation_list = [
        {
            'expression': '(va/486980 + en/3319921 + fo/132654) / 3',
            'symbol_to_path_map': {
                'va': '../pollination_esa_tifs/prod_poll_dep_realized_va_10s_ESACCI_LC_L4_LCSS.tif',
                'en': '../pollination_esa_tifs/prod_poll_dep_realized_en_10s_ESACCI_LC_L4_LCSS.tif',
                'fo': '../pollination_esa_tifs/prod_poll_dep_realized_fo_10s_ESACCI_LC_L4_LCSS.tif',
            },
            'target_nodata': -1,
            'target_raster_path': "pollination_ppl_fed_on_ag_10s_esa.tif",
            'build_overview': True,
        },
    ]

    for calculation in raster_calculation_list:
        raster_calculations_core.evaluate_calculation(
            calculation, TASK_GRAPH, WORKSPACE_DIR)

    


if __name__ == '__main__':
    TASK_GRAPH = taskgraph.TaskGraph(WORKSPACE_DIR, NCPUS, 5.0)
    main()
