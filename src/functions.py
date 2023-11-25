import pandas as pd
import numpy as np
import ramanspy as rpy
from lmfit.models import VoigtModel
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os


def rawdata_heatmap(selected_value, Rdata):
    # 创建热图
    fig, ax = plt.subplots()
    im = ax.imshow(
        Rdata.RMrawdata.band(selected_value).astype(float), cmap='YlOrRd',
        aspect='auto',
        extent=[min(Rdata.xlist), max(Rdata.xlist),
                min(Rdata.ylist), max(Rdata.ylist)]
    )

    # 设置 colorbar 标签
    cbar = fig.colorbar(im, ax=ax, label='Intensity')

    # 将colorbar标签放到左侧，整体左移0.5个单位距离
    cbar.ax.yaxis.set_label_coords(-1, 0.5)

    # 隐藏图形标题
    ax.set_title('')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    return fig


def rawdata_spectral(selected_x, selected_y, Rdata):
    # 寻找选择的点在数据中的位置
    print(Rdata.x)
    print(Rdata.y)
    index = np.where((Rdata.x == selected_x) &
                     (Rdata.y == selected_y))

    if not index[0].size or not index[1].size:
        print(f"No data found for x={selected_x} and y={selected_y}")
        return

    # 创建折线图
    fig, ax = plt.subplots()
    ax.plot(Rdata.RMrawdata[index[0][0], index[1][0]].spectral_axis,
            Rdata.RMrawdata[index[0][0], index[1][0]].spectral_data,
            label='')
    ax.legend()

    return fig


def pipline_choice(
        choice_crop,
        peak_min,
        peak_max,
        choice_cosmic,
        choice_baseline,
        choice_norm,
        choice_denoise):
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
    if not any(
        [choice_crop,
         choice_cosmic,
         choice_baseline,
         choice_norm,
         choice_denoise]):
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

