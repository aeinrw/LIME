import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
from Ui_window import Ui_MainWindow
from skimage import io
from LIME import LIME

import matplotlib
matplotlib.use("Qt5Agg")


class ImgFigure(FigureCanvas):
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi)
        super(ImgFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.originImgFigure = ImgFigure(dpi=100)
        self.enhancedImgFigure = ImgFigure(dpi=100)

        self.originImgFigure.axes.get_yaxis().set_visible(False)
        self.originImgFigure.axes.get_xaxis().set_visible(False)
        self.gridlayout1 = QGridLayout(self.origin_gb)
        self.gridlayout1.addWidget(self.originImgFigure)

        self.enhancedImgFigure.axes.get_yaxis().set_visible(False)
        self.enhancedImgFigure.axes.get_xaxis().set_visible(False)
        self.gridlayout2 = QGridLayout(self.enhanced_gb)
        self.gridlayout2.addWidget(self.enhancedImgFigure)

        self.statusBar.showMessage("请选择文件.")

    def loadImg(self):
        self.imgPath = QFileDialog.getOpenFileName(
            self, "请选择图片", "./data", "All Files (*)")[0]

        self.originImg = io.imread(self.imgPath)
        self.originImgFigure.axes.imshow(self.originImg)
        self.originImgFigure.draw()
        self.statusBar.showMessage("当前图片路径: "+self.imgPath)

        self.enhance_btn.setEnabled(True)
        self.save_btn.setEnabled(False)

    def enhanceImg(self):
        lime = LIME(self.imgPath)
        lime.optimizeIllumMap(self.progressBar)
        self.result = lime.enhance()
        self.enhancedImgFigure.axes.imshow(self.result)
        self.enhancedImgFigure.draw()
        self.statusBar.showMessage("当前图片路径: "+self.imgPath+"   图像增强成功")

        self.enhance_btn.setEnabled(False)
        self.save_btn.setEnabled(True)

    def saveImg(self):
        savePath = QFileDialog.getSaveFileName(
            self, "请选择保存位置", "./data", "BMP格式 (*.bmp);;JPG格式 (*.jpg)")[0]
        if savePath != '':
            io.imsave(savePath, self.result)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
