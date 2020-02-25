# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Source\LIME\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1450, 800)
        Form.setMinimumSize(QtCore.QSize(1450, 800))
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.origin_group = QtWidgets.QGroupBox(Form)
        self.origin_group.setMinimumSize(QtCore.QSize(700, 700))
        self.origin_group.setObjectName("origin_group")
        self.gridLayout.addWidget(self.origin_group, 0, 0, 1, 1)
        self.enhanced_group = QtWidgets.QGroupBox(Form)
        self.enhanced_group.setMinimumSize(QtCore.QSize(700, 700))
        self.enhanced_group.setObjectName("enhanced_group")
        self.gridLayout.addWidget(self.enhanced_group, 0, 1, 1, 1)
        self.load_btn = QtWidgets.QPushButton(Form)
        self.load_btn.setMinimumSize(QtCore.QSize(200, 0))
        self.load_btn.setObjectName("load_btn")
        self.gridLayout.addWidget(self.load_btn, 1, 0, 1, 1)
        self.enhance_btn = QtWidgets.QPushButton(Form)
        self.enhance_btn.setMinimumSize(QtCore.QSize(200, 0))
        self.enhance_btn.setObjectName("enhance_btn")
        self.gridLayout.addWidget(self.enhance_btn, 1, 1, 1, 1)

        self.retranslateUi(Form)
        self.load_btn.clicked.connect(Form.loadImg)
        self.enhance_btn.clicked.connect(Form.enhanceImg)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.origin_group.setTitle(_translate("Form", "初始图片"))
        self.enhanced_group.setTitle(_translate("Form", "增强后的图片"))
        self.load_btn.setText(_translate("Form", "加载图片"))
        self.enhance_btn.setText(_translate("Form", "图像增强"))
