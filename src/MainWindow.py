from PyQt6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QGraphicsScene,
    QMessageBox,
    QTableWidgetItem
)
import csv
from src.UI.Ui_RamanFWHM import Ui_RamanFWHM
import src.figures as figs
import src.dataprocess as dtp
import os
import numpy as np
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
        # 连接按钮和槽函数
        self.ui.Fileselectbutton.clicked.connect(self.select_file)
        self.ui.AxisList.currentItemChanged.connect(self.update_map)
        self.ui.XList.currentItemChanged.connect(self.update_spec)
        self.ui.YList.currentItemChanged.connect(self.update_spec)
        self.ui.XList.currentItemChanged.connect(self.update_map)
        self.ui.YList.currentItemChanged.connect(self.update_map)
        self.ui.XList.currentItemChanged.connect(self.update_fwhm)
        self.ui.YList.currentItemChanged.connect(self.update_fwhm)
        self.ui.Begin_Pro.clicked.connect(self.begin_processing)
        self.ui.progressBar.hide()
        self.ui.Button_Save.clicked.connect(self.save_fwhm_table)

    def clear_map(self):
        """清空地图显示"""
        self.ui.Rawmap.setScene(None)
        self.ui.Promap.setScene(None)

    def display_map(self, canvas, data, is_pro=False):
        """显示地图"""
        scene_map = QGraphicsScene(self)
        scene_map.addWidget(canvas)

        # 设置图形位置居中
        canvas.figure.subplots_adjust(left=0.14, right=0.93,
                                      top=0.95, bottom=0.15)

        if is_pro:
            self.ui.Promap.setScene(scene_map)
            self.ui.Promap.show()
        else:
            self.ui.Rawmap.setScene(scene_map)
            self.ui.Rawmap.show()

    def display_map_peak(self, current_peak, is_pro=False):
        """显示地图峰值"""
        map_label = self.ui.PromapPeak if is_pro else self.ui.RawmapPeak
        map_label.setText(
            f"<html><b><font style=\"font-weight:700; color:#ff0000; font-size:8pt;\">Current Peak:</font></b> "
            f"<span style=\"font-weight:700; font-size:8pt;\">{current_peak.text()}</span></html>"
        )

    # def update_peak_label(ui, selected_value, is_pro):
    #     label = ui.PromapPeak if is_pro else ui.RawmapPeak
    #     label.setText(
    #         f"<html><b><font style=\"font-weight:700; color:#ff0000; font-size:8pt;\">Current Peak:</font></b> "
    #         f"<span style=\"font-weight:700; font-size:8pt;\">{selected_value}</span></html>"
    #     )

    #     # 更新位置标签
    #     if is_pro:
    #         ui.ProXPosition.setText(f"X Position: {selected_x}")
    #         ui.ProYPosition.setText(f"Y Position: {selected_y}")
    #     else:
    #         ui.RawXPosition.setText(f"X Position: {selected_x}")
    #         ui.RawYPosition.setText(f"Y Position: {selected_y}")

    def begin_processing(self):
        """开始处理数据"""
        self.Choices = params.ProcessingOptions()
        self.Choices.set_from_ui(self.ui)

        if self.Choices.choice_crop and (not self.Choices.peak_min or not self.Choices.peak_max):
            QMessageBox.warning(self, 'Warning', 'Please input your wanted cropping peak min and max')
            return

        self.Rdata.RMprodata = dtp.preprocess(self.Choices, self.Rdata)
        (self.Rdata.fit_result,
         self.Rdata.fwhm,
         self.Rdata.fwhm_err) = dtp.fwhm_cal(self.Rdata, self.ui)

        self.update_map()
        self.update_spec()
        self.update_fwhm()
        # 更新表格
        self.update_fwhm_table()
        if self.Rdata.fit_result is not None:
            self.ui.Button_Save.setEnabled(True)

    def select_file(self):
        """选择文件"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")

        if file_path:
            self.Rdata = params.Ramandata()
            file_name = os.path.basename(file_path)
            loaded_data = dtp.data_load(file_path)

            self.init_raman_data(loaded_data, file_name)

            self.enable_processing_options()

            self.populate_list_items()
            self.select_default_items()

            self.clear_map()
            self.update_map()
            self.update_spec()

    def init_raman_data(self, loaded_data, file_name):
        """初始化 Raman 数据"""
        self.Rdata.RMrawdata = loaded_data['RMrawdata']
        self.Rdata.x = loaded_data['xreshape']
        self.Rdata.y = loaded_data['yreshape']
        self.Rdata.xlist = loaded_data['xlist']
        self.Rdata.ylist = loaded_data['ylist']
        self.ui.DataRowsCols.setText(
            f"data contains {len(self.Rdata.xlist)}(x)"
            f"*{len(self.Rdata.ylist)}(y)""points"
        )
        self.ui.SelectedFileBrowser.setText(f"Selected File: {file_name}")

    def enable_processing_options(self):
        """启用处理选项"""
        self.ui.CropOrNot.setEnabled(True)
        self.ui.Choice_Cosmic.setEnabled(True)
        self.ui.Choice_Normalization.setEnabled(True)
        self.ui.Choice_Denoise.setEnabled(True)
        self.ui.Choice_Baseline.setEnabled(True)
        self.ui.Begin_Pro.setEnabled(True)

    def populate_list_items(self):
        """填充列表项目"""
        self.populate_list(self.ui.AxisList,
                           self.Rdata.RMrawdata.spectral_axis)
        self.populate_list(self.ui.XList, self.Rdata.xlist)
        self.populate_list(self.ui.YList, self.Rdata.ylist)

    def populate_list(self, list_widget, values):
        """填充列表"""
        list_widget.clear()
        for value in values:
            list_widget.addItem(str(value))

    def select_default_items(self):
        """选择默认项目"""
        self.ui.AxisList.setCurrentRow(0)
        self.ui.XList.setCurrentRow(0)
        self.ui.YList.setCurrentRow(0)

    def update_map(self):
        """更新地图"""
        self.clear_map()

        current_peak = self.ui.AxisList.currentItem()
        current_item_x = self.ui.XList.currentItem()
        current_item_y = self.ui.YList.currentItem()

        if current_peak is None:
            print("No current peak selected.")
            return

        if current_item_x and current_item_y:
            self.display_map_peak(current_peak)
            self.display_map(
                FigureCanvas(figs.specmap(
                    float(current_peak.text()),
                    float(current_item_x.text()),
                    float(current_item_y.text()),
                    self.Rdata,
                    self.Rdata.RMrawdata,
                    self.ui
                )),
                self.Rdata.RMprodata
            )

            if self.Rdata.RMprodata is not None:
                self.display_map_peak(current_peak, is_pro=True)
                self.display_map(
                    FigureCanvas(figs.specmap(
                        float(current_peak.text()),
                        float(current_item_x.text()),
                        float(current_item_y.text()),
                        self.Rdata,
                        self.Rdata.RMprodata,
                        self.ui
                    )),
                    self.Rdata.RMprodata,
                    is_pro=True
                )

    def update_spec(self):
        """更新谱图"""
        self.ui.RawdataSpec.setScene(None)
        self.ui.ProdataSpec.setScene(None)

        current_item_x = self.ui.XList.currentItem()
        current_item_y = self.ui.YList.currentItem()

        if current_item_x and current_item_y:
            figraw, figpro = figs.raw_specplot(
                float(current_item_x.text()),
                float(current_item_y.text()),
                self.Rdata,
                self.ui
            ), figs.pro_specplot(
                float(current_item_x.text()),
                float(current_item_y.text()),
                self.Rdata,
                self.ui
            )

            if figraw is not None:
                # 显示 Raw Data 谱图
                canvas_raw = FigureCanvas(figraw)
                scene_raw = QGraphicsScene(self)
                scene_raw.addWidget(canvas_raw)

                figraw.subplots_adjust(left=0.12,
                                       right=0.93,
                                       top=0.92,
                                       bottom=0.15)

                self.ui.RawdataSpec.setScene(scene_raw)

            if figpro is not None:
                # 显示 Processed Data 和 Voigt Fit 谱图
                canvas_pro = FigureCanvas(figpro)
                scene_pro = QGraphicsScene(self)

                # 清空 ProdataSpec 中的图形
                scene_pro.clear()

                scene_pro.addWidget(canvas_pro)

                # 调整 ProdataSpec 图形的边缘
                figpro.subplots_adjust(left=0.12,
                                       right=0.93,
                                       top=0.92,
                                       bottom=0.15)

                self.ui.ProdataSpec.setScene(scene_pro)

    def update_fwhm(self):
        self.ui.FWHMmap.setScene(None)

        current_item_x = self.ui.XList.currentItem()
        current_item_y = self.ui.YList.currentItem()

        if self.Rdata.fit_result is None:
            print("No fit result available yet.")
            return

        if current_item_x and current_item_y:
            figfwhm = figs.fwhmmap(
                float(current_item_x.text()),
                float(current_item_y.text()),
                self.Rdata
            )

            canvas_fwhm = FigureCanvas(figfwhm)
            scene_fwhm = QGraphicsScene(self)
            scene_fwhm.addWidget(canvas_fwhm)

            # 调整 FWHMmap 图形的边缘
            figfwhm.subplots_adjust(left=0.12,
                                    right=0.93,
                                    top=0.92,
                                    bottom=0.15)

            self.ui.FWHMmap.setScene(scene_fwhm)

    def update_fwhm_table(self):
        # 清空表格
        self.ui.FWHMTable.clearContents()

        # 设置行数和列数
        rows = len(self.Rdata.ylist)
        cols = len(self.Rdata.xlist)
        self.ui.FWHMTable.setRowCount(rows * cols)
        self.ui.FWHMTable.setColumnCount(4)  # 一列序号(去除) + 四列数据

        # 设置表头
        # header = ["Index", "X", "Y", "FWHM", "FWHM Error"]
        # self.ui.FWHMTable.setHorizontalHeaderLabels(header)

        # 填充数据
        index = 0
        for i in range(rows):
            for j in range(cols):
                # 添加行序号
                # self.ui.FWHMTable.setItem(index, 0, QTableWidgetItem(str(index + 1)))

                # 添加 X、Y、FWHM、FWHM Error 数据
                self.ui.FWHMTable.setItem(index, 0, QTableWidgetItem(str(self.Rdata.x[i, j])))
                self.ui.FWHMTable.setItem(index, 1, QTableWidgetItem(str(self.Rdata.y[i, j])))
                self.ui.FWHMTable.setItem(index, 2, QTableWidgetItem(f'{np.around(self.Rdata.fwhm[i, j], decimals=6)}'))
                self.ui.FWHMTable.setItem(index, 3, QTableWidgetItem(f'{np.around(self.Rdata.fwhm_err[i, j], decimals=6)}'))

                index += 1

    def save_fwhm_table(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save FWHM Table", "", "CSV Files (*.csv)")

        if file_path:
            try:
                with open(file_path, 'w', newline='') as csvfile:
                    # Create a CSV writer object
                    csv_writer = csv.writer(csvfile)

                    # Write the header row
                    header = ["X", "Y", "FWHM", "FWHM Error"]
                    csv_writer.writerow(header)

                    # Write the data rows
                    for i in range(self.ui.FWHMTable.rowCount()):
                        row_data = []
                        for j in range(self.ui.FWHMTable.columnCount()):
                            item = self.ui.FWHMTable.item(i, j)
                            if item is not None:
                                row_data.append(item.text())
                            else:
                                row_data.append("")  # Handle empty cells

                        csv_writer.writerow(row_data)

                QMessageBox.information(self, 'Success', 'FWHM Table saved successfully!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'An error occurred: {str(e)}')
