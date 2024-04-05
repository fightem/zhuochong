from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame

from PyQt5 import QtCore, QtGui, QtWidgets
# import pymysql
import re
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import QTimer
class MyPlainTextEdit(QPlainTextEdit):  #父类为QPlainTextEdit

    def __init__(self,parent=None):
        super(MyPlainTextEdit, self).__init__(parent)
        # self.setAcceptRichText(False)

    def keyPressEvent(self, event: QKeyEvent): #重写keyPressEvent方法
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:#ctrl+回车
            self.insertPlainText('\n')                                              #添加换行
        elif self.toPlainText() and event.key() == Qt.Key_Return:                                          #回车
            self.demo_function() # 调用 demo 函数
        else:
            super().keyPressEvent(event)

    def demo_function(self):
        self.setEnabled(False)          #主函数使用undoAvailable监听信号
        self.setUndoRedoEnabled(False)  #设置焦点
        self.setUndoRedoEnabled(True)   #设置焦点

if __name__ == '__main__':
    import sys
    app = QApplication([])
    main_window = MyPlainTextEdit()
    main_window.show()
    app.exec_()