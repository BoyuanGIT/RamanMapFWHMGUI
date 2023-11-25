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
        self.ui.AxisList.currentItemChanged.connect(self.update_rawmap)
        self.ui.XList.currentItemChanged.connect(self.update_rawspec)
        self.ui.YList.currentItemChanged.connect(self.update_rawspec)
        self.ui.Begin_Pro.clicked.connect(self.begin_processing)
        self.ui.XList_2.currentItemChanged.connect(self.begin_processing)
        self.ui.YList_2.currentItemChanged.connect(self.begin_processing)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        if file_path:
            file_name = os.path.basename(file_path)
            loaded_data = dtp.data_load(file_path)
            self.Rdata.RMrawdata = loaded_data['RMrawdata']  # rpy格式原始数据
            self.Rdata.x = loaded_data['xreshape']  # 符合数据形状的x
            self.Rdata.y = loaded_data['yreshape']  # 符合数据形状的y
            self.Rdata.xlist = loaded_data['xlist']  # 唯一值x列表
            self.Rdata.ylist = loaded_data['ylist']  # 唯一值y列表
            self.ui.DataRowsCols.setText(
                f"data contains {len(self.Rdata.xlist)}(x)*{len(self.Rdata.ylist)}(y) points"
            )
            self.ui.SelectedFileBrowser.setText(f"Selected File: {file_name}")

            # 清空 AxisList、XList、YList 中的所有项目
            self.ui.AxisList.clear()
            self.ui.XList.clear()
            self.ui.XList_2.clear()
            self.ui.YList.clear()
            self.ui.YList_2.clear()

            for value in self.Rdata.RMrawdata.spectral_axis:
                # 添加项目
                self.ui.AxisList.addItem(str(value))

            for value in self.Rdata.xlist:
                # 添加项目
                self.ui.XList.addItem(str(value))
                self.ui.XList_2.addItem(str(value))

            for value in self.Rdata.ylist:
                # 添加项目
                self.ui.YList.addItem(str(value))
                self.ui.YList_2.addItem(str(value))

            # 默认选择第一个值
            self.ui.AxisList.setCurrentRow(0)
            self.ui.XList.setCurrentRow(0)
            self.ui.YList.setCurrentRow(0)
            # 清空 Rawmap 中的内容
            self.ui.Rawmap.setScene(None)
            self.ui.RawdataSpec.setScene(None)

            self.update_rawmap()
            self.update_rawspec()

    def update_rawmap(self):
        # 清空 Rawmap 中的内容
        self.ui.Rawmap.setScene(None)

        # 显示Rawmap
        self.canvas_rawmap = FigureCanvas(
            func.rawdata_heatmap(
                float(self.ui.AxisList.currentItem().text()),
                self.Rdata
            )
        )
        scene_rawmap = QGraphicsScene(self)
        scene_rawmap.addWidget(self.canvas_rawmap)

        self.ui.Rawmap.setScene(scene_rawmap)
        self.ui.Rawmap.show()

        # 设置 RawmapPeak 标签的文本
        self.ui.RawmapPeak.setText(
            f"<html><b><font color='red'>Current Peak:</font></b> {self.ui.AxisList.currentItem()}</html>"
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
                func.rawdata_spectral(
                    float(current_item_x.text()),
                    float(current_item_y.text()),
                    self.Rdata
                )
            )
            scene_rawspec = QGraphicsScene(self)
            scene_rawspec.addWidget(self.canvas_rawspec)
            self.ui.RawdataSpec.setScene(scene_rawspec)
            self.ui.RawdataSpec.show()

            # 设置 RawXYPosition 标签的文本
            self.ui.RawXYPosition.setText(
                f"<html><head/><body><p><span style=\" font-weight:700; color:#ff0000;\">Current X: </span><span style=\" font-weight:700; color:#000000;\">{current_item_x.text()}</span></p><p><span style=\" font-weight:700; color:#ff0000;\">Current Y: </span><span style=\" font-weight:700; color:#000000;\">{current_item_y.text()}</span></p></body></html>"
            )

    def begin_processing(self):
        # 获取用户选择的参数
        choice_crop = self.ui.CropOrNot.isChecked()
        choice_cosmic = self.ui.Choice_Cosmic.isChecked()
        choice_baseline = self.ui.Choice_Baseline.isChecked()
        choice_norm = self.ui.Choice_Normalization.isChecked()
        choice_denoise = self.ui.Choice_Denoise.isChecked()

        # 获取用户输入的 Cropmin 和 Cropmax
        peak_min = self.ui.Cropmin.toPlainText()
        peak_max = self.ui.Cropmax.toPlainText()

        # 检查用户选择了 CropOrNot 时是否输入了 Cropmin 和 Cropmax
        if choice_crop and (not peak_min or not peak_max):
            QMessageBox.warning(self, 'Warning', 'Please input your wanted cropping peak min and max')
            return  # 如果没有输入 Cropmin 和 Cropmax，则停止处理

        # 调用 functions.py 中的 pipline_choice 函数
        pipe = pipline_choice(choice_crop, peak_min, peak_max, choice_cosmic, choice_baseline, choice_norm, choice_denoise)
        
        # 运行 Pipeline
        if pipe is None:
            QMessageBox.warning(self, 'Warning', 'No method was selected')
            return  # 如果没有选择任何方法，则停止处理
        
        self.processed_data = data_process(self.rawdata, pipe)

        # 把处理好的数据分门别类打包成各参数以便后续画图参数调用

        self.processed_x = np.asarray([row[0] for row in self.processed_data])
        self.processed_y = np.asarray([row[1] for row in self.processed_data])
        self.rawaxis = self.processed_data[0][3]
        self.processed_coord = np.column_stack((self.processed_x, self.processed_y))
        self.rawpeak = np.asarray([row[4] for row in self.processed_data])

        self.proaxis = self.processed_data[0][6]
        self.propeak = np.asarray([row[7] for row in self.processed_data])
        self.fitpeak = np.asarray([row[8] for row in self.processed_data])

        # 获取 Figures 文件夹的路径
        figures_folder = os.path.join(os.getcwd(), 'Figures')

        # 在 Figures 文件夹中创建 processed 文件夹
        processed_folder = os.path.join(figures_folder, 'processed')
        os.makedirs(processed_folder, exist_ok=True)

        # 将 processed_data 传入 fwhm_heatmap 函数
        fwhm_image_path = fwhm_heatmap(self.processed_data)

        # 显示 fwhm 图像在 ProMap QGraphicsView 中
        fwhm_image = QImage(fwhm_image_path)
        fwhm_pixmap = QPixmap.fromImage(fwhm_image)
        fwhm_item = QGraphicsPixmapItem(fwhm_pixmap)
        fwhm_scene = QGraphicsScene(self)
        fwhm_scene.addItem(fwhm_item)
        self.ui.ProMap.setScene(fwhm_scene)
        self.ui.ProMap.show()

        # 获取用户选择的 X 和 Y 值
        x_item = self.ui.XList_2.currentItem()
        y_item = self.ui.YList_2.currentItem()

        if x_item is None or y_item is None:
            # 如果用户没有选择 X 和 Y 值，默认选择 XList_2 和 YList_2 中的第一个值
            x_item = self.ui.XList_2.item(0)
            y_item = self.ui.YList_2.item(0)

        # 获取选定的 X 和 Y 值
        selected_x = float(x_item.text())
        selected_y = float(y_item.text())

        # 将选定的 X 和 Y 值传入 processed_spectral 函数
        spectral_image_path = processed_spectral(selected_x, selected_y, self.processed_coord, self.rawaxis, self.proaxis, self.propeak, self.fitpeak)

        # 显示 processed_spectral 图像在 ProSpectral QGraphicsView 中
        spectral_image = QImage(spectral_image_path)
        spectral_pixmap = QPixmap.fromImage(spectral_image)
        spectral_item = QGraphicsPixmapItem(spectral_pixmap)
        spectral_scene = QGraphicsScene(self)
        spectral_scene.addItem(spectral_item)
        self.ui.ProSpectral.setScene(spectral_scene)
        self.ui.ProSpectral.show()
