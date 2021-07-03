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
