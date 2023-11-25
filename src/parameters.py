# 储存了所有需要调用的参数

# parameters.py
class Ramandata:
    def __init__(self):
        self.x = None
        self.y = None
        self.axis = None
        self.rawdata = None  # 原始表格数据所有
        self.RMrawdata = None  # 原始数据rpy加载
        self.RMprodata = None  # 处理完数据rpy加载


class ProcessingOptions:
    def __init__(self):
        self.choice_crop = False
        self.choice_cosmic = False
        self.choice_baseline = False
        self.choice_norm = False
        self.choice_denoise = False
        self.peak_min = 0
        self.peak_max = 100
        # ... 其他处理选项
