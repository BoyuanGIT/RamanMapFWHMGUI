# 储存了所有需要调用的参数

# parameters.py
class Ramandata:
    def __init__(self):
        self.x = None
        self.y = None
        self.xlist = None
        self.ylist = None
        self.axis = None
        self.rawdata = None  # 原始表格数据所有
        self.RMrawdata = None  # 原始数据rpy加载
        self.RMprodata = None  # 处理完数据rpy加载
        self.fit_result = None


class ProcessingOptions:
    def __init__(self):
        self.choice_crop = False
        self.choice_cosmic = False
        self.choice_baseline = False
        self.choice_norm = False
        self.choice_denoise = False
        self.peak_min = None
        self.peak_max = None

    def set_from_ui(self, ui):
        self.choice_crop = ui.CropOrNot.isChecked()
        self.choice_cosmic = ui.Choice_Cosmic.isChecked()
        self.choice_baseline = ui.Choice_Baseline.isChecked()
        self.choice_norm = ui.Choice_Normalization.isChecked()
        self.choice_denoise = ui.Choice_Denoise.isChecked()
        self.peak_min = ui.Cropmin.toPlainText()
        self.peak_max = ui.Cropmax.toPlainText()
