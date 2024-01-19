import pandas as pd
import numpy as np
import ramanspy as rpy
from lmfit.models import VoigtModel


# 传入文件路径，处理数据，返回xy列表，xy不重复列表，rpy的image contanier


def data_load(filename):
    try:
        # 尝试从文件中读取数据
        rawdata = pd.read_csv(filename, header=None).to_numpy()

        # 处理数据
        axis = rawdata[3:, 0].astype(float)
        spectral_data = rawdata[3:, 1:].astype(float)
        x = rawdata[1, 1:].astype(float)
        y = rawdata[2, 1:].astype(float)
        xlist = np.unique(x)
        ylist = np.unique(y)
        xreshape = x.reshape(len(ylist), len(xlist))
        yreshape = y.reshape(len(ylist), len(xlist))
        RMrawdata = rpy.SpectralContainer(
             spectral_data.T.reshape(len(ylist), len(xlist), len(axis)),
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


def preprocess(options, Rdata):
    # 初始化 Pipeline
    pipe = rpy.preprocessing.Pipeline([])

    if options.choice_crop:
        # 如果选择了 Crop，则获取用户输入的波数范围，并添加 Cropper 到 Pipeline
        wavenumber = (float(options.peak_min), float(options.peak_max))
        pipe.append(rpy.preprocessing.misc.Cropper(region=wavenumber))

    if options.choice_cosmic:
        # 如果选择了 Cosmic，则添加 WhitakerHayes 到 Pipeline
        pipe.append(rpy.preprocessing.despike.WhitakerHayes())

    if options.choice_baseline:
        # 如果选择了 Baseline，则添加 ASLS 到 Pipeline
        pipe.append(rpy.preprocessing.baseline.ASLS())

    if options.choice_norm:
        # 如果选择了 Normalization，则添加 MaxIntensity 到 Pipeline
        pipe.append(rpy.preprocessing.normalise.MaxIntensity())

    if options.choice_denoise:
        # 如果选择了 Denoise，则添加 Gaussian 到 Pipeline
        pipe.append(rpy.preprocessing.denoise.Gaussian())

    # 如果没有选择任何一个框，返回空值

    if not any([
        options.choice_crop,
        options.choice_cosmic,
        options.choice_baseline,
        options.choice_norm,
        options.choice_denoise
    ]):
        return Rdata.RMrawdata

    return pipe.apply(Rdata.RMrawdata)


def fwhm_cal(Rdata, ui):
    rmdata = Rdata.RMprodata
    tobefitdata = np.zeros((len(Rdata.ylist), len(Rdata.xlist)),
                           dtype=object)
    tobefitaxis = np.zeros((len(Rdata.ylist), len(Rdata.xlist)),
                           dtype=object)
    for i in range(len(Rdata.ylist)):
        for j in range(len(Rdata.xlist)):
            tobefitdata[i, j] = rmdata.spectral_data[i, j, :]
            tobefitaxis[i, j] = rmdata.spectral_axis

    total_steps = len(Rdata.ylist) * len(Rdata.xlist)
    current_step = 0

    model = VoigtModel()
    params = model.make_params(amplitude=1, center=0, sigma=1, gamma=1)

    fitresult_list = []  # 使用列表存储拟合结果

    ui.progressBar.show()

    for i in range(len(Rdata.ylist)):
        row_results = []  # 存储一行的拟合结果
        for j in range(len(Rdata.xlist)):
            fitresult = model.fit(tobefitdata[i, j],
                                  params,
                                  x=tobefitaxis[i, j])
            row_results.append(fitresult)
            current_step += 1
            progress_percentage = int((current_step / total_steps) * 100)
            ui.progressBar.setValue(progress_percentage)
        fitresult_list.append(row_results)
        current_step += 1
        progress_percentage = int((current_step / total_steps) * 100)
        ui.progressBar.setValue(progress_percentage)

    ui.progressBar.hide()

    fwhm_values = [[fitresult.params['fwhm'].value for fitresult in row] for row in fitresult_list]
    fwhm_array = np.array(fwhm_values)
    fwhm_err = [[fitresult.params['fwhm'].stderr for fitresult in row] for row in fitresult_list]
    fwhm_err_array = np.array(fwhm_err)

    return fitresult_list, fwhm_array, fwhm_err_array
