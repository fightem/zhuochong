from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
from PyQt5 import QtCore, QtGui
import sys
import pymysql
class LoginRegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('登录注册页面')
        self.resize(400, 300)

        layout = QVBoxLayout()

        # 欢迎信息
        welcome_label = QLabel('欢迎进入桌宠服务')
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498DB;")
        layout.addWidget(welcome_label, alignment=QtCore.Qt.AlignCenter)

        # 添加间距
        layout.addSpacing(10)

        # 输入框布局
        input_layout = QVBoxLayout()

        username_label = QLabel('用户名:')
        input_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        input_layout.addWidget(self.username_input)

        password_label = QLabel('密码:')
        input_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        input_layout.addWidget(self.password_input)

        # 添加竖直间距
        input_layout.addSpacing(10)

        layout.addLayout(input_layout)

        # 登录和注册按钮布局
        button_layout = QHBoxLayout()

        login_button = QPushButton('登录')
        login_button.setStyleSheet("background-color: #27AE60; color: white; border: none; padding: 8px 16px;")
        login_button.clicked.connect(self.check_credentials)
        button_layout.addWidget(login_button)

        register_button = QPushButton('注册')
        register_button.setStyleSheet("background-color: #3498DB; color: white; border: none; padding: 8px 16px;")
        register_button.clicked.connect(self.show_register_page)
        button_layout.addWidget(register_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def check_credentials(self):
        # 检查用户名和密码
        username = self.username_input.text()
        password = self.password_input.text()
        print(username, password)

        # 1.链接数据库
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='520520hxa', charset='utf8', db='zhuochong2333')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 2.发送指令

        sql = "select * from user_login"
        cursor.execute(sql)
        list1 = cursor.fetchall()
        if list1:
            print(list1)

        else:
            print("没数据了")

        # 3.关闭链接
        cursor.close()
        conn.close()

        index = 0
        for i in list1:
            if username == i["username"] and password == i["password"]:
                QMessageBox.information(self, '登录成功', '欢迎回来，admin！')
                index = 1
        if index == 0:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误！')

    def show_register_page(self):
        # 切换到注册页面
        register_page = RegisterPage()
        self.close()
        register_page.show()

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('注册页面')
        self.resize(400, 300)

        layout = QVBoxLayout()

        # 注册信息输入
        username_label = QLabel('用户名:')
        layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        layout.addWidget(self.username_input)

        password_label = QLabel('密码:')
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # 添加竖直间距
        layout.addSpacing(10)

        # 注册按钮
        register_button = QPushButton('注册')
        register_button.setStyleSheet("background-color: #3498DB; color: white; border: none; padding: 8px 16px;")
        register_button.clicked.connect(self.register_user)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def register_user(self):
        # 实现注册逻辑，这里只是示例
        username = self.username_input.text()
        password = self.password_input.text()

        QMessageBox.information(self, '注册成功', f'账号 {username} 注册成功！')




class MiniProductPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mini Product Introduction')
        self.resize(400, 300)

        layout = QVBoxLayout()
        intro_label = QLabel('欢迎来到我们的产品介绍页面！')
        intro_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(intro_label)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_page = LoginRegisterPage()
    login_page.show()
    sys.exit(app.exec_())
