import argparse
from DataProcessor import *
from DataPostProcessor import *
from DataAdvanceProcessor import *


def main():
    parser = argparse.ArgumentParser(description='Data Processor')
    parser.add_argument('--processing_type', action='store', type=str, default='GeneratingDEM',
                        help='Street map database, GeneratingDEM|CalMeanStd|RemoveReplica|Check|AdvanceDataProcessing')
    parser.add_argument('--street_map_database', action='store', type=str, default='../references/StreetMaps/',
                        help='Street map database')
    parser.add_argument('--tmp_export_path', action='store', type=str, default='../export/',
                        help='Tmp export path')
    parser.add_argument('--post_processing_index_path', action='store', type=str, default='../output/',
                        help='Post processing index path')
    parser.add_argument('--post_processing_dem_path', action='store', type=str, default='../output/DEMMaps/',
                        help='Post processing dem path')
    parser.add_argument('--post_processing_street_path', action='store', type=str, default='../output/StreetMaps/',
                        help='Post processing street path')
    parser.add_argument('--post_processing_sketch_path', action='store', type=str, default='D:/Data/SketchMap',
                        help='Post processing sketch path')
    parser.add_argument('--remove_img_same_to', action='store', type=str, default='N30.300E115.240N30.310E115.250.png',
                        help='Activated when processing_type == RemoveReplica')
    parser.add_argument('--advance_processing_type', action='store', type=str, default='GenGradImgFormat',
                        help='Activated when processing_type == AdvanceDataProcessing, GenGradImgFormat|CalGradMeanStd')
    parser.add_argument('--input_path', action='store', type=str, default='../output/DEMMaps/',
                        help='Input path for advance data processing')
    parser.add_argument('--output_path', action='store', type=str, default='../output/AdvanceDataProcessing/',
                        help='Output path for advance data processing')
    parser.add_argument('--tmp', action='store', type=str, default='',
                        help='Tmp')
    parser.add_argument('--tmp_path', action='store', type=str, default='',
                        help='Tmp path')
    arg = parser.parse_args()

    data_processor = DataProcessor(arg.street_map_database,
                                   arg.tmp_export_path,
                                   arg.post_processing_index_path,
                                   arg.post_processing_dem_path,
                                   arg.post_processing_street_path)

    data_post_processor = DataPostProcessor(arg.street_map_database,
                                            arg.tmp_export_path,
                                            arg.post_processing_index_path,
                                            arg.post_processing_dem_path,
                                            arg.post_processing_street_path,
                                            arg.post_processing_sketch_path)

    if arg.processing_type == 'GeneratingDEM':
        data_processor.process_to_img()
    elif arg.processing_type == 'CalMeanStd':
        data_post_processor.calculate_mean_std()
    elif arg.processing_type == 'RemoveReplica':
        data_post_processor.open_index()
        data_post_processor.remove_replica(arg.remove_img_same_to)
    elif arg.processing_type == 'Check':
        data_post_processor.open_index()
        data_post_processor.check()
    elif arg.processing_type == 'AdvanceDataProcessing':
        if arg.advance_processing_type == 'GenGradImgFormat':
            DataAdvanceProcessor.gen_grad_img_format(arg.input_path, arg.output_path)
        if arg.advance_processing_type == 'CalGradMeanStd':
            DataAdvanceProcessor.cal_grad_mean_std(arg.input_path)
    else:
        pass

    return


if __name__ == '__main__':
    main()
