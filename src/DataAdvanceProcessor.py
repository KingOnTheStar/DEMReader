import os
import cv2 as cv
import numpy as np
import pandas as pd
from advance_processing.integral_grad import *


class DataAdvanceProcessor:
    def __init__(self):
        return

    @staticmethod
    def gen_grad_img_format(input_path, output_path):
        integral_grad = IntegralGrad()
        imgs = os.listdir(input_path)
        for img_name in imgs:
            img_full_name = os.path.join(input_path, img_name)
            base_name = os.path.splitext(img_name)[0]
            np_name = ''.join([base_name, '.npy'])
            np_out_name = os.path.join(output_path, np_name)

            grad_np = integral_grad.work_to_grad_np(img_full_name)
            np.save(np_out_name, grad_np)

            # Load
            # out = np.load(np_out_name)
            # if (out == grad_np).all():
            #     print('yes')
            print(img_name)
        return

    @staticmethod
    def cal_grad_mean_std(input_path):
        npdata = os.listdir(input_path)
        means = []
        stds = []
        minval = 256
        maxval = -256
        for np_name in npdata:
            np_full_name = os.path.join(input_path, np_name)
            # Load
            data = np.load(np_full_name)
            np_mean = np.mean(data, axis=(0, 1))
            means.append(np_mean)
            local_min = np.min(data)
            local_max = np.max(data)
            minval = minval if minval <= local_min else local_min
            maxval = maxval if maxval >= local_max else local_max
        mean = np.mean(means, axis=0)

        for np_name in npdata:
            np_full_name = os.path.join(input_path, np_name)
            # Load
            data = np.load(np_full_name)
            pixel_num = data.shape[0] * data.shape[1]
            np_std_sum = np.sum(np.power(data - mean, 2), axis=(0, 1)) / pixel_num
            stds.append(np_std_sum)
        std = np.sqrt(np.mean(stds, axis=0))

        mean = mean / 255
        std = std / 255
        print('mean: ' + str(mean))
        print('std: ' + str(std))
        print('minval: ' + str(minval))
        print('maxval: ' + str(maxval))
        return mean, std
