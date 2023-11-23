import pandas as pd
import numpy as np
import ramanspy as rpy
from lmfit.models import VoigtModel
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os

#读取数据函数
def data_load(filename):
    rawdata = pd.read_csv(filename, header=None).to_numpy() #读取文件并转换为numpy数组
    xnum = len(set(rawdata[1, 1:])) #计算x坐标的数量
    ynum = len(set(rawdata[2, 1:])) #计算y坐标的数量
    axis = rawdata[3:,0] #获取峰位置并存入表
    x = rawdata[1, 1:].astype(float) #读取x轴所有坐标并转换为浮点数
    y = rawdata[2, 1:].astype(float) #读取y轴所有坐标并转换为浮点数
    unique_x = np.unique(x) #获取x轴唯一坐标
    unique_y = np.unique(y) #获取y轴唯一坐标


    return x, y, unique_x, unique_y, xnum, ynum, axis, rawdata


def rawdata_heatmap(selected_value, rawdata):
    # 寻找与 selected_value 近似相等的值在 rawdata[3:, 0] 中的位置
    indices = np.where(np.isclose(rawdata[3:, 0].astype(float), selected_value, atol=0.5))[0]

    row = indices[0]  # 使用第一个匹配的索引

    # 提取 x, y, z 数据
    x = rawdata[1, 1:].astype(float)
    
    y = rawdata[2, 1:].astype(float)
    
    unique_x, index_x = np.unique(x, return_index=True)
    unique_y, index_y = np.unique(y, return_index=True)
    lenx = len(unique_x)
    leny = len(unique_y)
    z = rawdata[row + 3, 1:].reshape(leny, lenx).astype(float)

    # 创建热图
    fig, ax = plt.subplots()
    im = ax.imshow(z, cmap='YlOrRd', aspect='auto', extent=[min(x), max(x), min(y), max(y)])

    # 设置 colorbar 标签
    cbar = fig.colorbar(im, ax=ax, label='Intensity')

    # 将colorbar标签放到左侧，整体左移0.5个单位距离
    cbar.ax.yaxis.set_label_coords(-1, 0.5)

    # 隐藏图形标题
    ax.set_title('')

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # 创建 Figures 文件夹路径
    figures_folder = os.path.join(os.getcwd(), 'Figures')
    os.makedirs(figures_folder, exist_ok=True)  # 如果文件夹不存在，创建文件夹

    # 构建图像文件的路径
    save_path = os.path.join(figures_folder, 'rawdataheatmap.png')

    # 保存图像到文件
    fig.savefig(save_path, bbox_inches='tight')
    plt.close(fig)  # 关闭图形，防止显示图形窗口

    return save_path

import os
import matplotlib.pyplot as plt

def rawdata_spectral(x, y, rawdata):
    # 寻找 x 在 rawdata[1, 1:] 中的位置
    x_indices = [i for i, val in enumerate(rawdata[1, 1:]) if float(val) == x]

    # 寻找 y 在 rawdata[2, 1:] 中的位置
    y_indices = [i for i, val in enumerate(rawdata[2, 1:]) if float(val) == y]

    # 获取同时具有 x, y 值的列的索引
    common_indices = list(set(x_indices) & set(y_indices))

    if not common_indices:
        print(f"No data found for x={x} and y={y}")
        return

    col = common_indices[0] + 1  # 加1是因为列的索引从1开始，而数组索引从0开始

    # 提取 x, y 数据
    x_values = rawdata[3:, 0].astype(float)
    y_values = rawdata[3:, col].astype(float)

    # 创建折线图
    fig, ax = plt.subplots(figsize=(491 / 80, 311 / 80))
    ax.plot(x_values, y_values, label='')
    ax.legend()

    # 创建 Figures 文件夹路径
    figures_folder = os.path.join(os.getcwd(), 'Figures')
    os.makedirs(figures_folder, exist_ok=True)  # 如果文件夹不存在，创建文件夹

    # 构建图像文件的路径
    save_path = os.path.join(figures_folder, 'rawdata_spectral.png')

    # 保存图像到文件
    fig.savefig(save_path, bbox_inches='tight')
    plt.close(fig)  # 关闭图形，防止显示图形窗口

    return save_path

def pipline_choice(choice_crop, peak_min, peak_max, choice_cosmic, choice_baseline, choice_norm, choice_denoise):
    # 初始化 Pipeline
    pipe = rpy.preprocessing.Pipeline([])

    if choice_crop:
        # 如果选择了 Crop，则获取用户输入的波数范围，并添加 Cropper 到 Pipeline
        wavenumber = (float(peak_min), float(peak_max))
        pipe.append(rpy.preprocessing.misc.Cropper(region=wavenumber))

    if choice_cosmic:
        # 如果选择了 Cosmic，则添加 WhitakerHayes 到 Pipeline
        pipe.append(rpy.preprocessing.despike.WhitakerHayes())

    if choice_baseline:
        # 如果选择了 Baseline，则添加 ASLS 到 Pipeline
        pipe.append(rpy.preprocessing.baseline.ASLS())

    if choice_norm:
        # 如果选择了 Normalization，则添加 MaxIntensity 到 Pipeline
        pipe.append(rpy.preprocessing.normalise.MaxIntensity())

    if choice_denoise:
        # 如果选择了 Denoise，则添加 Gaussian 到 Pipeline
        pipe.append(rpy.preprocessing.denoise.Gaussian())

    # 如果没有选择任何一个框，返回空值
    if not any([choice_crop, choice_cosmic, choice_baseline, choice_norm, choice_denoise]):
        return None

    return pipe

