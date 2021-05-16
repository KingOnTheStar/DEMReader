import os
import cv2
import numpy as np
import pandas as pd


class DataPostProcessor:
    def __init__(self, street_map_database, tmp_export_path,
                 post_processing_index_path, post_processing_dem_path,
                 post_processing_street_path, post_processing_sketch_path):
        self.street_map_database = street_map_database
        self.tmp_export_path = tmp_export_path
        self.post_processing_index_path = post_processing_index_path
        self.post_processing_DEM_path = post_processing_dem_path
        self.post_processing_street_path = post_processing_street_path
        self.post_processing_sketch_path = post_processing_sketch_path

        self.post_processing_index_name = os.path.join(self.post_processing_index_path, 'index.csv')
        self.index_df = None
        return

    def open_index(self):
        self.index_df = pd.read_csv(self.post_processing_index_name)

    def remove_replica(self, remove_img_same_to):
        remove_num = 0
        imgs = os.listdir(self.post_processing_street_path)
        image_aim = cv2.imread(os.path.join(self.post_processing_street_path, remove_img_same_to))
        for img in imgs:
            if img == remove_img_same_to:
                continue
            img_name = os.path.join(self.post_processing_street_path, img)
            image_now = cv2.imread(img_name)
            difference = cv2.subtract(image_aim, image_now)
            result = not np.any(difference)
            if result:
                remove_num += 1
                self.remove_strt_dem_ske(img)
                print(img)
        self.index_df.to_csv(self.post_processing_index_name, mode='w', index=False)
        print(f'Remove {remove_num} images')
        return

    def remove_strt_dem_ske(self, name):
        strt_name = os.path.join(self.post_processing_street_path, name)
        dem_name = os.path.join(self.post_processing_DEM_path, name)
        ske_name = os.path.join(self.post_processing_sketch_path, name)

        if os.path.exists(strt_name):
            os.remove(strt_name)
        if os.path.exists(dem_name):
            os.remove(dem_name)
        if os.path.exists(ske_name):
            os.remove(ske_name)

        row_indexs = self.index_df[self.index_df['StreetMaps'] == name].index
        self.index_df.drop(row_indexs, inplace=True)
        return

    def check(self):
        for index, row in self.index_df.iterrows():
            name = row['StreetMaps']
            strt_name = os.path.join(self.post_processing_street_path, name)
            if not os.path.exists(strt_name):
                row_indexs = self.index_df[self.index_df['StreetMaps'] == name].index
                self.index_df.drop(row_indexs, inplace=True)
                print(f'Remove {name} in index')

        self.index_df.to_csv(self.post_processing_index_name, mode='w', index=False)
        return
