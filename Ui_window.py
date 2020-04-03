# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Source\LIME\window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 700))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupbox.setObjectName("groupbox")
        self.horizontalLayout_2.addWidget(self.groupbox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(14)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.load_btn = QtWidgets.QPushButton(self.centralwidget)
        self.load_btn.setObjectName("load_btn")
        self.horizontalLayout.addWidget(self.load_btn)
        self.enhance_btn = QtWidgets.QPushButton(self.centralwidget)
        self.enhance_btn.setEnabled(False)
        self.enhance_btn.setObjectName("enhance_btn")
        self.horizontalLayout.addWidget(self.enhance_btn)
        self.save_btn = QtWidgets.QPushButton(self.centralwidget)
        self.save_btn.setEnabled(False)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout.addWidget(self.save_btn)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1200, 18))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        self.load_btn.clicked.connect(MainWindow.loadImg)
        self.enhance_btn.clicked.connect(MainWindow.enhanceImg)
        self.save_btn.clicked.connect(MainWindow.saveImg)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图像增强系统"))
        self.groupbox.setTitle(_translate("MainWindow", "原始图片/增强后图片"))
        self.load_btn.setText(_translate("MainWindow", "图片加载"))
        self.enhance_btn.setText(_translate("MainWindow", "图片增强"))
        self.save_btn.setText(_translate("MainWindow", "保存图片"))
