from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)

        # 创建透明的窗口
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(-200, -160, 671, 531))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        self.label.setFont(font)
        self.label.setStyleSheet("background-image: url(./logins_register/img/chatbox.png);")
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")

        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(90, 90, 211, 91))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(13)
        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("border: none")
        self.textEdit.setObjectName("textEdit")




        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)



    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


    def changeDialog(self,message):
        self.textEdit.setText(message)


from PyQt5 import QtCore, QtGui, QtWidgets
class CustomDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 添加鼠标按下和移动事件
        self.mouse_dragging = False
        self.drag_position = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_dragging = True
            self.drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.mouse_dragging:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_dragging = False
            self.drag_position = None

    def changeDialog(self, message):
        self.ui.textEdit.setText(message)

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame

if __name__ == '__main__':
    app = QApplication([])
    main_window = CustomDialog()
    main_window.show()
    app.exec_()
