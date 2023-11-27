# Created by: PyQt6 UI code generator 6.4.2
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_RamanFWHM(object):
    def setupUi(self, RamanFWHM):
        RamanFWHM.setObjectName("RamanFWHM")
        RamanFWHM.resize(1920, 1024)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RamanFWHM.sizePolicy().hasHeightForWidth())
        RamanFWHM.setSizePolicy(sizePolicy)
        RamanFWHM.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(parent=RamanFWHM)
        self.centralwidget.setObjectName("centralwidget")
        self.Fileselectbutton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Fileselectbutton.setGeometry(QtCore.QRect(100, 10, 101, 31))
        self.Fileselectbutton.setObjectName("Fileselectbutton")
        self.SelectedFileBrowser = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.SelectedFileBrowser.setGeometry(QtCore.QRect(210, 10, 321, 31))
        self.SelectedFileBrowser.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.SelectedFileBrowser.setObjectName("SelectedFileBrowser")
        self.Rawmap = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.Rawmap.setGeometry(QtCore.QRect(110, 50, 601, 471))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Rawmap.sizePolicy().hasHeightForWidth())
        self.Rawmap.setSizePolicy(sizePolicy)
        self.Rawmap.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Rawmap.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Rawmap.setObjectName("Rawmap")
        self.RawmapLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.RawmapLabel.setGeometry(QtCore.QRect(360, 50, 111, 16))
        self.RawmapLabel.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.RawmapLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RawmapLabel.setObjectName("RawmapLabel")
        self.AxisList = QtWidgets.QListWidget(parent=self.centralwidget)
        self.AxisList.setGeometry(QtCore.QRect(10, 60, 91, 461))
        self.AxisList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.AxisList.setAlternatingRowColors(False)
        self.AxisList.setModelColumn(0)
        self.AxisList.setObjectName("AxisList")
        self.DataRowsCols = QtWidgets.QTextBrowser(parent=self.centralwidget)
        self.DataRowsCols.setGeometry(QtCore.QRect(540, 10, 341, 31))
        self.DataRowsCols.setObjectName("DataRowsCols")
        self.PeakposLable = QtWidgets.QLabel(parent=self.centralwidget)
        self.PeakposLable.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.PeakposLable.setObjectName("PeakposLable")
        self.ProdataSpec = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.ProdataSpec.setGeometry(QtCore.QRect(715, 530, 601, 461))
        self.ProdataSpec.setMaximumSize(QtCore.QSize(601, 471))
        self.ProdataSpec.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ProdataSpec.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ProdataSpec.setObjectName("ProdataSpec")
        self.RawSpectralLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.RawSpectralLabel.setGeometry(QtCore.QRect(360, 530, 131, 16))
        self.RawSpectralLabel.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.RawSpectralLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RawSpectralLabel.setObjectName("RawSpectralLabel")
        self.Choice_Cosmic = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.Choice_Cosmic.setEnabled(False)
        self.Choice_Cosmic.setGeometry(QtCore.QRect(1230, 0, 151, 25))
        self.Choice_Cosmic.setObjectName("Choice_Cosmic")
        self.Choice_Baseline = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.Choice_Baseline.setEnabled(False)
        self.Choice_Baseline.setGeometry(QtCore.QRect(1410, 0, 131, 25))
        self.Choice_Baseline.setObjectName("Choice_Baseline")
        self.Choice_Normalization = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.Choice_Normalization.setEnabled(False)
        self.Choice_Normalization.setGeometry(QtCore.QRect(1230, 20, 181, 25))
        self.Choice_Normalization.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.Choice_Normalization.setObjectName("Choice_Normalization")
        self.Cropmin = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.Cropmin.setEnabled(False)
        self.Cropmin.setGeometry(QtCore.QRect(1140, 0, 81, 21))
        self.Cropmin.setAcceptDrops(False)
        self.Cropmin.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Cropmin.setObjectName("Cropmin")
        self.Cropmax = QtWidgets.QTextEdit(parent=self.centralwidget)
        self.Cropmax.setEnabled(False)
        self.Cropmax.setGeometry(QtCore.QRect(1140, 22, 81, 21))
        self.Cropmax.setAcceptDrops(False)
        self.Cropmax.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Cropmax.setObjectName("Cropmax")
        self.Begin_Pro = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Begin_Pro.setEnabled(False)
        self.Begin_Pro.setGeometry(QtCore.QRect(1540, 0, 161, 41))
        self.Begin_Pro.setObjectName("Begin_Pro")
        self.Button_Save = QtWidgets.QPushButton(parent=self.centralwidget)
        self.Button_Save.setEnabled(False)
        self.Button_Save.setGeometry(QtCore.QRect(1710, 0, 211, 41))
        self.Button_Save.setObjectName("Button_Save")
        self.FWHMmap = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.FWHMmap.setGeometry(QtCore.QRect(1320, 50, 591, 471))
        self.FWHMmap.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.FWHMmap.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.FWHMmap.setObjectName("FWHMmap")
        self.RawmapPeak = QtWidgets.QLabel(parent=self.centralwidget)
        self.RawmapPeak.setGeometry(QtCore.QRect(115, 500, 191, 16))
        self.RawmapPeak.setObjectName("RawmapPeak")
        self.XList = QtWidgets.QListWidget(parent=self.centralwidget)
        self.XList.setGeometry(QtCore.QRect(10, 540, 91, 221))
        self.XList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.XList.setObjectName("XList")
        self.YList = QtWidgets.QListWidget(parent=self.centralwidget)
        self.YList.setGeometry(QtCore.QRect(10, 780, 91, 211))
        self.YList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.YList.setObjectName("YList")
        self.RawXPosition = QtWidgets.QLabel(parent=self.centralwidget)
        self.RawXPosition.setGeometry(QtCore.QRect(120, 535, 241, 20))
        self.RawXPosition.setObjectName("RawXPosition")
        self.CropOrNot = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.CropOrNot.setEnabled(False)
        self.CropOrNot.setGeometry(QtCore.QRect(1060, 0, 121, 41))
        self.CropOrNot.setObjectName("CropOrNot")
        self.Choice_Denoise = QtWidgets.QCheckBox(parent=self.centralwidget)
        self.Choice_Denoise.setEnabled(False)
        self.Choice_Denoise.setGeometry(QtCore.QRect(1410, 20, 131, 25))
        self.Choice_Denoise.setObjectName("Choice_Denoise")
        self.FWHMmapLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.FWHMmapLabel.setGeometry(QtCore.QRect(1590, 50, 101, 20))
        self.FWHMmapLabel.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.FWHMmapLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FWHMmapLabel.setObjectName("FWHMmapLabel")
        self.RawYPosition = QtWidgets.QLabel(parent=self.centralwidget)
        self.RawYPosition.setGeometry(QtCore.QRect(120, 550, 231, 20))
        self.RawYPosition.setObjectName("RawYPosition")
        self.Promap = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.Promap.setGeometry(QtCore.QRect(715, 50, 601, 471))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Promap.sizePolicy().hasHeightForWidth())
        self.Promap.setSizePolicy(sizePolicy)
        self.Promap.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Promap.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.Promap.setObjectName("Promap")
        self.RawdataSpec = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.RawdataSpec.setGeometry(QtCore.QRect(110, 530, 601, 461))
        self.RawdataSpec.setMaximumSize(QtCore.QSize(601, 471))
        self.RawdataSpec.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.RawdataSpec.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.RawdataSpec.setObjectName("RawdataSpec")
        self.PromapPeak = QtWidgets.QLabel(parent=self.centralwidget)
        self.PromapPeak.setGeometry(QtCore.QRect(720, 500, 191, 16))
        self.PromapPeak.setObjectName("PromapPeak")
        self.PromapLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.PromapLabel.setGeometry(QtCore.QRect(940, 50, 161, 16))
        self.PromapLabel.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.PromapLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PromapLabel.setObjectName("PromapLabel")
        self.ProSpectralLabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.ProSpectralLabel.setGeometry(QtCore.QRect(930, 530, 181, 16))
        self.ProSpectralLabel.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.ProSpectralLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ProSpectralLabel.setObjectName("ProSpectralLabel")
        self.ProXPosition = QtWidgets.QLabel(parent=self.centralwidget)
        self.ProXPosition.setGeometry(QtCore.QRect(720, 535, 241, 20))
        self.ProXPosition.setObjectName("ProXPosition")
        self.ProYPosition = QtWidgets.QLabel(parent=self.centralwidget)
        self.ProYPosition.setGeometry(QtCore.QRect(720, 550, 231, 20))
        self.ProYPosition.setObjectName("ProYPosition")
        self.XposLable = QtWidgets.QLabel(parent=self.centralwidget)
        self.XposLable.setGeometry(QtCore.QRect(10, 521, 71, 16))
        self.XposLable.setObjectName("XposLable")
        self.YposLable = QtWidgets.QLabel(parent=self.centralwidget)
        self.YposLable.setGeometry(QtCore.QRect(10, 761, 71, 16))
        self.YposLable.setObjectName("YposLable")
        self.FWHMTable = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.FWHMTable.setGeometry(QtCore.QRect(1320, 530, 591, 461))
        self.FWHMTable.setObjectName("FWHMTable")
        self.FWHMTable.setColumnCount(4)
        self.FWHMTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.FWHMTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.FWHMTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.FWHMTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.FWHMTable.setHorizontalHeaderItem(3, item)
        self.FWHMTable.horizontalHeader().setDefaultSectionSize(117)
        self.FWHMTable.verticalHeader().setCascadingSectionResizes(False)
        self.FWHMTable.verticalHeader().setDefaultSectionSize(30)
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(900, 10, 151, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.label_2.setObjectName("label_2")
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(1540, 0, 161, 41))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.Croplabel = QtWidgets.QLabel(parent=self.centralwidget)
        self.Croplabel.setGeometry(QtCore.QRect(870, 500, 431, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        self.Croplabel.setFont(font)
        self.Croplabel.setText("")
        self.Croplabel.setObjectName("Croplabel")
        self.Promap.raise_()
        self.PromapLabel.raise_()
        self.ProdataSpec.raise_()
        self.RawdataSpec.raise_()
        self.Fileselectbutton.raise_()
        self.SelectedFileBrowser.raise_()
        self.Rawmap.raise_()
        self.RawmapLabel.raise_()
        self.AxisList.raise_()
        self.DataRowsCols.raise_()
        self.PeakposLable.raise_()
        self.RawSpectralLabel.raise_()
        self.Choice_Cosmic.raise_()
        self.Choice_Baseline.raise_()
        self.Choice_Normalization.raise_()
        self.Cropmin.raise_()
        self.Cropmax.raise_()
        self.Begin_Pro.raise_()
        self.Button_Save.raise_()
        self.FWHMmap.raise_()
        self.RawmapPeak.raise_()
        self.RawXPosition.raise_()
        self.CropOrNot.raise_()
        self.Choice_Denoise.raise_()
        self.FWHMmapLabel.raise_()
        self.RawYPosition.raise_()
        self.XList.raise_()
        self.YList.raise_()
        self.PromapPeak.raise_()
        self.ProSpectralLabel.raise_()
        self.ProXPosition.raise_()
        self.ProYPosition.raise_()
        self.XposLable.raise_()
        self.YposLable.raise_()
        self.FWHMTable.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.progressBar.raise_()
        self.Croplabel.raise_()
        RamanFWHM.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=RamanFWHM)
        self.statusbar.setObjectName("statusbar")
        RamanFWHM.setStatusBar(self.statusbar)

        self.retranslateUi(RamanFWHM)
        self.AxisList.setCurrentRow(-1)
        self.CropOrNot.clicked['bool'].connect(self.Cropmin.setEnabled) # type: ignore
        self.CropOrNot.clicked['bool'].connect(self.Cropmax.setEnabled) # type: ignore
        self.Begin_Pro.clicked['bool'].connect(self.Button_Save.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(RamanFWHM)

    def retranslateUi(self, RamanFWHM):
        _translate = QtCore.QCoreApplication.translate
        RamanFWHM.setWindowTitle(_translate("RamanFWHM", "RamanFWHM"))
        self.Fileselectbutton.setText(_translate("RamanFWHM", "Select File"))
        self.RawmapLabel.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#ff0000;\">Raw data map</span></p></body></html>"))
        self.PeakposLable.setText(_translate("RamanFWHM", "Peak positions"))
        self.RawSpectralLabel.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#ff0000;\">Raw data spectral</span></p></body></html>"))
        self.Choice_Cosmic.setText(_translate("RamanFWHM", "Cosmic rays removal"))
        self.Choice_Baseline.setText(_translate("RamanFWHM", "Baseline correction"))
        self.Choice_Normalization.setText(_translate("RamanFWHM", "Max intensity normalisation"))
        self.Cropmin.setToolTip(_translate("RamanFWHM", "<html><head/><body><p>The peak value you want to crop from</p></body></html>"))
        self.Cropmin.setHtml(_translate("RamanFWHM", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">900</span></p></body></html>"))
        self.Cropmax.setToolTip(_translate("RamanFWHM", "<html><head/><body><p>The peak value you want to crop to</p></body></html>"))
        self.Cropmax.setHtml(_translate("RamanFWHM", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">1000</span></p></body></html>"))
        self.Begin_Pro.setToolTip(_translate("RamanFWHM", "<html><head/><body><p>Begin preprocessing input data.</p></body></html>"))
        self.Begin_Pro.setWhatsThis(_translate("RamanFWHM", "<html><head/><body><p><br/></p></body></html>"))
        self.Begin_Pro.setText(_translate("RamanFWHM", "Begin Processing"))
        self.Button_Save.setText(_translate("RamanFWHM", "Save FWHM data"))
        self.RawmapPeak.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">Current Peak: </span></p></body></html>"))
        self.RawXPosition.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">Current X: </span></p></body></html>"))
        self.CropOrNot.setText(_translate("RamanFWHM", "Crop data"))
        self.Choice_Denoise.setText(_translate("RamanFWHM", "Gaussian denoise"))
        self.FWHMmapLabel.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#ff0000;\">FWHM map</span></p></body></html>"))
        self.RawYPosition.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">Current Y:</span></p></body></html>"))
        self.PromapPeak.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">Current Peak: </span></p></body></html>"))
        self.PromapLabel.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#ff0000;\">Processed data map</span></p></body></html>"))
        self.ProSpectralLabel.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#ff0000;\">Processed data spectral</span></p></body></html>"))
        self.ProXPosition.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">Current X: </span></p></body></html>"))
        self.ProYPosition.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700; color:#ff0000;\">Current Y:</span></p></body></html>"))
        self.XposLable.setText(_translate("RamanFWHM", "X position"))
        self.YposLable.setText(_translate("RamanFWHM", "Y position"))
        item = self.FWHMTable.horizontalHeaderItem(0)
        item.setText(_translate("RamanFWHM", "X"))
        item = self.FWHMTable.horizontalHeaderItem(1)
        item.setText(_translate("RamanFWHM", "Y"))
        item = self.FWHMTable.horizontalHeaderItem(2)
        item.setText(_translate("RamanFWHM", "FWHM"))
        item = self.FWHMTable.horizontalHeaderItem(3)
        item.setText(_translate("RamanFWHM", "FWHM_error"))
        self.label.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:11pt;\">Data preprocessing</span></p></body></html>"))
        self.label_2.setText(_translate("RamanFWHM", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Data Input</span></p></body></html>"))
