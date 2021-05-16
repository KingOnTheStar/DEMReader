import os
import re


def get_street_map_file_names(database_path):
    return os.listdir(database_path)


def stmap_name_to_lat_lon(name):
    print(name)
    res = re.findall(r"\d+\.?\d*", name)
    north_st = float(res[0])
    south_st = float(res[1])
    north_ed = float(res[2])
    south_ed = float(res[3])
    return [north_st, south_st, north_ed, south_ed]
