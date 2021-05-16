import cv2
import numpy as np
from common import utils
from DEM import srtm
from DEM import StreetMapInfo
from DEM.MapWriter import *


class DataProcessor:
    def __init__(self, street_map_database, tmp_export_path,
                 post_processing_index_path, post_processing_dem_path,
                 post_processing_street_path):
        self.street_map_database = street_map_database
        self.tmp_export_path = tmp_export_path
        self.post_processing_index_path = post_processing_index_path
        self.post_processing_DEM_path = post_processing_dem_path
        self.post_processing_street_path = post_processing_street_path
        return

    def process_to_np(self):
        dataset = MapDataset(True, True, os.path.join(self.post_processing_index_path, 'index.csv'))
        stmap_names = StreetMapInfo.get_street_map_file_names(self.street_map_database)
        for name in stmap_names:
            lat_lons = StreetMapInfo.stmap_name_to_lat_lon(name)
            err, graph, local_max, local_min = srtm.get_elevation_area(lat_lons[0], lat_lons[1], lat_lons[2],
                                                                       lat_lons[3])
            if err:
                print('ERROR HAPPENDED!')
                return
            # img_data = dataset.height_to_rgb(graph, True)
            # img_data = dataset.height_to_rgb_cstred(graph, local_max, local_min)
            dataset.export_to_dataset_np(graph, self.tmp_export_path, name)
            # dataset.write_to_export(img_data, export_path, name)
        self.resize_np((64, 64))
        return

    def resize_np(self, dim=(256, 256)):
        utils.resize_all_img(self.street_map_database, self.post_processing_street_path, dim=dim)
        utils.resize_all_np(self.tmp_export_path, self.post_processing_DEM_path, dim=dim)
        return

    def process_to_img(self):
        dataset = MapDataset(True, True, os.path.join(self.post_processing_index_path, 'index.csv'))
        stmap_names = StreetMapInfo.get_street_map_file_names(self.post_processing_street_path)
        for name in stmap_names:
            lat_lons = StreetMapInfo.stmap_name_to_lat_lon(name)
            err, graph, local_max, local_min = srtm.get_elevation_area(lat_lons[0], lat_lons[1], lat_lons[2],
                                                                       lat_lons[3])
            if err:
                print('ERROR HAPPENDED!')
                return
            img_data = dataset.height_to_rgb(graph, True)
            # img_data = dataset.height_to_rgb_cstred(graph, local_max, local_min)
            dataset.export_to_dataset(img_data, self.tmp_export_path, name)
            # dataset.write_to_export(img_data, export_path, name)
        self.resize_img()
        return

    def resize_img(self, dim=(256, 256)):
        utils.resize_all_img(self.street_map_database, self.post_processing_street_path, dim=dim)
        utils.resize_all_img(self.tmp_export_path, self.post_processing_DEM_path, dim=dim)
        return

    def test(self):
        arr = np.load(os.path.join(self.post_processing_index_path, '/N31.200E119.810N31.210E119.820.npy'))
        print(np.max(arr))
        dataset = MapDataset(True, False, os.path.join(self.post_processing_index_path, 'index.csv'))
        print(arr.shape)
        arr = np.resize(arr, (64, 64))
        img_data = dataset.height_to_rgb(arr, True)
        dataset.export_to_dataset(img_data, self.tmp_export_path, 'ff.png')
        return
