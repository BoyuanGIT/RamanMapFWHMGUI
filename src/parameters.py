# 储存了所有需要调用的参数

# parameters.py
class Ramandata:
    def __init__(self):
        self.x = None
        self.y = None
        self.axis = None
        self.data = None
        self.xnum = None
        self.ynum = None
        self.user_id = 0


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

# 创建全局参数对象


rdata = Ramandata()
pipe_options = ProcessingOptions()
