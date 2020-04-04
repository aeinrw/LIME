from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import numpy as np
from Ui_window import Ui_MainWindow
from skimage import io


class ImgFigure(FigureCanvas):
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi)
        super(ImgFigure, self).__init__(self.fig)
        self.axes1 = self.fig.add_subplot(121)
        self.axes2 = self.fig.add_subplot(122)


class WorkThread(QThread):

    finishSignal = pyqtSignal(np.ndarray)

    def __init__(self, imgPath, progressBar):
        super(WorkThread, self).__init__()

        from LIME import LIME
        self.lime = LIME(imgPath)
        self.lime.setMaximumSignal.connect(progressBar.setMaximum)
        self.lime.setValueSignal.connect(progressBar.setValue)

    def run(self):
        self.lime.optimizeIllumMap()
        result = self.lime.enhance()
        self.finishSignal.emit(result)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        self.imgFigure = ImgFigure()

        self.imgFigure.axes1.get_yaxis().set_visible(False)
        self.imgFigure.axes1.get_xaxis().set_visible(False)
        self.imgFigure.axes2.get_yaxis().set_visible(False)
        self.imgFigure.axes2.get_xaxis().set_visible(False)

        self.layout = QHBoxLayout(self.groupbox)
        self.layout.addWidget(self.imgFigure)

        self.statusBar.showMessage("请选择文件")

    @pyqtSlot()
    def on_loadBtn_clicked(self):
        self.imgPath = QFileDialog.getOpenFileName(
            self, "请选择图片", "./data", "All Files (*)")[0]

        if self.imgPath != '':
            originImg = io.imread(self.imgPath)
            self.imgFigure.axes1.imshow(originImg)
            self.imgFigure.draw()
            self.statusBar.showMessage("当前图片路径: "+self.imgPath)

            self.enhanceBtn.setEnabled(True)
            self.saveBtn.setEnabled(False)

    @pyqtSlot()
    def on_enhanceBtn_clicked(self):
        self.workThread = WorkThread(self.imgPath, self.progressBar)
        self.workThread.start()
        self.workThread.finishSignal.connect(self.on_workThread_finishSignal)

    def on_workThread_finishSignal(self, result):
        self.result = result
        self.statusBar.showMessage("当前图片路径: " + self.imgPath + "   图像增强成功")
        self.imgFigure.axes2.imshow(self.result)
        self.imgFigure.draw()
        self.enhanceBtn.setEnabled(False)
        self.saveBtn.setEnabled(True)

    @pyqtSlot()
    def on_saveBtn_clicked(self):
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
