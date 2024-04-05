import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDialog,QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

from UI_main.bagin import Ui_Form as Ui_Form_1
from UI_main.untitled_2 import Ui_Form as Ui_Form_2
from work_place.SmartDeskPet.convert import FileConverter
from pet import App
from work_place.OCR.ocr import OCRProcessor
from work_place.yuying.yuying import SpeechRecognitionService
from work_place.send_IP.send import FileSender
from work_place.send_IP.receive import FileReceiver
from UI_main.password_find import PasswordWindow
from UI_main.register import RegisterWindow
from work_place.translate.fanyi import BaiduTranslator
import os
import sys
import json
import requests
import socket
import threading
import pymysql
import datetime
import UI_main.resources_rc

def check_bysql(username,password):
    # 1.链接数据库
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='520520hxa', charset='utf8', db='zhuochong2333')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 2.发送指令

    sql = "select * from login"
    cursor.execute(sql)
    list1 = cursor.fetchall()
    if list1:
        print(list1)

    else:
        return False

    for item in list1:
        if item['username'] == username and item['password'] == password:
            return True

    return False


    # 3.关闭链接
    cursor.close()
    conn.close()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form_1()
        self.ui.setupUi(self)
        self.ui.toolButton_3.clicked.connect(self.on_toolButton3_clicked)  # 登入
        self.ui.toolButton.clicked.connect(self.on_toolButton_clicked)     # 注册
        self.ui.toolButton_2.clicked.connect(self.on_toolButton2_clicked)  # 忘记密码
        self.another_window = None
        self.register_window = None
        self.find_password = None


#登入
    def on_toolButton3_clicked(self):
        # 创建另一个界面或执行其他操作
        if self.check_credentials():
            if not self.another_window:
                self.close()
                from pet import App
                self.another_window = App()
                self.another_window.show()

                # self.another_window = AnotherWindow()
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


#注册
    def on_toolButton_clicked(self):
        if self.register_window is None or not self.register_window.isVisible():
            self.register_window = RegisterWindow()
        self.register_window.show()

#找回密码
    def on_toolButton2_clicked(self):
        if self.find_password is None or not self.find_password.isVisible():
            self.find_password = PasswordWindow()
        self.find_password.show()


#功能
class AnotherWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.dialogue_num = 0
        self.count_yuyin = 0
        self.count=0
        self.count1=0
        self.two = Ui_Form_2()
        self.two.setupUi(self)
        self.two.toolButton.clicked.connect(self.display_page)
        self.two.toolButton_2.clicked.connect(self.display_page1)
        self.two.toolButton_3.clicked.connect(self.display_page2)
        self.two.toolButton_4.clicked.connect(self.display_page3)
        self.two.toolButton_5.clicked.connect(self.display_page4)
        self.two.toolButton_6.clicked.connect(self.display_page5)
        self.two.toolButton_7.clicked.connect(self.on_toolButton7_clicked)
        self.two.toolButton_8.clicked.connect(self.on_toolButton8_clicked)
        self.two.toolButton_9.clicked.connect(self.on_toolButton9_clicked)
        self.two.toolButton_10.clicked.connect(self.on_toolButton10_clicked)
        self.two.toolButton_11.clicked.connect(self.on_toolButton11_clicked)
        self.two.toolButton_12.clicked.connect(self.on_toolButton12_clicked)
        self.two.pushButton_2.clicked.connect(self.on_pushButton2_clicked)
        self.two.toolButton_13.clicked.connect(self.on_toolButton13_clicked)
        self.two.toolButton_14.clicked.connect(self.on_toolButton14_clicked)
        self.two.toolButton_15.clicked.connect(self.on_toolButton15_clicked)
        self.two.toolButton_16.clicked.connect(self.display_page11)
        self.two.toolButton_17.clicked.connect(self.display_page12)
        self.two.toolButton_18.clicked.connect(self.on_toolButton18_clicked)
        self.two.toolButton_19.clicked.connect(self.on_toolButton19_clicked)


        self.two.pushButton.clicked.connect(self.on_pushButton_clicked)
        self.two.pushButton_3.clicked.connect(self.on_pushButton3_clicked)  #翻译转换
        self.two.pushButton_4.clicked.connect(self.on_pushButton4_clicked)
        self.two.pushButton_5.clicked.connect(self.on_pushButton5_clicked)


#换页面
    def display_page1(self):
        self.two.stackedWidget.setCurrentIndex(0)
    def display_page2(self):
        self.two.stackedWidget.setCurrentIndex(1)
    def display_page3(self):
        self.two.stackedWidget.setCurrentIndex(2)
        self.two.stackedWidget_2.setCurrentIndex(3)
    def display_page4(self):
        self.two.stackedWidget.setCurrentIndex(3)
    def display_page5(self):
        self.two.stackedWidget.setCurrentIndex(4)
    def display_page(self):
        self.two.stackedWidget.setCurrentIndex(5)

    def display_page11(self):
        self.two.stackedWidget_2.setCurrentIndex(1)

    def display_page12(self):
        self.two.stackedWidget_2.setCurrentIndex(2)

