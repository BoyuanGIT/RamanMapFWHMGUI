import numpy as np
import matplotlib.pyplot as plt


def update_peak_label(ui, selected_value, is_pro):
    label = ui.PromapPeak if is_pro else ui.RawmapPeak
    label.setText(
        f"<html><b>"
        f"<font style=\"font-weight:700; color:#ff0000; font-size:8pt;\">Current Peak:</font></b> "
        f"<span style=\"font-weight:700; font-size:8pt;\">{selected_value}</span></html>"
    )


def specmap(selected_value, selected_x, selected_y, Rdata, RMdata, ui):
    is_pro = None

    min_spectral_axis = round(np.min(RMdata.spectral_axis), 1)
    max_spectral_axis = round(np.max(RMdata.spectral_axis), 1)

    if selected_value < np.min(RMdata.spectral_axis):
        selected_value = np.min(RMdata.spectral_axis)
        ui.Croplabel.setText(f'Please select peak between {min_spectral_axis} and {max_spectral_axis}')
        ui.Croplabel.setStyleSheet('color: red; font-size: 10pt; font-weight: bold')
        ui.Croplabel.show()
        is_pro = True
    elif selected_value > np.max(RMdata.spectral_axis):
        selected_value = np.max(RMdata.spectral_axis)
        ui.Croplabel.setText(f'Please select peak between {min_spectral_axis} and {max_spectral_axis}')
        ui.Croplabel.setStyleSheet('color: red; font-size: 10pt; font-weight: bold')
        ui.Croplabel.show()
        is_pro = True
    else:
        ui.Croplabel.hide()
        is_pro = False

    update_peak_label(ui, selected_value, is_pro)

    plt.close()

    # 创建热图
    fig, ax = plt.subplots()
    im = ax.imshow(
        RMdata.band(selected_value).astype(float), cmap='YlOrRd',
        aspect='auto',
        extent=[0, len(Rdata.xlist),
                len(Rdata.ylist), 0]
    )

    # 设置 colorbar 标签
    cbar = fig.colorbar(im, ax=ax, label='Intensity')

    # 将colorbar标签放到左侧，整体左移0.5个单位距离
    cbar.ax.yaxis.set_label_coords(-1, 0.5)

    # 隐藏图形标题
    ax.set_title('')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    index = np.where((Rdata.x == selected_x) &
                     (Rdata.y == selected_y))

    # 设置X轴ticks在每行的中间线上
    xticks_positions = np.arange(0.5, len(Rdata.xlist)+0.5, 1)
    xticks = np.arange(1, len(Rdata.xlist)+1, 1)
    plt.xticks(xticks_positions, xticks)

    # 设置Y轴ticks在每行的中间线上
    yticks_positions = np.arange(0.5, len(Rdata.ylist)+0.5, 1)
    yticks = np.arange(1, len(Rdata.ylist)+1, 1)
    plt.yticks(yticks_positions, yticks)

    # 在选定的X轴位置上画一条绿色加粗虚线
    ax.axvline(index[1][0] + 0.5, color='green', linestyle='--', linewidth=2)

    # 在选定的Y轴位置上画一条绿色加粗虚线
    ax.axhline(index[0][0] + 0.5, color='green', linestyle='--', linewidth=2)

    n = 5  # 调整n以达到你想要的刻度密度
    plt.locator_params(axis='x', nbins=len(xticks) // n + 1)
    plt.locator_params(axis='y', nbins=len(yticks) // n + 1)

    return fig


def raw_specplot(selected_x, selected_y, Rdata, ui):
    """显示 Raw Data 谱图"""
    index = np.where((Rdata.x == selected_x) & (Rdata.y == selected_y))

    if not index[0].size or not index[1].size:
        print(f"No data found for x={selected_x} and y={selected_y}")
        return None

    plt.close()

    figraw, axraw = plt.subplots()
    axraw.plot(
        Rdata.RMrawdata[index[0][0], index[1][0]].spectral_axis,
        Rdata.RMrawdata[index[0][0], index[1][0]].spectral_data,
        label='Raw Data',
        color='purple'
    )
    axraw.legend()
    axraw.set_xlabel('Peak')
    axraw.set_ylabel('Intensity')
    ui.RawXPosition.setText(
        f"<html><head/><body>"
        f"<span style=\"font-weight:700; color:#ff0000; font-size:9pt;\">"
        f"Current X: "
        f"</span>"
        f"<span style=\"font-size:9pt;\">{selected_x}</span>"
        f"</body></html>"
    )
    ui.RawYPosition.setText(
        f"<html><head/><body>"
        f"<span style=\"font-weight:700; color:#ff0000; font-size:9pt;\">"
        f"Current X: "
        f"</span>"
        f"<span style=\"font-size:9pt;\">{selected_y}</span>"
        f"</body></html>"
    )

    return figraw


def pro_specplot(selected_x, selected_y, Rdata, ui):
    """显示 Processed Data 和 Voigt Fit 谱图"""
    if Rdata.RMprodata is None:
        return None

    index = np.where((Rdata.x == selected_x) & (Rdata.y == selected_y))

    if not index[0].size or not index[1].size:
        print(f"No data found for x={selected_x} and y={selected_y}")
        return None

    plt.close()

    figpro, axpro = plt.subplots()

    # 绘制折线并设置颜色和标签
    # yrow = Rdata.RMrawdata[index[0][0], index[1][0]].spectral_data
    ypro = Rdata.RMprodata[index[0][0], index[1][0]].spectral_data
    # xrow = Rdata.RMrawdata[index[0][0], index[1][0]].spectral_axis
    xpro = Rdata.RMprodata[index[0][0], index[1][0]].spectral_axis

    # axpro.plot(xrow, yrow, label='Raw Data', color='purple', alpha=0.7)
    axpro.plot(xpro, ypro, label='Processed Data', color='blue', alpha=0.7)
    axpro.plot(
        xpro,
        Rdata.fit_result[index[0][0]][index[1][0]].best_fit,
        label='Voigt Fit',
        color='red',
        alpha=0.7
    )

    # 显示图例
    axpro.legend()

    # 添加标题和标签
    axpro.set_xlabel('Peak')
    axpro.set_ylabel('Intensity')

    ui.ProXPosition.setText(
        f"<html><head/><body>"
        f"<span style=\"font-weight:700; color:#ff0000; font-size:9pt;\">"
        f"Current X: "
        f"</span>"
        f"<span style=\"font-size:9pt;\">{selected_x}</span>"
        f"</body></html>"
    )
    ui.ProYPosition.setText(
        f"<html><head/><body>"
        f"<span style=\"font-weight:700; color:#ff0000; font-size:9pt;\">"
        f"Current X: "
        f"</span>"
        f"<span style=\"font-size:9pt;\">{selected_y}</span>"
        f"</body></html>"
    )

    return figpro


def fwhmmap(selected_x, selected_y, Rdata):


    fwhm_values = [[fitresult.params['fwhm'].value for fitresult in row] for row in Rdata.fit_result]
    fwhm_array = np.array(fwhm_values)

    plt.close()

    fig, ax = plt.subplots()
    im = ax.imshow(
        fwhm_array, cmap='YlOrRd',
        aspect='auto',
        extent=[0, len(Rdata.xlist),
                len(Rdata.ylist), 0]
    )

    # 设置 colorbar 标签
    cbar = fig.colorbar(im, ax=ax, label='Intensity')

    # 将colorbar标签放到左侧，整体左移0.5个单位距离
    cbar.ax.yaxis.set_label_coords(-1, 0.5)

    # 隐藏图形标题
    ax.set_title('')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    index = np.where((Rdata.x == selected_x) &
                     (Rdata.y == selected_y))

    # 设置X轴ticks在每行的中间线上
    xticks_positions = np.arange(0.5, len(Rdata.xlist)+0.5, 1)
    xticks = np.arange(1, len(Rdata.xlist)+1, 1)
    plt.xticks(xticks_positions, xticks)

    # 设置Y轴ticks在每行的中间线上
    yticks_positions = np.arange(0.5, len(Rdata.ylist)+0.5, 1)
    yticks = np.arange(1, len(Rdata.ylist)+1, 1)
    plt.yticks(yticks_positions, yticks)

    # 在选定的X轴位置上画一条绿色加粗虚线
    ax.axvline(index[1][0] + 0.5, color='green', linestyle='--', linewidth=2)

    # 在选定的Y轴位置上画一条绿色加粗虚线
    ax.axhline(index[0][0] + 0.5, color='green', linestyle='--', linewidth=2)

    n = 5  # 调整n以达到你想要的刻度密度
    plt.locator_params(axis='x', nbins=len(xticks) // n + 1)
    plt.locator_params(axis='y', nbins=len(yticks) // n + 1)

    return fig
