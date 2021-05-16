import os
import cv2
import numpy as np

from common.nparray_intpla import NparrayIntpla


def resize_all_img(path, out_path, dim=(128, 128)):
    names = os.listdir(path)
    for name in names:
        img = cv2.imread(os.path.join(path, name))
        ret = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(out_path, name), ret)
    return


def resize_all_np(path, out_path, dim=(128, 128)):
    names = os.listdir(path)
    for name in names:
        arr = np.load(os.path.join(path, name))
        arr = NparrayIntpla.clip_array(arr)
        arr = NparrayIntpla.resize2d(arr, dim)
        arr = np.expand_dims(arr, axis=2)
        np.save(os.path.join(out_path, name), arr)
    return


def remove_suffix(filename):
    dot_char = '.'
    filenames = filename.split(dot_char)
    prefixname = ''
    for i in range(len(filenames) - 1):
        if i != 0:
            prefixname += dot_char
        prefixname += filenames[i]
    return prefixname


def to_numpy_name(filename):
    prefixname = remove_suffix(filename)
    return prefixname + '.npy'
