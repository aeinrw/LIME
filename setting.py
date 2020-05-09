from Ui_setting import Ui_Form
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal


class SettingWindow(QWidget, Ui_Form):

    changeParameterSignal = pyqtSignal(float, float, float)

    def __init__(self):
        super(SettingWindow, self).__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_confirmBtn_clicked(self):
        alpha = (401-self.smoothnessSlider.value()) / 100
        gamma = self.brightnessSlider.value() / 100
        weigh = self.denosieSlider.value() / 100
        self.changeParameterSignal.emit(alpha, gamma, weigh)
        self.hide()

    @pyqtSlot()
    def on_cancelBtn_clicked(self):
        self.hide()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = SettingWindow()
    window.show()
    sys.exit(app.exec())
