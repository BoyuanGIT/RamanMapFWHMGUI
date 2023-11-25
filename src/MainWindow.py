from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QTableWidgetItem,
    QMessageBox  # 添加这一行
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from Ui_RamanFWHM import Ui_RamanFWHM
import src.functions as func
import src.dataprocess as dtp
import os
import src.parameters as params
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class FWHMWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RamanFWHM()
        self.Rdata = params.Ramandata()
        self.Choices = params.ProcessingOptions()
        self.ui.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        self.ui.Fileselectbutton.clicked.connect(self.select_file)
        self.ui.AxisList.currentItemChanged.connect(self.update_map)
        self.ui.XList.currentItemChanged.connect(self.update_rawspec)
        self.ui.YList.currentItemChanged.connect(self.update_rawspec)
        self.ui.Begin_Pro.clicked.connect(self.begin_processing)
        self.ui.progressBar.hide()

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        if file_path:
            # 用户选中文件时，初始化 self.Rdata
            self.Rdata = params.Ramandata()


            file_name = os.path.basename(file_path)
            loaded_data = dtp.data_load(file_path)
            self.Rdata.RMrawdata = loaded_data['RMrawdata']  # rpy格式原始数据
            self.Rdata.x = loaded_data['xreshape']  # 符合数据形状的x
            self.Rdata.y = loaded_data['yreshape']  # 符合数据形状的y
            self.Rdata.xlist = loaded_data['xlist']  # 唯一值x列表
            self.Rdata.ylist = loaded_data['ylist']  # 唯一值y列表
            self.ui.DataRowsCols.setText(
                f"data contains {len(self.Rdata.xlist)}(x)\n"
                f"*{len(self.Rdata.ylist)}(y)\n""points"
            )
            self.ui.SelectedFileBrowser.setText(f"Selected File: {file_name}")

            # enable所有处理选项
            self.ui.CropOrNot.setEnabled(True)
            self.ui.Choice_Cosmic.setEnabled(True)
            self.ui.Choice_Normalization.setEnabled(True)
            self.ui.Choice_Denoise.setEnabled(True)
            self.ui.Choice_Baseline.setEnabled(True)
            self.ui.Begin_Pro.setEnabled(True)

            # 清空 AxisList、XList、YList 中的所有项目
            self.ui.AxisList.clear()
            self.ui.XList.clear()
            self.ui.YList.clear()

            for value in self.Rdata.RMrawdata.spectral_axis:
                # 添加项目
                self.ui.AxisList.addItem(str(value))

            for value in self.Rdata.xlist:
                # 添加项目
                self.ui.XList.addItem(str(value))

            for value in self.Rdata.ylist:
                # 添加项目
                self.ui.YList.addItem(str(value))

            # 默认选择第一个值
            self.ui.AxisList.setCurrentRow(0)
            self.ui.XList.setCurrentRow(0)
            self.ui.YList.setCurrentRow(0)
            # 清空 Rawmap 中的内容
            self.ui.Rawmap.setScene(None)
            self.ui.RawdataSpec.setScene(None)

            self.update_map()
            self.update_rawspec()

    def update_map(self):
        # 清空 Rawmap 中的内容
        self.ui.Rawmap.setScene(None)
        self.ui.Promap.setScene(None)  # 清空 Promap 中的内容

        # 获取当前选中的 XList 项目
        current_peak = self.ui.AxisList.currentItem()

        if current_peak is None:
            # 在这里处理 currentItem 为 None 的情况
            print("No current peak selected.")
            return

        # 显示 Rawmap
        self.canvas_rawmap = FigureCanvas(
            func.specmap(
                float(current_peak.text()),
                self.Rdata,
                self.Rdata.RMrawdata
            )
        )
        scene_rawmap = QGraphicsScene(self)
        scene_rawmap.addWidget(self.canvas_rawmap)

        # 设置图形位置居中
        self.canvas_rawmap.figure.subplots_adjust(
            left=0.14, right=0.93, top=0.95, bottom=0.15
        )

        self.ui.Rawmap.setScene(scene_rawmap)
        self.ui.Rawmap.show()

        # 设置 RawmapPeak 标签的文本
        self.ui.RawmapPeak.setText(
            f"<html><b><font style=\"font-weight:700; color:#ff0000; font-size:8pt;\">Current Peak:</font></b> "
            f"<span style=\"font-weight:700; font-size:8pt;\">{self.ui.AxisList.currentItem().text()}</span></html>"
        )

        if self.Rdata.RMprodata is not None:
            # 如果 Rdata.RMprodata 不为空，更新 Promap
            self.canvas_promap = FigureCanvas(
                func.specmap(
                    float(current_peak.text()),
                    self.Rdata,
                    self.Rdata.RMprodata
                )
            )
            scene_promap = QGraphicsScene(self)
            scene_promap.addWidget(self.canvas_promap)

            # 设置图形位置居中
            self.canvas_promap.figure.subplots_adjust(
                left=0.14, right=0.93, top=0.95, bottom=0.15
            )

            self.ui.Promap.setScene(scene_promap)
            self.ui.Promap.show()

            # 设置 PromapPeak 标签的文本
            self.ui.PromapPeak.setText(
                f"<html><b><font style=\"font-weight:700; color:#ff0000; font-size:8pt;\">Current Peak:</font></b> "
                f"<span style=\"font-weight:700; font-size:8pt;\">{self.ui.AxisList.currentItem().text()}</span></html>"
            )

    def update_rawspec(self):
        # 清空 RawdataSpec 中的内容
        self.ui.RawdataSpec.setScene(None)

        # 获取当前选中的 XList 项目
        current_item_x = self.ui.XList.currentItem()
        current_item_y = self.ui.YList.currentItem()

        if current_item_x and current_item_y:
            # 显示Rawspec
            self.canvas_rawspec = FigureCanvas(
                func.specplot(
                    float(current_item_x.text()),
                    float(current_item_y.text()),
                    self.Rdata,
                    self.Rdata.RMrawdata
                )
            )
            scene_rawspec = QGraphicsScene(self)
            scene_rawspec.addWidget(self.canvas_rawspec)
            self.ui.RawdataSpec.setScene(scene_rawspec)
            self.ui.RawdataSpec.show()

            # 设置 RawXYPosition 标签的文本
            self.ui.RawXPosition.setText(
                f"<html><head/><body>"
                f"<span style=\"font-weight:700; color:#ff0000;\">Current X: </span>"
                f"<span style=\"font-weight:700; color:#000000;\">{current_item_x.text()}</span>"
                f"</body></html>"
            )

            self.ui.RawYPosition.setText(
                f"<html><head/><body>"
                f"<span style=\"font-weight:700; color:#ff0000;\">Current Y: </span>"
                f"<span style=\"font-weight:700; color:#000000;\">{current_item_y.text()}</span>"
                f"</body></html>"
            )

    def begin_processing(self):
        # 获取用户选择的参数
        options = params.ProcessingOptions()
        options.set_from_ui(self.ui)

        # 检查用户选择了 CropOrNot 时是否输入了 Cropmin 和 Cropmax
        if options.choice_crop and (not options.peak_min or not options.peak_max):
            QMessageBox.warning(self, 'Warning',
                                'Please input your wanted cropping peak min and max')
            return  # 如果没有输入 Cropmin 和 Cropmax，则停止处理
        
        self.ui.progressBar.show()

        # 调用 dataprocess.py 中的 preprocess 函数对数据进行预处理
        self.Rdata.RMprodata = dtp.preprocess(options, self.Rdata)
        self.Rdata.fit_result = dtp.fwhm_cal(self.Rdata)

        # 显示处理后的map
        self.update_map()
        self.update_prospec()

    def update_prospec(self):
        # 清空 ProdataSpec 中的内容
        self.ui.ProdataSpec.setScene(None)

        # 获取当前选中的 XList 项目
        current_item_x = self.ui.XList.currentItem()
        current_item_y = self.ui.YList.currentItem()

        if current_item_x and current_item_y:
            # 显示ProdataSpec
            self.canvas_prospec = FigureCanvas(
                func.specplot(
                    float(current_item_x.text()),
                    float(current_item_y.text()),
                    self.Rdata,
                    self.Rdata.RMprodata
                )
            )
            scene_prospec = QGraphicsScene(self)
            scene_prospec.addWidget(self.canvas_prospec)
            self.ui.RawdataSpec.setScene(scene_prospec)
            self.ui.RawdataSpec.show()

            # 设置 ProXPosition 标签的文本
            self.ui.ProXPosition.setText(
                f"<html><head/><body>"
                f"<span style=\"font-weight:700; color:#ff0000;\">Current X: </span>"
                f"<span style=\"font-weight:700; color:#000000;\">{current_item_x.text()}</span>"
                f"</body></html>"
            )

            self.ui.ProYPosition.setText(
                f"<html><head/><body>"
                f"<span style=\"font-weight:700; color:#ff0000;\">Current Y: </span>"
                f"<span style=\"font-weight:700; color:#000000;\">{current_item_y.text()}</span>"
                f"</body></html>"
            )