#语音对话
    def on_toolButton7_clicked(self):
        print('语音对话被点击了')
        speech = SpeechRecognitionService()
        message = speech.speech_recognition()
        print("录音完毕")
        from TTS_bachongshenzi import tts_and_play
        headers = {'Content-Type': 'application/json'}
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(
            speech.get_access_token())
        payload = json.dumps(
            {"messages": [{"role": "user", "content": f'请限制在100个字以内回答：{message}'}], "stream": True})
        response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        from TTS_bachongshenzi import tts_and_play
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8").replace("data: ", ""))
                msg = data['result']
                tts_and_play(msg)
                # 朗读msg



#产品解释
    def on_toolButton8_clicked(self):
        text = "<span style='font-size: 20px;'>  桌宠是一种小巧可爱的虚拟宠物，通常以软件应用的形式存在于电脑桌面上。它们会在桌面上活动、表情丰富地展现情绪，并且会对用户的操作做出互动响应。\n  这种产品的设计初衷是为了给用户带来陪伴感和乐趣，同时也可以作为桌面工作的休闲娱乐。用户可以抚摸、玩耍或者跟它对话，从而促进放松心情、减轻压力。</span>"
        #QtWidgets.QMessageBox.warning(self, "提示",text)

        msg_box = QtWidgets.QMessageBox()
        # 设置消息框的标题和文本内容
        msg_box.setWindowTitle("桌宠介绍")
        msg_box.setText(text)
        msg_box.setFixedSize(500, 300)
        msg_box.exec_()
#ocr技术
    def on_toolButton9_clicked(self):
        imagePath, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)")
        if imagePath:
            self.two.lineEdit.setText(imagePath)
            pixmap = QPixmap(imagePath)
            self.two.label_14.setPixmap(pixmap)


    def on_toolButton10_clicked(self):
        imagePath = self.two.lineEdit.text()
        print(imagePath)
        processor = OCRProcessor()
        self.two.textEdit.setText(processor.process_image(imagePath))

#提交反馈
    def sql_insert(self,message):
        # 1.链接数据库
        conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='520520hxa', charset='utf8',
                               db='zhuochong2333')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        # 2.发送指令
        current_time = datetime.datetime.now()
        ctime = str(current_time.year)+"/"+str(current_time.month)+"/"+str(current_time.day)+"//"+str(current_time.hour)+"/"+str(current_time.minute)
        sql = "insert into reflect(message,time) values(%s,%s)"  # 将我们用户前端输入的内容放到我们的数据库中保存下来的指令，其中%s就是字符串的代替形式，学习python后就有更深刻理解
        cursor.execute(sql, [message, ctime])  # 将用户输入信息放到数据库中
        conn.commit()

        # 3.关闭链接
        cursor.close()
        conn.close()

        return '反馈成功'

    def on_toolButton11_clicked(self):
        text_content = self.two.textEdit_3.toPlainText() #反馈提交内容
        print(type(text_content))
        #写入数据库
        self.sql_insert(text_content)
        QtWidgets.QMessageBox.warning(self, "提示", "反馈成功！")
        self.two.textEdit_3.setText("")

        #print(text_content)

#获得用户ip
    def get_local_ip(self):
        return socket.gethostbyname(socket.gethostname())
    def on_toolButton12_clicked(self):
        font = QFont()
        font.setPointSize(16)
        my_ip = self.get_local_ip()
        self.two.textBrowser_2.setFont(font)
        self.two.textBrowser_2.setText(my_ip)


#选择文件
    def on_pushButton_clicked(self):
        filePath, _  = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*);;")
        if filePath:
            self.two.pushButton.setText(filePath)


#发送文件
    def on_toolButton13_clicked(self):
        fileSender = FileSender()
        ip = self.two.lineEdit_2.text()
        filepath = self.two.pushButton.text()

        fileSender.server_host = ip
        fileSender.file_path = filepath
        yes = fileSender.send_file()
        msg_box = QtWidgets.QMessageBox()
        # 设置消息框的标题和文本内容
        msg_box.setWindowTitle("桌宠介绍")
        msg_box.setText(yes)
        msg_box.setFixedSize(500, 300)
        msg_box.exec_()

#接收路径
    def on_pushButton2_clicked(self):
        filePath = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if filePath:
            self.two.pushButton_2.setText(filePath)

