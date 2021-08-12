# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Source\LIME\illuMap.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 600)
        Form.setMinimumSize(QtCore.QSize(500, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/image/denoise.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.colorComboBox = QtWidgets.QComboBox(Form)
        self.colorComboBox.setObjectName("colorComboBox")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.colorComboBox.addItem("")
        self.horizontalLayout.addWidget(self.colorComboBox)
        self.confirmBtn = QtWidgets.QPushButton(Form)
        self.confirmBtn.setObjectName("confirmBtn")
        self.horizontalLayout.addWidget(self.confirmBtn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.saveIlluMapBtn = QtWidgets.QPushButton(Form)
        self.saveIlluMapBtn.setObjectName("saveIlluMapBtn")
        self.horizontalLayout.addWidget(self.saveIlluMapBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "光照图"))
        self.label.setText(_translate("Form", "光照图颜色调整"))
        self.colorComboBox.setItemText(0, _translate("Form", "红黄"))
        self.colorComboBox.setItemText(1, _translate("Form", "灰色"))
        self.colorComboBox.setItemText(2, _translate("Form", "红粉"))
        self.colorComboBox.setItemText(3, _translate("Form", "蓝绿"))
        self.colorComboBox.setItemText(4, _translate("Form", "黄绿蓝"))
        self.colorComboBox.setItemText(5, _translate("Form", "粉蓝"))
        self.confirmBtn.setText(_translate("Form", "确认"))
        self.saveIlluMapBtn.setText(_translate("Form", "保存光照图"))
