import numpy as np
from scipy import interpolate


class NparrayIntpla:
    def __init__(self):
        return

    @staticmethod
    def clip_array(ori):
        if len(ori.shape) != 2:
            print('clip_array not support!')
            return None
        xlen = ori.shape[0]
        ylen = ori.shape[1]
        if xlen == ylen:
            return ori
        minlen = np.min([xlen, ylen])
        ret = ori[0: minlen, 0: minlen]
        return ret

    @staticmethod
    def resize2d(ori, shape):
        if len(ori.shape) != 2 \
                or len(shape) != 2:
            print('resize2d not support!')
            return None
        xlen = ori.shape[0]
        ylen = ori.shape[1]
        if xlen != ylen:
            print('resize2d xlen != ylen !')
            return None

        x = np.array(range(0, xlen))
        y = np.array(range(0, ylen))
        f = interpolate.interp2d(x, y, ori, kind='cubic')

        ret = np.zeros(shape=shape)
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                ret[j, i] = f(float(xlen) * i / shape[0], float(ylen) * j / shape[1])
        return ret
