# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bagin.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_Form(object):
    def setupUi(self, Form):
        current_dir = os.path.dirname(__file__)
        self.current_dir_str = str(current_dir)
        Form.setObjectName("Form")
        Form.resize(826, 644)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.current_dir_str + "/UI_pic/happy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background:#faf2f5")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(250, 560, 141, 42))
        self.toolButton.setMaximumSize(QtCore.QSize(1000, 600))
        self.toolButton.setStyleSheet("color:rgb(245, 102, 146);\n"
"font: 75 15pt \"微软雅黑\";\n"
"border: 0px solid black;")
        self.toolButton.setObjectName("toolButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(190, 310, 451, 60))
        self.lineEdit.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lineEdit.setStyleSheet(" border: 2px solid black; \n"
"font: 75 25pt \"微软雅黑\";")
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(120, 310, 60, 60))
        self.label_2.setMaximumSize(QtCore.QSize(60, 60))
        self.label_2.setStyleSheet(" border: 0px solid red; ")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(self.current_dir_str + "/UI_pic/登入.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 390, 451, 60))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lineEdit_2.setStyleSheet(" border: 2px solid black; \n"
"font: 75 25pt \"微软雅黑\";")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.toolButton_3 = QtWidgets.QToolButton(Form)
        self.toolButton_3.setGeometry(QtCore.QRect(190, 470, 451, 61))
        self.toolButton_3.setMaximumSize(QtCore.QSize(2000, 2000))
        self.toolButton_3.setMouseTracking(False)
        self.toolButton_3.setStyleSheet("font: 30pt \"黑体\";\n"
"color:rgb(255, 255, 255);\n"
"border: 1px solid ;\n"
"border-radius:15px;\n"
"background:#f6769d")
        self.toolButton_3.setObjectName("toolButton_3")
        self.toolButton_2 = QtWidgets.QToolButton(Form)
        self.toolButton_2.setGeometry(QtCore.QRect(430, 560, 171, 42))
        self.toolButton_2.setMaximumSize(QtCore.QSize(1000, 1000))
        self.toolButton_2.setStyleSheet("color:rgb(245, 102, 146);\n"
"font: 75 15pt \"微软雅黑\";\n"
"border: 0px solid black;")
        self.toolButton_2.setObjectName("toolButton_2")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(120, 390, 60, 60))
        self.label_4.setMaximumSize(QtCore.QSize(60, 60))
        self.label_4.setStyleSheet(" border: 0px solid red; ")
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(self.current_dir_str + "/UI_pic/登入2.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 831, 251))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(self.current_dir_str + "/UI_pic/login_label.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "智能桌宠服务系统"))
        self.toolButton.setText(_translate("Form", "注册用户"))
        self.lineEdit.setPlaceholderText(_translate("Form", "账号"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "密码"))
        self.toolButton_3.setText(_translate("Form", "登入"))
        self.toolButton_2.setText(_translate("Form", "忘记密码"))
