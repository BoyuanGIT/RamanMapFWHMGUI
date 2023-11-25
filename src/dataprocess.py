import os
import pandas as pd
import numpy as np
import ramanspy as rpy

# 传入文件路径，处理数据，返回xy列表，xy不重复列表，rpy的image contanier


def data_load(filename):
    try:
        # 尝试从文件中读取数据
        rawdata = pd.read_csv(filename, header=None).to_numpy()

        # 处理数据
        axis = rawdata[3:, 0].astype(float)
        x = rawdata[1, 1:].astype(float)
        y = rawdata[2, 1:].astype(float)
        xlist = np.unique(x)
        ylist = np.unique(y)
        xreshape = x.reshape(len(ylist), len(xlist))
        yreshape = y.reshape(len(ylist), len(xlist))
        RMrawdata = rpy.SpectralImage(
             rawdata[3:, 1:].T.reshape(len(ylist), len(xlist), len(axis)),
             axis
             )

        # 返回有用的信息
        return {
            'rawdata': rawdata,
            'axis': axis,
            'x': x,
            'y': y,
            'xlist': xlist,
            'ylist': ylist,
            'xreshape': xreshape,
            'yreshape': yreshape,
            'RMrawdata': RMrawdata
        }
    except Exception as e:
        # 处理异常情况，例如文件不存在或格式不正确
        print(f"Error loading data from {filename}: {e}")
        # 返回一个标志错误的值或者抛出异常，具体取决于你的需求
        return None