from __future__ import print_function
import os
import sys
import numpy as np
from common.type import *

SRTM_DICT = {'SRTM1': 3601, 'SRTM3': 1201}

# Get the type of SRTM files or use SRTM1 by default
SRTM_TYPE = os.getenv('SRTM_TYPE', 'SRTM1')
SAMPLES = SRTM_DICT[SRTM_TYPE]

# put uncompressed hgt files in HGT_DIR, defaults to 'hgt'
HGTDIR = os.getenv('HGT_DIR', '..\\database\\')


def get_elevation(lat, lon):
    hgt_file = get_file_name(lat, lon)
    if hgt_file:
        return ERROR, read_elevation_from_file(hgt_file, lat, lon)
    # Treat it as data void as in SRTM documentation
    # if file is absent
    return RIGHT, None


def get_elevation_area(lat_st, lon_st, lat_ed, lon_ed):
    divided_area1 = divide_by_integer(lat_st, lat_ed)
    divided_area2 = divide_by_integer(lon_st, lon_ed)
    areas = get_divided_area(divided_area1, divided_area2)

    intact_graph = None
    row_graph = None
    local_max = float('-inf')
    local_min = float('inf')
    for row_area in areas:
        for area in row_area:
            err, graph, area_max, area_min = get_elevation_area_single_graph(area[0], area[1], int(area[2]), int(area[3]))
            if err:
                return err, None, 0, 0

            local_max = np.max([local_max, area_max])
            local_min = np.min([local_min, area_min])

            # Concatenate graphs to row graph
            if row_graph is None:
                row_graph = graph
            else:
                row_graph = np.concatenate((row_graph, graph), axis=1)
        # Concatenate row graphs to intact graph
        if intact_graph is None:
            intact_graph = row_graph
        else:
            intact_graph = np.concatenate((row_graph, intact_graph), axis=0)
        row_graph = None
    return RIGHT, intact_graph, local_max, local_min


def get_elevation_area_len(lat, lon, lat_len, lon_len):
    lat_ed = lat + lat_len / (SAMPLES - 1)
    lon_ed = lon + lon_len / (SAMPLES - 1)
    divided_area1 = divide_by_integer(lat, lat_ed)
    divided_area2 = divide_by_integer(lon, lon_ed)
    areas = get_divided_area(divided_area1, divided_area2)

    intact_graph = None
    row_graph = None
    local_max = float('-inf')
    local_min = float('inf')
    for row_area in areas:
        for area in row_area:
            err, graph, area_max, area_min = get_elevation_area_single_graph(area[0], area[1], int(area[2]), int(area[3]))
            if err:
                return err, None, 0, 0

            local_max = np.max([local_max, area_max])
            local_min = np.min([local_min, area_min])

            # Concatenate graphs to row graph
            if row_graph is None:
                row_graph = graph
            else:
                row_graph = np.concatenate((row_graph, graph), axis=1)
        # Concatenate row graphs to intact graph
        if intact_graph is None:
            intact_graph = row_graph
        else:
            intact_graph = np.concatenate((row_graph, intact_graph), axis=0)
        row_graph = None
    return RIGHT, intact_graph, local_max, local_min


def get_elevation_area_single_graph(lat, lon, lat_len, lon_len):
    lat_ed = lat + lat_len / (SAMPLES - 1)
    lon_ed = lon + lon_len / (SAMPLES - 1)
    if lat_ed > int(lat) + 1 or lon_ed > int(lon) + 1:
        print('Sampling area not in a single graph!')
        return ERROR, None, 0, 0

    hgt_file = get_file_name(lat, lon)
    if hgt_file:
        with open(hgt_file, 'rb') as hgt_data:
            # HGT is 16bit signed integer(i2) - big endian(>)
            elevations = np.fromfile(
                hgt_data,  # binary data
                np.dtype('>i2'),  # data type
                SAMPLES * SAMPLES  # length
            ).reshape((SAMPLES, SAMPLES))

            area_max = np.max(elevations)
            area_min = np.max(elevations)

            lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
            lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))

            graph = np.zeros((lat_len, lon_len), dtype=int, order='C')
            for i in range(0, lat_len):
                for j in range(0, lon_len):
                    lat_idx = lat_row + i
                    lon_idx = lon_row + j
                    elev = elevations[SAMPLES - 1 - lat_idx, lon_idx].astype(int)
                    graph[lat_len - 1 - i, j] = elev

            return RIGHT, graph, area_max, area_min

    print('Fail to open file at (%(lat)02d, %(lon)02d)' % {'lat': lat, 'lon': lon})
    return ERROR, None, 0, 0


def divide_by_integer(st, ed):
    i = 0
    done = False
    # divided_area is an ordered set, its element are ordered from small to large
    divided_area = []
    pre_sp = st
    sp = int(st)
    while not done:
        sp = sp + 1
        if sp < ed:
            divided_area.append([pre_sp, sp])
            pre_sp = sp
        else:
            divided_area.append([pre_sp, ed])
            done = True
    return divided_area


def get_divided_area(divided_area1, divided_area2):
    areas = []
    for area_i in divided_area1:
        row_areas = []
        for area_j in divided_area2:
            ilen = (area_i[1] - area_i[0]) * (SAMPLES - 1)
            jlen = (area_j[1] - area_j[0]) * (SAMPLES - 1)
            row_areas.append([area_i[0], area_j[0], ilen, jlen])
        areas.append(row_areas)
    return areas


def read_elevation_from_file(hgt_file, lat, lon):
    with open(hgt_file, 'rb') as hgt_data:
        # HGT is 16bit signed integer(i2) - big endian(>)
        elevations = np.fromfile(
            hgt_data,  # binary data
            np.dtype('>i2'),  # data type
            SAMPLES * SAMPLES  # length
        ).reshape((SAMPLES, SAMPLES))

        lat_row = int(round((lat - int(lat)) * (SAMPLES - 1), 0))
        lon_row = int(round((lon - int(lon)) * (SAMPLES - 1), 0))

        return elevations[SAMPLES - 1 - lat_row, lon_row].astype(int)


def get_file_name(lat, lon):
    """
    Returns filename such as N27E086.hgt, concatenated
    with HGTDIR where these 'hgt' files are kept
    """
    ns = 'N'
    ew = 'E'

    if lat >= 0:
        ns = 'N'
    elif lat < 0:
        ns = 'S'

    if lon >= 0:
        ew = 'E'
    elif lon < 0:
        ew = 'W'

    hgt_file = "%(ns)s%(lat)02d%(ew)s%(lon)03d.hgt" % \
               {'lat': abs(lat), 'lon': abs(lon), 'ns': ns, 'ew': ew}
    hgt_file_path = os.path.join(HGTDIR, hgt_file)
    if os.path.isfile(hgt_file_path):
        return hgt_file_path
    else:
        return None

