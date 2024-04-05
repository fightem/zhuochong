import sys
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QApplication, QGroupBox, QScrollArea, QPushButton, QFontDialog
)

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSettings
from multiprocessing import Process
import pyttsx3
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QHBoxLayout
import pickle
import json

# 语音朗读函数，将在单独的进程中运行
def speak(text):
    print('**********************************')
    print('**********************************')
    print('**********************************')
    print('**********************************')
    print('**********************************')
    print('**********************************')
    print('**********************************')
    print('**********************************')

    # engine = pyttsx3.init()
    # engine.say(text)
    # engine.runAndWait()
    from RumiaPet_main.TTS_bachongshenzi import tts_and_play
    for i in text:
        print(i)
        tts_and_play(i)

class NewsWindow(QWidget):
    should_continue = True

    def __init__(self):
        super(NewsWindow, self).__init__()
        self.setWindowTitle("新闻信息")

        self.setWindowIcon(QIcon('./RumiaPet_main/data/rumia/icon.png'))
        self.setGeometry(100, 100, 800, 600)

        # 创建垂直布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 初始化主标题
        self.main_title_label = QLabel("最新新闻", self)
        self.main_title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.main_title_label)

        # 创建滚动区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # 创建内部容器
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        layout.addWidget(self.scroll_area)

        # 添加朗读按钮
        self.read_button = QPushButton("朗读新闻", self)
        self.read_button.clicked.connect(self.read_news)
        layout.addWidget(self.read_button)

        # 添加停止朗读按钮
        self.stop_button = QPushButton("停止朗读", self)
        self.stop_button.clicked.connect(self.stop_reading)
        layout.addWidget(self.stop_button)

        # 添加字体设置按钮
        self.font_button = QPushButton("设置字体", self)
        self.font_button.clicked.connect(self.set_font)
        layout.addWidget(self.font_button)

        # 初始化字体
        self.title_font = QFont("Arial", 16, QFont.Bold)
        self.content_font = QFont("Arial", 14)



        try:
            # 从文本文件中加载字体
            with open('font.txt', 'r') as f:
                lines = f.readlines()
                family = lines[0].split(': ')[1].strip()
                size = int(lines[1].split(': ')[1].strip())
                bold = lines[2].split(': ')[1].strip() == 'True'
                italic = lines[3].split(': ')[1].strip() == 'True'
                font = QFont(family, size)
                font.setBold(bold)
                font.setItalic(italic)
                # 更新标题和内容字体
                self.title_font = QFont(font.family(), font.pointSize() + 2, QFont.Bold)
                self.content_font = QFont(font.family(), font.pointSize())
        except FileNotFoundError:
            font = self.content_font
            with open('font.txt', 'w') as f:
                f.write(f"Family: {font.family()}\n")
                f.write(f"Size: {font.pointSize()}\n")
                f.write(f"Bold: {font.bold()}\n")
                f.write(f"Italic: {font.italic()}\n")

        # 用于跟踪语音进程的变量
        self.voice_process = None

        # 让新闻页面显示在屏幕中央
        desktop_rect = QApplication.desktop().availableGeometry()
        self.move(desktop_rect.center() - self.rect().center())



    def set_font(self):
        # 打开字体对话框
        font, ok = QFontDialog.getFont()
        if ok:
            # 更新标题和内容字体
            self.title_font = QFont(font.family(), font.pointSize() + 2, QFont.Bold)
            self.content_font = QFont(font.family(), font.pointSize())
            # 存储选择的字体, 保存字体到文件
            with open('font.txt', 'w') as f:
                f.write(f"Family: {font.family()}\n")
                f.write(f"Size: {font.pointSize()}\n")
                f.write(f"Bold: {font.bold()}\n")
                f.write(f"Italic: {font.italic()}\n")

            # 更新现有新闻内容的字体
            self.update_news_content(self.news_list)

    def open_url(self, url):
        # 打开超链接对应的网页
        QDesktopServices.openUrl(QUrl(url))


    def update_news_content(self, news_list):
        # 清空当前新闻内容，然后添加新的新闻
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # 添加新的新闻内容到内部容器中
        for i, news in enumerate(news_list):
            group_box = QGroupBox(f"新闻 {i + 1}", self)
            group_layout = QVBoxLayout()
            group_box.setLayout(group_layout)
            # 创建水平布局用于放置标题和超链接按钮
            title_layout = QHBoxLayout()

            title_label = QLabel(news['title'], self)
            title_label.setFont(self.title_font) # 设置标题的字体
            title_layout.addWidget(title_label, stretch=7)  # 将标题部分设为占据 70% 的宽度


            # 添加超链接按钮
            link_button = QPushButton("阅读原文", self)
            link_button.setFlat(True)  # 将按钮设置为扁平风格，去掉边框
            link_button.setStyleSheet("color: blue; text-decoration: underline;")  # 设置超链接样式
            link_button.clicked.connect(lambda checked, url=news['href']: self.open_url(url))  # 绑定点击事件
            title_layout.addWidget(link_button, stretch=2)
            group_layout.addLayout(title_layout)




            # 创建一个展开/折叠内容的按钮
            toggle_button = QPushButton("更多...")
            toggle_button.setCheckable(True)  # 让按钮可以被选中
            toggle_button.toggled.connect(lambda checked, index=i: self.toggle_content(checked, index))
            group_layout.addWidget(toggle_button)

            # 创建内容标签，但默认隐藏
            description_label = QLabel(news['content'], self)
            description_label.setFont(self.content_font) # 设置内容的字体
            description_label.setWordWrap(True)
            description_label.setVisible(False)  # 默认隐藏内容
            group_layout.addWidget(description_label)

            self.scroll_layout.addWidget(group_box)

            # 保存内容标签、按钮和超链接按钮的引用，以便稍后使用
            news['description_label'] = description_label
            news['toggle_button'] = toggle_button
            news['link_button'] = link_button  # 添加超链接按钮的引用

        # 保存新闻列表，以便更新内容时使用
        self.news_list = news_list

    def toggle_content(self, checked, index):
        # 根据按钮的状态展开或折叠内容
        description_label = self.news_list[index]['description_label']
        toggle_button = self.news_list[index]['toggle_button']
        if checked:
            description_label.setVisible(True)
            toggle_button.setText("收起")
        else:
            description_label.setVisible(False)
            toggle_button.setText("更多...")

    def read_news(self):
        # 拼接新闻标题和描述，并将其添加到朗读内容中
        news_texts = []
        for i, news in enumerate(self.news_list):
            print("*"*50)
            print("\n")
            print(news)

            title = news['id']
            title_content = news['title']
            description = news['content']

            # print("title" + title)
            # print("title_content" + title_content)
            # print("description" + description)

            news_texts.append(f"新闻 {title}. {title_content} .{description}.")
        # full_text = ' '.join(news_texts)
        # print(news_texts)

        # 如果语音进程正在运行，先终止它
        if self.voice_process and self.voice_process.is_alive():
            self.voice_process.terminate()
            self.voice_process.join()

        # 启动新的语音朗读进程
        self.voice_process = Process(target=speak, args=(news_texts,))
        self.voice_process.start()

    def stop_reading(self):
        # 如果语音进程正在运行，终止它
        if self.voice_process and self.voice_process.is_alive():
            self.voice_process.terminate()
            self.voice_process.join()

    def closeEvent(self, event):
        NewsWindow.should_continue = False # 设置标志为False表示需要停止循环
        # 如果语音进程正在运行，终止它
        if self.voice_process and self.voice_process.is_alive():
            self.voice_process.terminate()
            self.voice_process.join()

        event.ignore()  # 忽略默认的关闭事件
        self.hide()  # 隐藏窗口，不关闭

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(Qt.OpenHandCursor)  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(Qt.ArrowCursor)

if __name__ == '__main__':
    from xinwen import guancha
    url = "https://m.guancha.cn/internation"
    list1 = guancha.get_news_list(url)
    print(list1)
    app = QApplication(sys.argv)
    news_window = NewsWindow()
    news_window.update_news_content(list1)
    news_window.show()

    sys.exit(app.exec_())
