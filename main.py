import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import numpy as np
from Ui_mainwindow import Ui_Form
from skimage import io
from LIME import LIME

import matplotlib
matplotlib.use("Qt5Agg")


class ImgFigure(FigureCanvas):
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi)
        super(ImgFigure, self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)


class Window(QWidget, Ui_Form):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.originImgFigure = ImgFigure(dpi=100)
        self.enhancedImgFigure = ImgFigure(dpi=100)

        self.originImgFigure.axes.get_yaxis().set_visible(False)
        self.originImgFigure.axes.get_xaxis().set_visible(False)
        self.gridlayout1 = QGridLayout(self.origin_group)
        self.gridlayout1.addWidget(self.originImgFigure)

        self.enhancedImgFigure.axes.get_yaxis().set_visible(False)
        self.enhancedImgFigure.axes.get_xaxis().set_visible(False)
        self.gridlayout2 = QGridLayout(self.enhanced_group)
        self.gridlayout2.addWidget(self.enhancedImgFigure)

    def loadImg(self):
        self.imgPath = QFileDialog.getOpenFileName(
            self, "请选择图片", "./data", "All Files (*)")[0]

        self.originImg = io.imread(self.imgPath)
        self.originImgFigure.axes.imshow(self.originImg)
        self.originImgFigure.draw()

    def enhanceImg(self):
        lime = LIME(self.imgPath)
        self.enhancedImgFigure.axes.imshow(lime.enhance())
        self.enhancedImgFigure.draw()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
