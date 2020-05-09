from matplotlib.pyplot import imread, imsave, get_cmap
from skimage import restoration

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar, QFileDialog, QMessageBox, QMainWindow, qApp


from Ui_mainwindow import Ui_MainWindow
from about import AboutWindow
from illuMap import IlluMapWindow
from utli import ImgFigure, WorkThread


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)

        # -------setupUi------------
        self.originImgFigure = ImgFigure()
        self.enhancedImgFigure = ImgFigure()

        self.originImgLayout = QHBoxLayout(self.originBox)
        self.enhancedImgLayout = QHBoxLayout(self.enhancedBox)
        self.originImgLayout.addWidget(self.originImgFigure)
        self.enhancedImgLayout.addWidget(self.enhancedImgFigure)

        self.statusBar.showMessage("请选择文件")
        self.progressBar = QProgressBar()
        self.statusBar.addPermanentWidget(self.progressBar)
        self.progressBar.setVisible(False)
        # -------setupUi------------

        with open("./resource/config/.history", 'r') as fp:
            self.action1 = self.recentOpenMenu.addAction(fp.readline())
            self.action1.triggered.connect(
                lambda: self.openImage(self.action1.text()))
            self.action2 = self.recentOpenMenu.addAction(fp.readline())
            self.action2.triggered.connect(
                lambda: self.openImage(self.action2.text()))
            self.action3 = self.recentOpenMenu.addAction(fp.readline())
            self.action3.triggered.connect(
                lambda: self.openImage(self.action3.text()))

    @pyqtSlot()
    def on_openAct_triggered(self):
        # imgPath = "./data/13.jpg"
        imgPath = QFileDialog.getOpenFileName(
            self, "请选择图片", "./data", "All Files (*)")[0]
        self.openImage(imgPath)

    def openImage(self, imgPath):
        self.imgPath = imgPath.strip()
        if imgPath != '':
            self.originImg = imread(self.imgPath)
            self.originImgFigure.axes.imshow(self.originImg)
            self.originImgFigure.draw()
            self.statusBar.showMessage("当前图片路径: " + self.imgPath)

            self.progressBar.setValue(0)

            self.enhanceAct.setEnabled(True)
            self.saveAct.setEnabled(False)
        else:
            QMessageBox.warning(self, "提示", "请重新选择图片")

    @pyqtSlot()
    def on_enhanceAct_triggered(self):
        self.progressBar.setValue(0)
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
        self.smoothnessSlider.setEnabled(True)
        self.brightnessSlider.setEnabled(True)
        self.T = T
        self.R = R
        self.statusBar.showMessage("当前图片路径: " + self.imgPath + "   图像增强成功")
        # self.imgFigure.T_axes.imshow(self.T, cmap=get_cmap('OrRd_r'))
        self.enhancedImgFigure.axes.imshow(self.R)

        self.progressBar.setValue(self.progressBar.maximum())
        self.progressBar.setVisible(False)

        self.enhancedImgFigure.draw()
        self.saveAct.setEnabled(True)

    @pyqtSlot()
    def on_saveAsAct_triggered(self):
        savePath = QFileDialog.getSaveFileName(
            self, "请选择保存位置", "./data", "BMP格式 (*.bmp);;JPG格式 (*.jpg)")[0]
        if savePath != '':
            imsave(savePath, self.R)
            QMessageBox.about(self, "提示", "保存成功")
        else:
            QMessageBox.warning(self, "提示", "请重新选择保存位置")

    @pyqtSlot()
    def on_saveAct_triggered(self):
        savePath = self.imgPath
        imsave(savePath, self.R)
        QMessageBox.about(self, "提示", "保存成功")

    @pyqtSlot()
    def on_clearAct_triggered(self):
        self.originImgFigure.axes.cla()
        self.originImgFigure.draw()
        self.enhancedImgFigure.axes.cla()
        self.enhancedImgFigure.draw()

    @pyqtSlot()
    def on_quitAct_triggered(self):
        qApp.quit()

    @pyqtSlot()
    def on_denoiseAct_triggered(self):
        self.R = restoration.denoise_tv_bregman(self.R, 3)
        self.enhancedImgFigure.axes.imshow(self.R)
        self.enhancedImgFigure.draw()
        QMessageBox.about(self, "提示", "去噪成功")

        # -------------其他界面-------------

    @pyqtSlot()
    def on_aboutAct_triggered(self):
        self.aboutWindow = AboutWindow()
        self.aboutWindow.show()

    @pyqtSlot()
    def on_illuMapAct_triggered(self):
        self.illuMapWindow = IlluMapWindow()
        self.illuMapWindow.figure.axes.imshow(self.T, cmap=get_cmap('OrRd_r'))
        self.illuMapWindow.figure.draw()
        self.illuMapWindow.show()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
