import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from Ui_mainwindow import Ui_MainWindow
from about import AboutWindow
from skimage import io


class ImgFigure(FigureCanvas):
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi)
        super(ImgFigure, self).__init__(self.fig)
        self.L_axes = self.fig.add_subplot(131)
        self.T_axes = self.fig.add_subplot(132)
        self.R_axes = self.fig.add_subplot(133)
        self.L_axes.get_yaxis().set_visible(False)
        self.L_axes.get_xaxis().set_visible(False)
        self.R_axes.get_yaxis().set_visible(False)
        self.R_axes.get_xaxis().set_visible(False)
        self.T_axes.get_yaxis().set_visible(False)
        self.T_axes.get_xaxis().set_visible(False)


class WorkThread(QThread):

    finishSignal = pyqtSignal(np.ndarray, np.ndarray)

    def __init__(self, imgPath, progressBar, alpha, gamma):
        super(WorkThread, self).__init__()

        from LIME import LIME
        self.lime = LIME(imgPath, alpha, gamma)
        self.lime.setMaximumSignal.connect(progressBar.setMaximum)
        self.lime.setValueSignal.connect(progressBar.setValue)

    def run(self):
        T = self.lime.optimizeIllumMap()
        R = self.lime.enhance()
        self.finishSignal.emit(T, R)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.imgFigure = ImgFigure()

        self.layout = QHBoxLayout(self.groupbox)
        self.layout.addWidget(self.imgFigure)

        self.statusBar.showMessage("请选择文件")
        self.progressBar = QProgressBar()
        self.statusBar.addPermanentWidget(self.progressBar)
        self.progressBar.setVisible(False)

    @pyqtSlot()
    def on_loadBtn_clicked(self):
        #self.imgPath = "./data/7.bmp"
        self.imgPath = QFileDialog.getOpenFileName(
            self, "请选择图片", "./data", "All Files (*)")[0]

        if self.imgPath != '':
            originImg = io.imread(self.imgPath)
            self.imgFigure.L_axes.imshow(originImg)
            self.imgFigure.draw()
            self.statusBar.showMessage("当前图片路径: " + self.imgPath)

            self.progressBar.setValue(0)

            self.enhanceBtn.setEnabled(True)
            self.saveBtn.setEnabled(False)

    @pyqtSlot()
    def on_enhanceBtn_clicked(self):
        self.progressBar.setVisible(True)
        self.smoothnessSlider.setEnabled(False)
        self.brightnessSlider.setEnabled(False)
        alpha = (401-self.smoothnessSlider.value()) / 100
        gamma = self.brightnessSlider.value() / 100
        self.workThread = WorkThread(
            self.imgPath, self.progressBar, alpha, gamma)
        self.workThread.start()
        self.workThread.finishSignal.connect(self.on_workThread_finishSignal)

    def on_workThread_finishSignal(self, T, R):
        self.progressBar.setVisible(False)
        self.smoothnessSlider.setEnabled(True)
        self.brightnessSlider.setEnabled(True)
        self.T = T
        self.R = R
        self.statusBar.showMessage("当前图片路径: " + self.imgPath + "   图像增强成功")
        self.imgFigure.T_axes.imshow(self.T, cmap=plt.get_cmap('OrRd_r'))
        self.imgFigure.R_axes.imshow(self.R)
        self.imgFigure.draw()
        self.saveBtn.setEnabled(True)

    @pyqtSlot()
    def on_saveBtn_clicked(self):
        savePath = QFileDialog.getSaveFileName(
            self, "请选择保存位置", "./data", "BMP格式 (*.bmp);;JPG格式 (*.jpg)")[0]
        if savePath != '':
            io.imsave(savePath, self.R)

    @pyqtSlot()
    def on_aboutAct_triggered(self):
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
