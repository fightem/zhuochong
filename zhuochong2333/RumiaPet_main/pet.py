import random
import csv,webbrowser

from setting import *
from config import  ConfigGetter
from scheduleUI import TodoApp
from components.bubble import *

import os
from TTS_bachongshenzi import tts_and_play
from VoiceSettingUI import get_latest_pet_sound

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGroupBox
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication

import requests
import pyttsx3
import time
from work_place.SmartDeskPet import RandomReminder
from work_place.SmartDeskPet.RandomReminder import ExpressionReminder
# 跳转右键菜单
# self.lb1.customContextMenuRequested.connect(self.rightMenu)

class Worker(QObject):
    finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.txt =""

    def do_work(self):
        # 模拟耗时任务
        # 在实际应用中，这里可以是你的tip_sentiment函数
        message = RandomReminder.Sentiment_pet()
        self.txt = f"{message}"
        self.finished.emit()


class App(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(App, self).__init__(parent)
        self.cout=0
        # self.label_hello = QLabel(self)
        # self.label_hello.setText('你好世界')
        # self.label_hello.setGeometry(1, 1, 400, 100)  # 调整标签位置和大小
        # self.label_hello.setFont(QFont('Arial', 16))  # 设置标签的字体和大小
        # self.label_hello.setStyleSheet("color: white;")  # 设置标签文字颜色为白色
        # self.label_hello.move(-1, -35)  # 设置标签在主窗口上方的位置，这里假设离顶部20px
        from zhuochong2333.RumiaPet_main.TTS_bachongshenzi import tts_and_play
        tts_and_play('主人，露米娅启动')
        from pet_box import CustomDialog
        self.dialogs = CustomDialog()

        # QTimer for updating the CustomDialog position
        self.dialog_position_timer = QTimer(self)
        self.dialog_position_timer.timeout.connect(self.update_dialog_position)
        self.dialog_position_timer.start(100)  # Update every 100 milliseconds

        self.dialogs.show()
        self.dialogs.hide()

        # 增加天气和情绪识别的随机生成
        # self.Timer = QTimer(self)
        # self.Timer.start(150000)
        #self.Timer.timeout.connect(self.tip_sentiment)

        self.worker_thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.Timer = QTimer(self)
        self.Timer.start(10000000)
        self.Timer.timeout.connect(self.worker.do_work)
        self.Timer.timeout.connect(self.tip_sentiment)
        self.worker.finished.connect(self.update_label)





        # 清除文字的内容
        self.clear_timer = QTimer(self)
        self.clear_timer.setSingleShot(True)  # Only trigger once
        self.clear_timer.timeout.connect(self.clear_label_text)

        # self.Timer2 = QTimer(self)
        # self.Timer2.start(10000)
        # self.Timer2.timeout.connect(self.tip_weather)

        # initialize
        self.is_follow_mouse = False
        self.settingMenu = None

        # Windows
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)

        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.repaint()

        screen = QDesktopWidget().screenGeometry()
        desktop = QDesktopWidget().availableGeometry()
        self.tray()

        cfg = ConfigGetter()

        cfg.screenwidth = screen.width()
        cfg.screenheight = screen.height()
        cfg.deskwidth = desktop.width()
        cfg.deskheight = desktop.height()
        cfg.gameleft = cfg.screenwidth - cfg.deskwidth
        cfg.gamebottom = cfg.screenheight - cfg.deskheight

        if cfg.intotray != "True":
            cfg.petleft = cfg.deskwidth - cfg.petwidth * cfg.petscale
            cfg.pettop = cfg.deskheight - cfg.petheight * cfg.petscale - cfg.bottomfix
        else:
            cfg.gameleft = 0
            cfg.gamebottom = 0
            cfg.petleft = cfg.screenwidth - cfg.petwidth * cfg.petscale
            cfg.pettop = cfg.screenheight - cfg.petheight * cfg.petscale - cfg.bottomfix

        # initial image
        petimage = cfg.image_url + 'start.png'
        # print(petimage)
        pix = QPixmap(petimage)
        pix = pix.scaled(int(cfg.petwidth * cfg.petscale),
                         int(cfg.petheight * cfg.petscale),
                         aspectRatioMode=Qt.KeepAspectRatio)
        self.lb1 = QLabel(self)
        self.lb1.setPixmap(pix)
        self.lb1.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lb1.customContextMenuRequested.connect(self.rightMenu)

        # display first pic
        cfg.petleft = int(cfg.petleft)
        cfg.pettop = int(cfg.pettop)
        self.move(cfg.petleft, cfg.pettop)
        self.resize(int(cfg.petwidth * cfg.petscale),
                    int(cfg.petheight * cfg.petscale))
        self.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game)
        self.timer.start(cfg.gamespeed)

    def Sentiment_pet(self):
        e = ExpressionReminder()
        expression = e.generateRemind()
        return expression

    def update_label(self):

        #message = self.Sentiment_pet
        #print(message)
        list1 = ["主人,写作业时间快到了,不要忘记了哟ヾ(･∀･`)", "主人，今天天气不错。你可以出去看看!","ヾ(･∀･`)有什么开心的事吗！, ヾ(･∀･`)很开心喵！","主人，有什么有趣的事情分享吗"]
        message = list1[random.randint(0,4)]



        #显示在桌宠头上
        self.dialogs.changeDialog(message)
        self.dialogs.show()
        self.clear_timer.start(5000)  # 文字展示5s后自动消失

        #self.label.setText("任务完成")

    def closeEvent(self, event):
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()

    def update_dialog_position(self):
        # Calculate the position for the CustomDialog relative to the App window
        dialog_x = self.x() + self.width() - self.dialogs.width() + 280
        dialog_y = self.y() - 190
        self.dialogs.move(dialog_x, dialog_y)

    def showEvent(self, event):
        super().showEvent(event)
        self.update_dialog_position()  # Update dialog

    def tip_sentiment(self):
        # print('Performing sentiment analysis...')

        message = self.worker.txt
        # self.label_hello.setText(message)
        # print('*****************')
        print(message)

    def clear_label_text(self):
        self.dialogs.hide()
        # self.label_hello.clear()  # Clear text after 5 seconds
        self.dialogs.changeDialog('')

    # def tip_weather(self):
    #
    #     message = RandomReminder.Weather_pet()
    #     # self.label_hello.setText(message)
    #     self.dialogs.show()
    #     self.dialogs.changeDialog(message)
    #     print(message)

    def game(self):
        '''
        主循环，核心功能为：寻找合适图片，寻找合适位置，放置图片
        :return:
        '''
        right=0
        cfg = ConfigGetter()

        if cfg.intotray != "True":
            cfg.gamebottom = cfg.screenheight-cfg.deskheight
        else:
            cfg.gamebottom = 0

        #handle quit
        if cfg.quit == 1:
            if cfg.playid<=cfg.quitactionnum:
                cfg.imgpath = 'quit' + str(cfg.playid) + '.png'
                cfg.playid+=1
            else:
                #final
                self.quit()
        elif cfg.hiding == 1:
            if cfg.playid<=cfg.quitactionnum:
                cfg.imgpath = 'quit' + str(cfg.playid) + '.png'
                cfg.playid+=1
            else:
                #final
                self.hide()


        # handle drag and fall
        elif cfg.drop==1 and cfg.onfloor==0 :
            if cfg.draging==1:
                #print("Draging")
                cfg.playnum=int(cfg.petactionnum[3])
                if cfg.playid<int(cfg.petactionnum[3]):
                        cfg.imgpath=cfg.petactions[3]+str(cfg.playid)+'.png'
                        cfg.playid+=1
                else:
                    #final action
                    cfg.imgpath=cfg.petactions[3]+str(cfg.playid)+'.png'
                    cfg.playid=1

            elif cfg.draging==0:
                #falling
                cfg.playnum=int(cfg.petactionnum[4])
                if cfg.playid<int(cfg.petactionnum[4]):
                        cfg.imgpath=cfg.petactions[4]+str(cfg.playid)+'.png'
                        cfg.playid += 1
                else:
                    cfg.imgpath=cfg.petactions[4]+str(cfg.playid)+'.png'
                    cfg.playid=1

            self.drop()



        # handle standing
        elif cfg.drop==0 or cfg.onfloor==1:

            if cfg.playtime==0:
                cfg.petaction=random.random()
                cfg.playstand=-1
                cfg.playid=1

            if cfg.petaction>=(float(cfg.petactionrate[0])+float(cfg.petactionrate[1])) \
                    and (cfg.petleft+cfg.petwidth*cfg.petscale+cfg.gameleft+cfg.petspeed)<cfg.deskwidth:
                ##print("Walking right")
                right=1
                cfg.playnum=int(cfg.petactionnum[2])
                if cfg.playid<int(cfg.petactionnum[2]):
                    cfg.imgpath=cfg.petactions[2]+str(cfg.playid)+'.png'
                    cfg.playid+=1

                else:
                    cfg.imgpath=cfg.petactions[2]+str(cfg.playid)+'.png'
                    cfg.playid=1


                cfg.petleft=cfg.petleft+cfg.petspeed
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)

                if cfg.playtime==0:
                    playtimemin=3
                    playtimemax=int((((cfg.deskwidth-
                                (cfg.petleft+cfg.petwidth*cfg.petscale+cfg.gameleft)
                                       ))/cfg.petspeed)/cfg.playnum)
                    if playtimemax<=3:
                        playtimemax=3
                cfg.playtime -= 1


            elif cfg.petaction<(float(cfg.petactionrate[0])+float(cfg.petactionrate[1])) \
                    and cfg.petaction>=float(cfg.petactionrate[0]) and (cfg.petleft-cfg.gameleft)>cfg.petspeed:
                cfg.playnum=int(cfg.petactionnum[1])
                if cfg.playid<int(cfg.petactionnum[1]):
                    cfg.imgpath=cfg.petactions[1]+str(cfg.playid)+'.png'
                    cfg.playid+=1

                else:
                    cfg.imgpath=cfg.petactions[1]+str(cfg.playid)+'.png'
                    cfg.playid=1

                cfg.petleft=cfg.petleft-cfg.petspeed
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)

                if cfg.playtime==0:
                    playtimemin=3
                    playtimemax=int((cfg.petleft-cfg.gameleft)
                                    /cfg.petspeed/cfg.playnum)
                    if playtimemax<=1:
                        playtimemax=1
                cfg.playtime=int(cfg.playtime)-1


            elif cfg.petaction<float(cfg.petactionrate[0]):
                # 站立循环

                if cfg.playstand==-1:
                    temp=random.random()
                    temp2=0

                    for i in range(len(cfg.standactionrate)):

                        if float(cfg.standactionrate[i])==0:
                            continue
                        temp2 = temp2+float(cfg.standactionrate[i])
                        ##print("内循环："+str(i)+"cfg.累计概率："+str(temp2))
                        if temp<temp2:
                            cfg.petaction2=i
                            cfg.playnum=int(cfg.standactionnum[i])
                            cfg.playstand=1

                            break

                    if cfg.playstand==-1:
                        cfg.playnum=int(cfg.standactionnum[0])
                        cfg.playstand=1


                if cfg.playstand<int(cfg.standactionnum[cfg.petaction2]):
                    #imgpath=standaction[i]+str(playid)+'.png'
                    cfg.imgpath=cfg.standaction[cfg.petaction2]+str(cfg.playstand)+'.png'
                    cfg.playstand+=1
                else:
                    cfg.imgpath=cfg.standaction[cfg.petaction2]+str(cfg.playstand)+'.png'
                    cfg.playstand=1
                    cfg.playid=1

                if cfg.playtime==0:
                    playtimemin=1
                    playtimemax=1

                cfg.playtime=int(cfg.playtime)-1



            else:
                cfg.petaction=random.random()
                cfg.playstand=-1

            if cfg.playtime==-1:
                cfg.playtime=random.randint(1,playtimemax)*cfg.playnum


        cfg.petimage = cfg.image_url + cfg.imgpath
        print(cfg.petimage)
        #petimage=petimage.mirrored(True, False)
        pix = QPixmap(cfg.petimage)
        if right==1:
            tempimg = pix.toImage()
            tempimg = tempimg.mirrored(True, False)
            pix=QPixmap.fromImage(tempimg)

        pix=pix.scaled(int(cfg.petwidth*cfg.petscale),
                       int(cfg.petheight*cfg.petscale),
                       aspectRatioMode=Qt.KeepAspectRatio)
        if cfg.ischangescale == 1 :
            self.resize(int(cfg.petwidth*cfg.petscale),
                           int(cfg.petheight*cfg.petscale))
            self.lb1.setGeometry(0,0,
                                 int(cfg.petwidth*cfg.petscale),
                                 int(cfg.petheight*cfg.petscale))
            cfg.ischangescale=0
        self.lb1.setPixmap(pix)

        pass

    def rightMenu(self):
        '''
        设置露米娅右击菜单内容
        :return:
        '''
        cfg = ConfigGetter()

        menu = QMenu(self)

        # 宠物状态菜单

        state_menu = QMenu('宠物状态')  # 设置菜单标题
        state_menu.setIcon(QIcon('./data/icon/deviceon.png'))
        #         state_menu = QMenu(QIcon('./data/icon/deviceon.png'), '宠物状态', self)
        state_menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        state_menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))
        state_menu.addAction(
            QAction(QIcon('./data/icon/eye_protection.png'), '隐藏', self, triggered=self.playHide))

        state_menu.addSeparator()

        menu.addMenu(state_menu)

        # menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        # menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))
        # menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'), '隐藏', self, triggered=self.playHide))
        # menu.addSeparator()

        # 宠物设置菜单
        settingMenu = QMenu('settingMenu')
        settingMenu.setTitle('宠物设置')
        settingMenu.setIcon(QIcon('./data/icon/settings.png'))
        settingMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '宠物形态设置', self, triggered=self.petSetting))
        settingMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '网站收藏管理', self, triggered=self.webSetting))
        settingMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '宠物语音设置', self, triggered=self.voiceSetting))
        menu.addMenu(settingMenu)

        menu.addAction(QAction(QIcon('./data/icon/schedule.png'), '办公助手', self, triggered=self.bangong))
        menu.addSeparator()

        # 记录模块菜单
        recordMenu = QMenu('记录模块')
        recordMenu.setTitle('记录模块')
        recordMenu.setIcon(QIcon('./data/icon/schedule.png'))
        recordMenu.addAction(QAction(QIcon('./data/icon/schedule.png'), '日程表', self, triggered=self.schedule))
        webData = self.readCsv(cfg.webDataPath)
        for name, xurl in webData:
            recordMenu.addAction(
                QAction(name, self, triggered=(lambda _, url=xurl: webbrowser.open(url)))
            )
        menu.addMenu(recordMenu)

        # 今日实况模块
        today_menu = QMenu('今日实况')
        today_menu.setTitle('今日实况')
        today_menu.setIcon(QIcon('./data/icon/search.png'))
        # 新闻模块
        newsMenu = QMenu('新闻')
        newsMenu.setTitle('新闻')
        newsMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '观察者网', self, triggered=self.news_guancha))
        newsMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '澎湃新闻', self, triggered=self.news_pengpai))
        newsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '今日头条', self, triggered=self.news_jinri))
        newsMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '中央国际新闻', self, triggered=self.news_zhongyang))
        newsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '网易新闻', self, triggered=self.news_wangyi))
        newsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '微博', self, triggered=self.news_weibo))
        today_menu.addMenu(newsMenu)

        # 天气模块
        today_menu.addAction(
            QAction(QIcon('./data/icon/eye_protection.png'), '天气情况', self, triggered=self.weather))

        menu.addMenu(today_menu)
        menu.addSeparator()

        # 娱乐模块
        funMenu = QMenu('funMenu')
        funMenu.setTitle('娱乐')
        funMenu.setIcon(QIcon('./data/icon/collection.png'))
        funMenu.addAction(
            QAction(QIcon('./data/icon/settings.png'), '音乐播放', self, triggered=self.music))
        funMenu.addAction(
            QAction(QIcon('./data/icon/deviceon.png'), '语音对话', self, triggered=self.chat)
        )
        menu.addMenu(funMenu)

        # menu.addAction(QAction(QIcon('./data/icon/schedule.png'), '办公助手', self, triggered=self.bangong))
        menu.addSeparator()

        # webMenu = QMenu('webMenu')
        # webMenu.setTitle('收藏的网站')
        # webData = self.readCsv(cfg.webDataPath)
        # for name, url in webData:
        #     webMenu.addAction(
        #         QAction(name, self, triggered=(lambda _, url=url: webbrowser.open(url)))
        #     )
        # menu.addMenu(webMenu)
        # menu.addSeparator()
        #
        # menu.addAction(QAction(QIcon('./data/icon/schedule.png'), '办公助手', self, triggered=self.bangong))
        # menu.addAction(QAction(QIcon('./data/icon/schedule.png'), '日程表', self, triggered=self.schedule))
        # menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '翻译功能', self, triggered=self.translate))

        # menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '文件传输', self, triggered=self.translate))
        menu.addSeparator()

        # menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'), '音乐播放', self, triggered=self.music))
        # menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'), '天气情况', self, triggered=self.weather))

        # NewsMenu = QMenu('NewsMenu')
        # NewsMenu.setTitle('新闻')
        # NewsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '观察者网', self, triggered=self.news_guancha))
        # NewsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '澎湃新闻', self, triggered=self.news_pengpai))
        # NewsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '今日头条', self, triggered=self.news_jinri))
        # NewsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '中央国际新闻', self, triggered=self.news_zhongyang))
        # NewsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '网易新闻', self, triggered=self.news_wangyi))
        # NewsMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '微博', self, triggered=self.news_weibo))
        # menu.addMenu(NewsMenu)

        menu.addSeparator()
        menu.addAction(QAction(QIcon('./data/icon/close.png'), '退出', self, triggered=self.playQuit))

        menu.exec_(QCursor.pos())
    def readCsv(self,filePath: str):
        '''
        读取对应filePath的csv文件并返回内容数组
        :param filePath: 文件路径
        :return: 一般为二维数组
        '''
        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                file.close()
                pass
        with open(filePath, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)

    def writeCsv(filePath: str, data: list):
        '''
        将数组写入csv文件
        :param data: 要写入的二维数组
        :return:
        '''
        # 数据准备
        # data = [
        #     ['哔哩哔哩', 'www.bilibili.com'],

        # ]

        # 打开CSV文件进行写入
        with open(filePath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)

    def mousePressEvent(self, event):
        cfg = ConfigGetter()
        if event.button()==Qt.LeftButton:
            self.is_follow_mouse = True
            cfg.onfloor=0
            cfg.draging=1
            if cfg.quit != 1:
                # means new action
                cfg.playid=1
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        cfg = ConfigGetter()

        if Qt.LeftButton and self.is_follow_mouse:
            cfg.petleft = QCursor.pos().x()-cfg.petwidth*cfg.petscale/2+cfg.dragingfixx*cfg.petscale
            cfg.pettop = QCursor.pos().y()-cfg.petheight*cfg.petscale/2+cfg.dragingfixy*cfg.petscale

            cfg.mouseposx4=cfg.mouseposx3
            cfg.mouseposx3=cfg.mouseposx2
            cfg.mouseposx2=cfg.mouseposx1
            cfg.mouseposx1=QCursor.pos().x()

            cfg.mouseposy4=cfg.mouseposy3
            cfg.mouseposy3=cfg.mouseposy2
            cfg.mouseposy2=cfg.mouseposy1
            cfg.mouseposy1=QCursor.pos().y()

            cfg.petleft = int(cfg.petleft)
            cfg.pettop = int(cfg.pettop)
            self.move(cfg.petleft, cfg.pettop)
            event.accept()

    def mouseReleaseEvent(self, event):
        cfg = ConfigGetter()
        if event.button()==Qt.LeftButton:
            if cfg.quit != 1:
                cfg.playid=1
            cfg.onfloor=0
            cfg.draging=0
            self.is_follow_mouse = False
            self.setCursor(QCursor(Qt.ArrowCursor))
            cfg.dropa=1
            cfg.dragspeedx=(cfg.mouseposx1-cfg.mouseposx3)/2*cfg.fixdragspeedx
            cfg.dragspeedy=(cfg.mouseposy1-cfg.mouseposy3)/2*cfg.fixdragspeedy
            cfg.mouseposx1=cfg.mouseposx3=0
            cfg.mouseposy1=cfg.mouseposy3=0
            ##print("mouseReleaseEvent")

    def tray(self):
        '''
        任务栏小图标相关，隐藏后的右键菜单
        :return:
        '''
        cfg = ConfigGetter()
        tray = QSystemTrayIcon(self)
        tray.setIcon(QIcon(cfg.traypath))
        menu = QMenu(self)

        menu.addAction(QAction(QIcon('./data/icon/eye_protection.png'),'显示', self, triggered=self.show))
        menu.addAction(QAction(QIcon('./data/icon/visible.png'), '隐藏', self, triggered=self.playHide))
        menu.addAction(QAction(QIcon('./data/icon/deviceon.png'), '开启掉落', self, triggered=self.dropon))
        menu.addAction(QAction(QIcon('./data/icon/deviceoff.png'), '禁用掉落', self, triggered=self.dropoff))
        menu.addSeparator()

        settingMenu = QMenu('settingMenu', self)
        settingMenu.setTitle('设置')
        settingMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '宠物设置', self, triggered=self.petSetting))
        settingMenu.addAction(QAction(QIcon('./data/icon/settings.png'), '网站收藏管理', self, triggered=self.webSetting))



        menu.addMenu(settingMenu)
        menu.addSeparator()
        menu.addAction(QAction(QIcon('./data/icon/close.png'), '退出', self, triggered=self.playQuit))

        tray.setContextMenu(menu)
        tray.show()


    def schedule(self):
        self.scheduleWindow = TodoApp()
        self.scheduleWindow.show()

    def bangong(self):
        from ui_main import AnotherWindow
        self.scheduleWindow = AnotherWindow()
        self.scheduleWindow.show()


    def petSetting(self):
        '''
        打开宠物设置菜单
        :return:
        '''
        self.settingMenu = PetSetting()
        # self.settingMenu.isChange = False
        self.settingMenu.show()
    def webSetting(self):
        '''
        打开网站设置菜单
        :return:
        '''
        self.settingMenu = WebSetting()
        self.settingMenu.show()


    def voiceSetting(self):
        from VoiceSettingUI import PetSoundSettings
        self.voiceset = PetSoundSettings()
        self.voiceset.show()


    def drop(self):
        '''
        用于处理露米娅掉落时的逻辑
        :return:
        '''
        #掉落
        cfg = ConfigGetter()

        # print("Dropping")
        if cfg.onfloor==0 and cfg.draging==0:
            dropnext=cfg.pettop+cfg.dragspeedy+cfg.dropspeed
            movenext=cfg.petleft+cfg.dragspeedx
            if cfg.throwout!="True":
                if movenext<=cfg.gameleft:
                    movenext=cfg.gameleft
                elif movenext>cfg.screenwidth-cfg.petwidth*cfg.petscale:
                    movenext=(cfg.screenwidth-cfg.petwidth*cfg.petscale)

            cfg.dragspeedy=cfg.dragspeedy+cfg.gravity



            # on floor
            if dropnext>=(cfg.screenheight-cfg.petheight*cfg.petscale
                          -cfg.gamebottom-cfg.bottomfix):
                cfg.pettop=cfg.screenheight-cfg.petheight*cfg.petscale-cfg.gamebottom-cfg.bottomfix
                cfg.petleft=movenext
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)
                cfg.onfloor=1
                cfg.dropa=0

            elif dropnext<(cfg.screenheight-cfg.petheight*cfg.petscale
                           -cfg.gamebottom-cfg.bottomfix):
                cfg.pettop=dropnext
                cfg.petleft=movenext
                cfg.petleft = int(cfg.petleft)
                cfg.pettop = int(cfg.pettop)
                self.move(cfg.petleft,cfg.pettop)

    def switchdrop(self):
        cfg = ConfigGetter()
        # global drop
        sender = self.sender()
        if sender.text() == "禁用掉落":
            sender.setText("开启掉落")
            cfg.drop=0
        else:
            sender.setText("禁用掉落")
            cfg.drop=1

    def dropon(self):
        cfg = ConfigGetter()
        # global drop
        cfg.drop=1

    def dropoff(self):
        cfg = ConfigGetter()
        # global drop
        cfg.drop=0
    #
    # def transfer(self):
    #     # from function_translate import TranslationWindow
    #     self.translation_window = TranslationWindow()
    #     self.translation_window.show()

    def translate(self):
        # from function_translate import TranslationWindow
        from fanyi_ui import TranslateWindow
        self.translation_window = TranslateWindow()
        self.translation_window.show()

    def display_schedule(instance, title, content):
        instance.schedule()  # 在新线程中调用self.schedule()函数
        speak(f"代办任务：{title}。内容：{content}")


    def chat(self):
        should_close = False  # 添加一个标志变量来控制退出循环
        from main import process_audio
        data = process_audio()
        print(data)
        weather_keywords = ["天气", "天气情况", "查看天气", "打开天气"]
        has_weather_intent = any(keyword in data for keyword in weather_keywords)
        list1 = file_get()
        website_keywords = ["打开", "浏览", "访问"]  # 添加打开网站类似的语言关键词

        todo_keywords = ["代办", "任务", "日程", "计划"]

        music_keywords = ["播放", "音乐", "一首音乐"]

        # 如果语音数据匹配到关键词，则实现播放任务清单列表
        if any(keyword in data for keyword in todo_keywords):
            list1 = file_get_schedule()
            id = 0
            for item in list1:
                id += 1
                msg = f'任务{id},{item["name"]},内容:{item["content"]}'
                print(msg)
                tts_and_play(text=msg)

            self.schedule()
            tts_and_play(text='主人，您的代办任务如上，工作的同时也要注意休息哦')
            # speak('主人，您的代办任务如上，工作的同时也要注意休息哦')
            # 如果语音数据包含特定内容，则调用neirong函数

        # 如果语音数据匹配到关键词，则调用天气窗口函数
        elif has_weather_intent:
            self.weather()

        # 如果语音数据匹配到关键词，则实现打开网站功能
        elif any(keyword in data for keyword in website_keywords):
            print(list1, data)
            for site in list1:
                if site['name'] in data:
                    print(site['name'], data)
                    url = site['href']
                    print(f"打开网站：{site['name']}，链接：{site['href']}")
                    webbrowser.open(url)
                    tts_and_play(text=f'好的主人，已为您打开{site["name"]}')
                    # speak(f'好的主人，已为您打开{site["name"]}')
                    return  # 打开网站后直接返回，不执行后续代码
            else:
                tts_and_play(text=f"主人，网站没有被收录，无法打开")
                # speak(f"主人，网站没有被收录，无法打开")
                return  # 网站未收录时直接返回，不执行后续代码

        # 如果语音数据匹配到关键词，则实现播放对应音乐的功能
        elif any(keyword in data for keyword in music_keywords):
            print('音乐播放')
            from music_player import MP3Player
            self.musics = MP3Player()
            id = 0
            music_list = self.musics.songs_list
            for i in music_list:
                msg = i[0].split('-')[1]
                msg2 = msg.strip(' ').split('.mp3')[0]
                if msg2 in data:
                    self.musics.musicList.setCurrentRow(id)
                    self.musics.setCurPlaying()
                    self.musics.playMusic()
                    self.musics.show()
                id += 1

            tts_and_play(text='主人，未找到您说的音乐，但为您打开了音乐播放器，您可以自行选择想要的音乐')
            # speak(f"主人，未找到您说的音乐，但为您打开了音乐播放器，您可以自行选择想要的音乐")
            return  # 网站未收录时直接返回，不执行后续代码
        # else:
        #     import json, time
        #     url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=e1adkIbaxkTYFNdUOeACBRP6&client_secret=UIlHoGkGHisD7dY3PKZScN1Zy234U21Y"
        #     payload = json.dumps("")
        #     headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        #     response = requests.request("POST", url, headers=headers, data=payload)
        #     tokens = response.json().get("access_token")
        #
        #     headers = {'Content-Type': 'application/json'}
        #     url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(
        #         tokens)
        #     payload = json.dumps({"messages": [{"role": "user", "content": f'{data}'}], "stream": True})
        #     response = requests.request("POST", url, headers=headers, data=payload, stream=True)
        #     from wen_xianshiUI import VoiceChatWindow
        #     self.wen = VoiceChatWindow()
        #
        #     for line in response.iter_lines():
        #         if not VoiceChatWindow.should_continue:  # 检查是否应该继续循环
        #             break  # 如果标志为False，则退出循环
        #
        #         if line:
        #             data = json.loads(line.decode("utf-8").replace("data: ", ""))
        #             msg = data["result"]
        #             print(msg)
        #             self.wen.set_text(msg)  # 更新窗口文本内容
        #             QApplication.processEvents()  # 更新UI
        #             self.wen.show()
        #
        #             while self.wen.is_voice_playing():
        #                 QApplication.processEvents()  # 这将允许UI响应事件，例如关闭按钮
        #                 time.sleep(0.1)  # 避免过度占用CPU
        #             # engine = pyttsx3.init()
        #             # engine.say(msg)
        #             #
        #             # engine.runAndWait()
        #
        #         self.game()
        else:
            print('被执行了')
            import json, time
            url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=e1adkIbaxkTYFNdUOeACBRP6&client_secret=UIlHoGkGHisD7dY3PKZScN1Zy234U21Y"
            payload = json.dumps("")
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload)
            tokens = response.json().get("access_token")

            headers = {'Content-Type': 'application/json'}
            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + str(
                tokens)
            payload = json.dumps({"messages": [{"role": "user", "content": f'{data}'}], "stream": True})
            response = requests.request("POST", url, headers=headers, data=payload, stream=True)
            from wen_xianshiUI import VoiceChatWindow
            self.voice_chat_window = VoiceChatWindow()  # 创建VoiceChatWindow实例
            for line in response.iter_lines():
                if not self.voice_chat_window.should_continue:
                    break

                if line:
                    data = json.loads(line.decode("utf-8").replace("data: ", ""))
                    msg = data["result"]
                    print(msg)
                    self.voice_chat_window.set_text(msg)
                    QApplication.processEvents()
                    self.voice_chat_window.show()

                    while self.voice_chat_window.is_voice_playing():
                        QApplication.processEvents()
                        time.sleep(0.1)

            # 这里可能需要根据具体情况调用某个方法或处理其他逻辑

    def news_guancha(self):
        url = "https://m.guancha.cn/internation"  # 观察者网
        from zhuochong2333.xinwen import guancha
        news_list = guancha.get_news_list(url)
        # for news in news_list:
        #     msg = "新闻"+str(news['id'])+str(news['title'])+str(news['content'])
        #     print(msg)
        #     tts_and_play(msg)

        from xinwen_UI import NewsWindow

        self.news = NewsWindow()
        self.news.update_news_content(news_list)  # 更新新闻内容
        self.news.show()

    def news_pengpai(self):
        url = "https://m.thepaper.cn/"  # 澎湃新闻
        from zhuochong2333.xinwen import pengpai
        news_list = pengpai.get_news_list(url)

        from xinwen_UI import NewsWindow

        self.news = NewsWindow()
        self.news.update_news_content(news_list)  # 更新新闻内容
        self.news.show()



    def news_jinri(self):
        url = "https://www.toutiao.com/"  # 今日头条
        from zhuochong2333.xinwen import jinri
        news_list = jinri.get_news_list(url)

        from xinwen_UI import NewsWindow

        self.news = NewsWindow()
        self.news.update_news_content(news_list)  # 更新新闻内容
        self.news.show()

    def news_zhongyang(self):
        url = "https://news.cctv.com/world/"  # 中央国际新闻
        from zhuochong2333.xinwen import zhongyang
        news_list = zhongyang.get_news_list(url)

        from xinwen_UI import NewsWindow

        self.news = NewsWindow()
        self.news.update_news_content(news_list)  # 更新新闻内容
        self.news.show()

    def news_weibo(self):
        pass

    def news_wangyi(self):
        url = "https://tophub.today/n/ENeYa4DeY4"  # 中央国际新闻
        from zhuochong2333.xinwen import wangyi
        news_list = wangyi.get_news_list(url)

        from xinwen_UI import NewsWindow

        self.news = NewsWindow()
        self.news.update_news_content(news_list)  # 更新新闻内容
        self.news.show()


    def music(self):
        from music_player import MP3Player
        self.musics = MP3Player()

        self.musics.show()
        self.musics.musicList.setCurrentRow(random.randint(0, 4))
        self.musics.setCurPlaying()
        # ex.playRandomMusic()
        self.musics.playMusic()

    def weather(self):
        # self.weather_window = QtWidgets.QApplication(sys.argv)


        from final_tianqi import weatherWindow
        self.weather_window = weatherWindow()
        self.weather_window.show()




    def playQuit(self):
        '''
        用于设置quit的flag，便于主循环接下来播放quit动画
        :return:
        '''
        cfg = ConfigGetter()
        cfg.quit = 1
        cfg.playid = 1

    def playHide(self):
        cfg = ConfigGetter()
        # quit优先级最高
        if cfg.quit == 1:
            return
        if cfg.hidden == 1:
            self.hide()
        cfg.hiding = 1
        cfg.playid = 1

    def hide(self):
        cfg = ConfigGetter()
        self.setVisible(False)
        self.bubble = BubbleWindow("./data/rumia/hideBubble.png", cfg.screenwidth*2//3, cfg.deskheight)
        self.bubble.show()
        cfg.hiding = 0
        cfg.hidden = 1

    def show(self):
        cfg = ConfigGetter()
        cfg.hidden = 0
        self.setVisible(True)

    # def restart_program(self):
    #     python = sys.executable
    #     os.execl(python, python, * sys.argv)

    def quit(self):
        self.close()
        sys.exit()


class VoiceThread(QThread):
    character_name = get_latest_pet_sound()
    print(f'当前声音{character_name}')
    finished = pyqtSignal()

    def __init__(self, msg):
        super(VoiceThread, self).__init__()
        self.msg = msg

    def run(self):
        character_name = get_latest_pet_sound()
        print(f'当前声音{character_name}')
        from TTS_bachongshenzi import tts_and_play
        tts_and_play(text=self.msg)





# 这个是我天气模块的窗口类
class WeatherWindow(QWidget):
    def __init__(self):
        super(WeatherWindow, self).__init__()
        self.setWindowTitle("Weather Information")
        self.setWindowIcon(QIcon('resource/image/weather_ico.png'))
        self.setGeometry(100, 100, 400, 300)

        # 获取天气信息
        weather_info = self.get_weather_info()

        # 创建垂直布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 城市信息
        city_label = QLabel(weather_info['city'], self)
        city_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(city_label)

        # 今天天气信息区域
        today_group = QGroupBox("今天天气", self)
        today_layout = QVBoxLayout()
        today_group.setLayout(today_layout)

        today_label = QLabel(weather_info['today'], self)
        today_layout.addWidget(today_label)

        today_notice_label = QLabel(weather_info['today_notice'], self)
        today_layout.addWidget(today_notice_label)

        layout.addWidget(today_group)

        # 明天天气信息区域
        tomorrow_group = QGroupBox("明天天气", self)
        tomorrow_layout = QVBoxLayout()
        tomorrow_group.setLayout(tomorrow_layout)

        tomorrow_label = QLabel(weather_info['tomorrow'], self)
        tomorrow_layout.addWidget(tomorrow_label)

        tomorrow_notice_label = QLabel(weather_info['tomorrow_notice'], self)
        tomorrow_layout.addWidget(tomorrow_notice_label)

        layout.addWidget(tomorrow_group)

        # 让天气页面显示在屏幕中央
        desktop_rect = QApplication.desktop().availableGeometry()
        self.move(desktop_rect.center() - self.rect().center())

        # 启动语音播报线程
        msg = f"今天天气：{weather_info['today']}。主人：{weather_info['today_notice']}"

        self.voice_thread = VoiceThread(msg)
        self.voice_thread.finished.connect(self.show)
        self.voice_thread.start()

    def get_weather_info(self):
        GET = requests.get("http://t.weather.sojson.com/api/weather/city/101200101")
        if GET.status_code == 200:
            JSON = GET.json()
            city = JSON['cityInfo']['city']
            today = JSON['data']['forecast'][0]  # 今天的天气数据
            tomorrow = JSON['data']['forecast'][1]  # 明天的天气数据

            weather_info = {
                'city': f"城市：{city}",
                'today': f"{today['type']}，{today['high']}，{today['low']}，{today['fx']}{today['fl']}",
                'today_notice': f"{today['notice']}",
                'tomorrow': f"{tomorrow['type']}，{tomorrow['high']}，{tomorrow['low']}，{tomorrow['fx']}{tomorrow['fl']}",
                'tomorrow_notice': f"{tomorrow['notice']}"
            }

            return weather_info
        else:
            return {
                'city': "无法获取天气信息",
                'today': "",
                'today_notice': "",
                'tomorrow': "",
                'tomorrow_notice': ""
            }

    def closeEvent(self, event):
        event.ignore()  # 忽略默认的关闭事件
        self.hide()  # 隐藏当前窗口，而不是关闭

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



# # 这个是我翻译模块的class窗口类
# class TranslationWindow(QWidget):
#     def __init__(self):
#         super(TranslationWindow, self).__init__()
#         self.setWindowTitle("翻译服务")
#         self.setWindowIcon(QIcon('resource/image/translation_ico.png'))
#         self.setGeometry(100, 100, 600, 500)
#
#         # 创建垂直布局
#         layout = QVBoxLayout()
#         self.setLayout(layout)
#
#         # 标题
#         title_label = QLabel("翻译服务", self)
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
#         layout.addWidget(title_label)
#
#         # 输入框和按钮区域
#         input_group = QGroupBox("", self)
#         input_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; border: 2px solid gray; border-radius: 10px; margin-top: 20px; }")
#         input_layout = QVBoxLayout()
#         input_group.setLayout(input_layout)
#
#         input_label = QLabel("输入", self)
#         input_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         input_layout.addWidget(input_label)
#
#         self.input_textedit = QLineEdit(self)
#         self.input_textedit.setMinimumHeight(50)  # 增大输入框的高度
#         input_layout.addWidget(self.input_textedit)
#
#         translate_button = QPushButton("translate", self)
#         translate_button.clicked.connect(self.translate)
#         input_layout.addWidget(translate_button)
#
#         layout.addWidget(input_group)
#
#         # 源语言和目标语言选择
#         languages_group = QGroupBox("", self)
#         languages_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; border: 2px solid gray; border-radius: 10px; margin-top: 20px; }")
#         languages_layout = QVBoxLayout()
#         languages_group.setLayout(languages_layout)
#
#         languages_label = QLabel("语言选择", self)
#         languages_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         languages_layout.addWidget(languages_label)
#
#         self.source_language_combo = QComboBox()
#         self.target_language_combo = QComboBox()
#
#
#
#         # 添加语言选项
#         languages = ["中文", "日文", "英文"]
#         self.source_language_combo.addItems(languages)
#         self.target_language_combo.addItems(languages)
#
#         languages_layout.addWidget(QLabel("源语言:", self))
#         languages_layout.addWidget(self.source_language_combo)
#         languages_layout.addWidget(QLabel("目标语言:", self))
#         languages_layout.addWidget(self.target_language_combo)
#
#         layout.addWidget(languages_group)
#
#         # 翻译结果区域
#         output_group = QGroupBox("", self)
#         output_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; border: 2px solid gray; border-radius: 10px; margin-top: 20px; }")
#         output_layout = QVBoxLayout()
#         output_group.setLayout(output_layout)
#
#         output_label = QLabel("翻译结果", self)
#         output_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
#         output_layout.addWidget(output_label)
#
#         self.translation_result_textedit = QTextEdit(self)
#         output_layout.addWidget(self.translation_result_textedit)
#
#         layout.addWidget(output_group)
#
#         # 让翻译页面显示在屏幕中央
#         desktop_rect = QApplication.desktop().availableGeometry()
#         self.move(desktop_rect.center() - self.rect().center())
#
#     def translate(self):
#
#         # 添加语言选项映射关系
#         languages_mapping = {
#             "中文": "zh",
#             "日文": "jp",
#             "英文": "en"
#         }
#
#         source_language = self.source_language_combo.currentText()
#         target_language = self.target_language_combo.currentText()
#
#         # 获取语言选项的映射值
#         from_lang = languages_mapping.get(source_language)
#         to_lang = languages_mapping.get(target_language)
#
#         text_to_translate = self.input_textedit.text()
#
#         translation = translate_text(text_to_translate, from_lang, to_lang)
#         self.translation_result_textedit.setText("\n".join(translation))  # 将翻译结果按行显示
#         engine = pyttsx3.init()
#         engine_thread = threading.Thread(target=self.speak_translation, args=(engine, translation))
#         engine_thread.start()
#
#     def speak_translation(self, engine, translation):
#         # 朗读翻译结果
#         for text in translation:
#             print(text)
#             tts_and_play(text=text)
#
#     def closeEvent(self, event):
#         event.ignore()  # 忽略默认的关闭事件
#         self.hide()  # 隐藏当前窗口，而不是关闭
#


# 停止按钮的class窗口类

#
# # 这个实现了我的文本翻译的功能
# def translate_text(query, from_lang='en', to_lang='zh'):
#     # 设置你自己的 appid/appkey。
#     appid = '20240222001970292'
#     appkey = 'uCBTLM_IlM9hf916fA2r'
#
#     endpoint = 'http://api.fanyi.baidu.com'
#     path = '/api/trans/vip/translate'
#     url = endpoint + path
#
#     def make_md5(s, encoding='utf-8'):
#         return md5(s.encode(encoding)).hexdigest()
#
#     salt = random.randint(32768, 65536)
#     sign = make_md5(appid + query + str(salt) + appkey)
#
#     headers = {'Content-Type': 'application/x-www-form-urlencoded'}
#     payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
#
#     r = requests.post(url, params=payload, headers=headers)
#     result = r.json()
#
#     # 解析JSON数据，选择目标内容
#     trans_result = result.get('trans_result', [])
#     filtered_results = [item['dst'] for item in trans_result]
#
#     return filtered_results


# 这个实现了打开我的csv文件的功能
def file_get():
    file_name = "data/web/web.csv"
    list1 = []
    try:
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Check if the row is not empty
                    dict1 = {}  # 创建一个新的字典对象
                    dict1['name'] = row[0]
                    dict1['href'] = row[1]
                    list1.append(dict1)
        return list1
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

def file_get_schedule():
    file_name = "data/schedule/todolist.csv"
    list1 = []
    try:
        with open(file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Check if the row is not empty
                    dict1 = {}  # 创建一个新的字典对象
                    dict1['name'] = row[0]
                    dict1['content'] = row[1]
                    list1.append(dict1)
        return list1
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

def process_schedule(item, id):
    title = item['name']
    content = item['content']
    speak(f"代办{id},{title}。内容：{content}")

# 这个实现了文本转语音的功能
def speak(msg):
    engine = pyttsx3.init()
    engine.say(msg)
    engine.runAndWait()



if __name__ == '__main__':
    app = QApplication([])

    # 创建主窗口并显示
    main_app = App()
    main_app.show()

    # 创建独立窗口并传递主窗口对象
    from pet_box import CustomDialog
    text_window = CustomDialog(main_app)
    text_window.show()

    app.exec_()