model = VoigtModel()
params = model.make_params(amplitude=1, center=965, sigma=1, gamma=1)
def vogitfit(preprocessed_data):
    data = np.column_stack((preprocessed_data.spectral_axis, preprocessed_data.spectral_data))
    x = data[:, 0]
    y = data[:, 1]
    result = model.fit(y, params, x=x)
    return result

def data_process(rawdata,pipe):
    
    x = rawdata[1,1:].astype(float)
    y = rawdata[2,1:].astype(float)
    axis = rawdata[3:,0].astype(float)
    ramandata =  rawdata[3:, 1:]
    ramandatalist = [ramandata[:, i].astype(float).tolist() for i in range(ramandata.shape[1])]
    final_data = [[] for _ in range(ramandata.shape[1])]
    for i in range(ramandata.shape[1]):
        final_data[i].append(x[i]) #1.处理完的x坐标
        final_data[i].append(y[i]) #2.处理完的y坐标
        final_data[i].append(rpy.SpectralContainer(ramandatalist[i], axis)) #3.处理前的数据rpy格式
        final_data[i].append(final_data[i][2].spectral_axis) #4.峰位置
        final_data[i].append(final_data[i][2].spectral_data) #5.处理前的峰强度
        final_data[i].append(pipe.apply(final_data[i][2])) #6.处理完的数据rpy格式
        final_data[i].append(pipe.apply(final_data[i][5]).spectral_axis) #7.处理完的峰位置
        final_data[i].append(pipe.apply(final_data[i][5]).spectral_data) #8.处理完的峰强度
        final_data[i].append(vogitfit(final_data[i][5]).best_fit) #9.拟合最优结果数组
        final_data[i].append(vogitfit(final_data[i][5]).params['fwhm'].value) #10.fwhm值
        final_data[i].append(vogitfit(final_data[i][5]).params['fwhm'].stderr) #11.fwhm值的标准差

    return final_data

def fwhm_heatmap(final_data):
    # 提取 x、y、强度值列
    x_values = np.asarray([row[0] for row in final_data])
    y_values = np.asarray([row[1] for row in final_data])
    unique_x, index_x = np.unique(x_values, return_index=True)
    unique_y, index_y = np.unique(y_values, return_index=True)
    lenx = len(unique_x)
    leny = len(unique_y)
    fwhm = np.asarray([row[9] for row in final_data]).reshape(leny, lenx).astype(float)

    # 创建热图
    fig, ax = plt.subplots()
    im = ax.imshow(fwhm, cmap='YlOrRd', aspect='auto', extent=[min(unique_x), max(unique_x), min(unique_y), max(unique_y)])

    # 设置 colorbar 标签
    cbar = fig.colorbar(im, ax=ax, label='FWHM')

    # 将colorbar标签放到左侧，整体左移0.5个单位距离
    cbar.ax.yaxis.set_label_coords(-1, 0.5)

    # 隐藏图形标题
    ax.set_title('')

    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # 创建 Figures 文件夹路径
    figures_folder = os.path.join(os.getcwd(), 'Figures')
    os.makedirs(figures_folder, exist_ok=True)  # 如果文件夹不存在，创建文件夹

    # 构建图像文件的路径
    save_path = os.path.join(figures_folder, 'fwhm.png')

    # 保存图像到文件
    fig.savefig(save_path, bbox_inches='tight')
    plt.close(fig)  # 关闭图形，防止显示图形窗口

    return save_path

def processed_spectral(selected_x, selected_y, final_data):
    x = np.asarray([row[0] for row in final_data])
    y = np.asarray([row[1] for row in final_data])
    rawaxis = final_data[0][3]
    coord = np.column_stack((x, y))
    rawpeak = np.asarray([row[4] for row in final_data])

    proaxis = final_data[0][6]
    propeak = np.asarray([row[7] for row in final_data])
    fitpeak = np.asarray([row[8] for row in final_data])

    # 寻找同时具有 x, y 值的行的索引
    common_indices = [i for i, (val_x, val_y) in enumerate(coord) if val_x == selected_x and val_y == selected_y]

    if not common_indices:
        print(f"No data found for x={selected_x} and y={selected_y}")
        return

    row = common_indices[0]  # 加1是因为列的索引从1开始

    # 以 axis 为 x 轴，rawpeak，propeak 和 fitpeak 的第 row 行为 y 轴，画折线图
    # plt.plot(rawaxis, rawpeak[row], label='raw-data', color='blue')
    plt.plot(proaxis, propeak[row], label='processed data', color='orange')
    plt.plot(proaxis, fitpeak[row], label='best-fit model (Vogit)', color='green')

    # 添加图例
    plt.legend()

    # 保存图像到 Figures 文件夹下
    save_path = 'Figures/fit_result.png'
    plt.savefig(save_path)

    # 显示图像
    plt.close()

    return save_path

