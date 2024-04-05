from PyQt5 import QtWidgets
from login_index import Ui_Form_1
from RumiaPet_main.UI_main.untitled_2 import Ui_Form_2
# import pymysql
from PyQt5.QtWidgets import QApplication

from rumia import App

# 数据库中进行用户的账号和密码的相关检查，有就返回true，没有就返回false
# def check_bysql(username,password):
#     # 1.链接数据库
#     conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='520520hxa', charset='utf8', db='zhuochong2333')
#     cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#     # 2.发送指令
#
#     sql = "select * from user_login"
#     cursor.execute(sql)
#     list1 = cursor.fetchall()
#     if list1:
#         print(list1)
#
#     else:
#         return False
#
#     for item in list1:
#         if item['username'] == username and item['password'] == password:
#             return True
#
#     return False
#
#
#     # 3.关闭链接
#     cursor.close()
#     conn.close()






class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form_1()
        self.ui.setupUi(self)
        self.ui.toolButton_3.clicked.connect(self.on_toolButton_clicked)
        self.another_window = None

    def on_toolButton_clicked(self):
        # 创建另一个界面或执行其他操作
        if self.check_credentials():
            if not self.another_window:
                self.close()
                self.another_window = AnotherWindow()
            self.another_window.show()
        else:
            # 如果条件不符合，可以执行其他操作，比如弹出提示框
            QtWidgets.QMessageBox.warning(self, "提示", "账号或密码不正确")

    def check_credentials(self):
        # 在这个函数中编写检查账号和密码是否符合条件的逻辑
        # 如果符合条件，返回 True；否则返回 False
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        if (check_bysql(username=username, password=password)) == True:
            return True
        else:
            return False






    # 这里简单示范一个检查逻辑，实际情况根据需要自行实现



# 功能
class AnotherWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.two = Ui_Form_2()
        self.two.setupUi(self)

        self.two.toolButton.clicked.connect(self.on_toolButton_clicked_pet)

        self.two.toolButton_2.clicked.connect(self.display_page1)
        self.two.toolButton_3.clicked.connect(self.display_page2)
        self.two.toolButton_4.clicked.connect(self.display_page3)
        self.two.toolButton_5.clicked.connect(self.display_page4)
        self.two.toolButton_6.clicked.connect(self.display_page5)

    def on_toolButton_clicked_pet(self):
        app = QApplication(sys.argv)
        pet = App()
        sys.exit(app.exec_())

        print("启动桌宠")

    #
    def display_page1(self):
        self.two.stackedWidget.setCurrentIndex(0)

    def display_page2(self):
        self.two.stackedWidget.setCurrentIndex(1)

    def display_page3(self):
        self.two.stackedWidget.setCurrentIndex(2)

    def display_page4(self):
        self.two.stackedWidget.setCurrentIndex(3)

    def display_page5(self):
        self.two.stackedWidget.setCurrentIndex(4)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
