import os
import cv2
import numpy as np
import pandas as pd
import math

from common import utils


class MapDataset:
    def __init__(self, need_index, overwirte, index_name):
        self.need_index = need_index
        self.index_name = index_name

        self.df = None

        if self.need_index:
            if os.path.isfile(self.index_name) and not overwirte:
                    self.df = pd.read_csv(self.index_name)
                    print(f'{self.index_name} already exist, try to append to it')
            else:
                self.df = pd.DataFrame([], columns=['StreetMaps', 'DEMMaps', 'graph_min', 'graph_max'])
                self.df.to_csv(self.index_name, index=False)
        return

    def height_to_rgb(self, graph, normal_delta):
        graph_max = np.max(graph)
        graph_min = np.min(graph)
        print("Max is " + str(graph_max))
        print("Min is " + str(graph_min))
        graph_delta = graph_max - graph_min

        img_unit = 255.0
        if normal_delta:
            hi_gap_idx = math.ceil(graph_delta / img_unit)
            if hi_gap_idx == 0:  # hi_gap_idx >= 1
                hi_gap_idx = 1
            graph_delta = hi_gap_idx * img_unit

        img_graph = img_unit * (graph - graph_min) / graph_delta
        img_data = {'img_graph': img_graph, 'graph_max': graph_max, 'graph_min': graph_min}
        return img_data

    def height_to_rgb_cstred(self, graph, local_max, local_min):
        graph_max = np.max(graph)
        graph_min = np.min(graph)
        graph_max = np.max([graph_max, local_max])
        graph_min = np.min([graph_min, local_min])
        print("Max is " + str(graph_max))
        print("Min is " + str(graph_min))
        graph_delta = graph_max - graph_min
        if graph_delta == 0:
            graph_delta = 0.00001
        img_graph = 255 * (graph - graph_min) / graph_delta
        img_data = {'img_graph': img_graph, 'graph_max': graph_max, 'graph_min': graph_min}
        return img_data

    def write_to_export(self, img_data, path, name):
        filename = path + name
        cv2.imwrite(filename, img_data['img_graph'])
        return

    def export_to_dataset(self, img_data, path, name):
        append_df = pd.DataFrame(
            [[name, name, img_data['graph_min'], img_data['graph_max']]],
            columns=['StreetMaps', 'DEMMaps', 'graph_min', 'graph_max'])
        append_df.to_csv(self.index_name, mode='a', header=False, index=False)
        self.write_to_export(img_data, path, name)
        return

    def write_to_export_np(self, graph, path, name):
        filename = os.path.join(path, name)
        np.save(filename, graph)
        return

    def export_to_dataset_np(self, graph, path, name):
        npy_name = utils.to_numpy_name(name)
        append_df = pd.DataFrame(
            [[name, npy_name]],
            columns=['StreetMaps', 'DEMMaps'])
        append_df.to_csv(self.index_name, mode='a', header=False, index=False)
        self.write_to_export_np(graph, path, npy_name)
        return
