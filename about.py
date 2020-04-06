from Ui_about import Ui_Form
from PyQt5.QtWidgets import QWidget, QApplication


class AboutWindow(QWidget, Ui_Form):
    def __init__(self):
        super(AboutWindow, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = AboutWindow()
    window.show()
    sys.exit(app.exec())
