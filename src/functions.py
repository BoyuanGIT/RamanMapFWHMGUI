import pandas as pd
import numpy as np
import ramanspy as rpy
from lmfit.models import VoigtModel
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os


# 返回选择的拉曼峰值所对应的二维热图map
def specmap(selected_value, Rdata, RMdata):
    # 创建热图
    fig, ax = plt.subplots()
    im = ax.imshow(
        RMdata.band(selected_value).astype(float), cmap='YlOrRd',
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


# 定义函数rawdata_spectral，用于显示选择的点的光谱图像
def specplot(selected_x, selected_y, Rdata, RMdata):
    # 寻找选择的点在数据中的位置
    index = np.where((Rdata.x == selected_x) &
                     (Rdata.y == selected_y))

    if not index[0].size or not index[1].size:
        print(f"No data found for x={selected_x} and y={selected_y}")
        return

    # 创建折线图
    fig, ax = plt.subplots()
    ax.plot(RMdata[index[0][0], index[1][0]].spectral_axis,
            RMdata[index[0][0], index[1][0]].spectral_data,
            label='')
    ax.legend()

    return fig


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