#开启接收模式
    # def on_toolButton14_clicked(self):
    #     fileReceiver = threading.Thread(target=FileReceiver)
    #     fileReceiver.save_path = self.two.pushButton_2.text()
    #     font = QFont()
    #     font.setFamily("Arial")  # 设置字体
    #     font.setPointSize(35)
    #     self.two.textBrowser.setFont(font)
    #     txt = "Server listening on port" + str(fileReceiver.port)
    #     self.two.textBrowser.setText(txt)
    #     yes = fileReceiver.start_server()
    #
    #     self.two.textBrowser.setFont(font)
    #     self.two.textBrowser.setText(yes)
    def on_toolButton14_clicked(self):
        self.fileReceiver = FileReceiver()
        self.fileReceiver.save_path = self.two.pushButton_2.text()
        if self.count1%2==0:
            self.two.toolButton_14.setText("关闭服务器")
            if self.count== 0:
                self.count += 1
                txt = "Server listening on port" + str(self.fileReceiver.port)
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText(txt)
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()
                self.file_receiver_thread = threading.Thread(target=self.start_file_receiver)
                self.file_receiver_thread.start()

            self.count1+=1
        else :
            self.two.toolButton_14.setText("启动服务器")

        # 创建一个新线程来启动文件接收器

    def start_file_receiver(self):
        # 在单独的线程中执行文件接收器的启动方法
        yes = self.fileReceiver.start_server()
        msg_box = QtWidgets.QMessageBox()
        # 设置消息框的标题和文本内容
        msg_box.setWindowTitle("桌宠介绍")
        msg_box.setText("停止服务器")
        msg_box.setFixedSize(500, 300)
        msg_box.exec_()


#转换-文件路径
    def on_pushButton5_clicked(self):
        left = self.two.comboBox.currentText()

        if left=='pdf':
            filePath, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                      "PDF 文件 (*.pdf)")
            if filePath:
                self.two.pushButton_5.setText(filePath)
        elif left=='word':
            filePath, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                      "Word 文档 (*.docx *.doc)")
            if filePath:
                self.two.pushButton_5.setText(filePath)
        else:
            filePath, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                      "图像文件(*.jpg *.png *.bmp)")
            if filePath:
                self.two.pushButton_5.setText(filePath)
#转换-保存路径
    def on_pushButton4_clicked(self):
        filePath = QFileDialog.getExistingDirectory(self, "选择文件夹", "")
        if filePath:
            self.two.pushButton_4.setText(filePath)
#开始转换
    def on_toolButton15_clicked(self):
        left = self.two.comboBox.currentText()
        right = self.two.comboBox_2.currentText()
        base_file_path = self.two.pushButton_5.text()
        save_file_path = self.two.pushButton_4.text()
        fileConverter = FileConverter()
        if left =='pdf':
            if right =='pdf':
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("格式错误！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()
            elif right =='word':
                fileConverter.pdf2docx(base_file_path,save_file_path)
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("转换成功！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()

            elif right =='image':
                fileConverter.pdf2img(base_file_path,save_file_path)
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("转换成功！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()

        elif left=='word':
            if right == 'word':
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("格式错误！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()

            elif right == 'pdf':
                fileConverter.docx2pdf(base_file_path,save_file_path)
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("转换成功！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()

        elif left == 'image':
            if right =='image':
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("格式错误！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()

            elif right == 'pdf':
                fileConverter.img2pdf(base_file_path,save_file_path)
                msg_box = QtWidgets.QMessageBox()
                # 设置消息框的标题和文本内容
                msg_box.setWindowTitle("桌宠介绍")
                msg_box.setText("转换成功！")
                msg_box.setFixedSize(500, 300)
                msg_box.exec_()

#翻译
    def on_toolButton18_clicked(self):
        dic = {"中文":'zh',"英语":'en',"日语":'jp'}
        left = self.two.comboBox_3.currentText()
        right = self.two.comboBox_4.currentText()
        if left not in dic.keys() or right not in dic.keys():
            QtWidgets.QMessageBox.warning(self, "提示", "格式错误！")
        else:
            left = dic[left]
            right = dic[right]
            original = self.two.textEdit_2.toPlainText()
            translator = BaiduTranslator('20240222001970292', 'uCBTLM_IlM9hf916fA2r')
            translation = translator.translate_text(original,left,right)
            self.two.textBrowser_5.setText("".join(translation))

    def on_pushButton3_clicked(self):
        text1 = self.two.comboBox_3.currentText()
        text2 = self.two.comboBox_4.currentText()
        self.two.comboBox_3.setCurrentText(text2)
        self.two.comboBox_4.setCurrentText(text1)

    def on_toolButton19_clicked(self):
        question = self.two.textEdit_5.toPlainText()
        self.two.textEdit_5.clear()
        self.two.label_11.clear()
        self.two.textEdit_4.append("输入:"+question+'\n')
        txt = "限制在100字以内回答问题："+question
        from main import wenxin
        self.two.textEdit_4.append("回答：")
        for answer in wenxin(txt):
            self.two.textEdit_4.append(answer)
        self.two.textEdit_4.append("\n------------------------------------------------------------\n")



#页面关闭
    def closeEvent(self, event):
         event.ignore()  # 忽略默认的关闭事件
         self.hide()  # 隐藏当前窗口，而不是关闭


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
