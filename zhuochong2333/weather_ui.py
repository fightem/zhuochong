import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy, QFrame
from PyQt5.QtCore import QDate, Qt, QLocale
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis  # 导入QtCharts模块
default_city = '长沙'
from weather_api import QWeatherAPI
list1 = QWeatherAPI.weather_seven(default_city)
print(list1)
from qt_material import apply_stylesheet

from PyQt5.QtCore import Qt, QThread, pyqtSignal

from VoiceSettingUI import get_latest_pet_sound

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
        print(self.msg)
        tts_and_play(text=self.msg)



def get_weekday_text(day):
    if day == '昨天':
        return f'{get_weekday(0)}(今天)'
    elif day == '今天':
        return get_weekday(1)
    elif day == '明天':
        return get_weekday(2)
    elif day == '后天':
        return get_weekday(3)
    elif day == '第四天':
        return get_weekday(4)
    elif day == '第五天':
        return get_weekday(5)
    elif day == '第六天':
        return get_weekday(6)

def get_weekday(days_offset):
    current_date = QDate.currentDate()
    date = current_date.addDays(days_offset)
    locale = QLocale()
    weekday_index = date.dayOfWeek()
    return locale.dayName(weekday_index, QLocale.LongFormat)

class WeatherForecastWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('天气预报')
        self.setGeometry(100, 100, 800, 400)



        # 定义每个元素之间的默认垂直间距
        self.default_spacing = 40

        # 定义天气图标到空气质量的垂直距离
        self.default_spacing_biao_toair = 40

        # 定义日期标签和模块之间的自定义间距
        self.date_module_spacing = 20

        # 定义最高温和最低温之间的距离
        self.default_spacing_wendu = 20



        # 定义空气可见度和风之间的距离
        self.default_spacing_kongqi = 30

        # 顶级风和级数之间的距离
        self.default_spacing_jishu = 5


        # 添加自定义的垂直间距变量
        self.weather_label_spacing = 20  # 自定义天气标签之间的垂直间距
        self.info_label_spacing = 20  # 自定义信息标签之间的垂直间距


        self.setup_ui()

    def setup_ui(self):
        data = list1[0]
        main_layout = QHBoxLayout()

        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)  # 设置布局中控件之间的默认间距为0

        title_label = QLabel(f'当前城市名称:{list1[0]["province_name"]}({list1[0]["city_name"]}市)')
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333333;")  # 设置标题样式
        left_layout.addWidget(title_label)
        # search_label = QLabel(f'当前城市名称:{list1[0]["province_name"]}({list1[0]["city_name"]}市)')
        # self.search_edit = QLineEdit()
        #
        # search_button = QPushButton('搜索')
        # search_button.clicked.connect(self.fetch_weather_data)  # 连接搜索按钮的点击事件到 fetch_weather_data 方法上
        # search_button.clicked.connect(self.search_weather)

        #
        # left_layout.addWidget(search_label)
        # left_layout.addWidget(self.search_edit)
        # left_layout.addWidget(search_button)
        left_layout.addSpacing(40)  # 添加天气标签和信息标签之间的垂直间距

        # 天气提示信息
        weather_icon_label = QLabel(f'今日天气：{list1[0]["weather_text"]} {list1[1][0]["min_temp"]}°C-{list1[1][0]["max_temp"]}°C')
        weather_icon_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333333;")
        left_layout.addWidget(weather_icon_label)

        left_layout.addSpacing(self.weather_label_spacing)  # 添加天气标签和信息标签之间的垂直间距


        # 天气提示信息
        weather_alert_label = QLabel(f'{data["msg"]}')
        left_layout.addWidget(weather_alert_label)
        left_layout.addSpacing(self.weather_label_spacing)  # 添加天气标签和信息标签之间的垂直间距

        # 天气信息标签
        weather_info_label = QLabel(f'体感温度：{data["temp_ti"]}  湿度：{data["humidity"]}  天气：{data["weather_text"]}  空气质量：{data["air_aqi"]}')
        left_layout.addWidget(weather_info_label)
        left_layout.addSpacing(self.info_label_spacing)  # 添加信息标签和后续标签之间的垂直间距

        # 后续标签
        weather_hourlater_label = QLabel(f'{data["hour_later"]}')
        left_layout.addWidget(weather_hourlater_label)

        main_layout.addLayout(left_layout, 4)  # 左侧布局占比4

        # 添加分隔线
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(separator_line)

        # 右侧布局
        right_layout = QVBoxLayout()

        # 添加当前日期和星期几到右上角
        current_date = QDate.currentDate()
        date_text = current_date.toString(Qt.SystemLocaleLongDate)
        weekday_text = current_date.toString("dddd")
        msg = date_text + ' ' + weekday_text  # 添加空格分隔

        date_label = QLabel(msg)
        date_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        date_label.setStyleSheet("font-size: 16px;")  # 设置字体大小
        right_layout.addWidget(date_label)

        right_layout.addSpacing(self.date_module_spacing)  # 添加日期标签和模块之间的自定义间距

        days_layout = QHBoxLayout()

        # 设定星期几下面的所有功能
        days = ['昨天', '今天', '明天', '后天', '第四天', '第五天', '第六天']

        temperatures = []
        for msg in list1[1]:
            dic_temp = {}
            dic_temp['max_temp'] = msg['max_temp']
            dic_temp['min_temp'] = msg['min_temp']
            dic_temp['weather_day'] = msg['weather_day']
            dic_temp['windDirDay'] = msg['windDirDay']
            dic_temp['windSpeedDay'] = msg['windSpeedDay']
            dic_temp['vis'] = msg['vis']

            temperatures.append(dic_temp)

        # temperatures = ['18°C', '20°C', '22°C', '18°C', '20°C', '22°C', '20°C']

        for day, temp in zip(days, temperatures):

            true_day = get_weekday_text(day)   # 得到星期几的数据
            day_label = QLabel(true_day)

            # 添加月/日日期
            date_label = QLabel(current_date.addDays(days.index(day)).toString("MM/dd"))

            weather_icon = QLabel(f'{temp["weather_day"]}')

            temperature_label_max = QLabel(f'高温{temp["max_temp"]}°C')  # 最高温度
            temperature_label_min = QLabel(f'低温{temp["min_temp"]}°C')  # 最低温度
            air_label = QLabel(f'可见度{temp["vis"]}')
            windDirDay = QLabel(f'{temp["windDirDay"]}')
            windSpeedDay = QLabel(f'{temp["windSpeedDay"]}')

            # # 添加折线图显示温度
            chart_view = QChartView(self.create_temperature_chart_low())


            day_layout = QVBoxLayout()
            day_layout.addWidget(day_label)              # 1.添加星期几的情况
            day_layout.addWidget(date_label)             # 2.添加星期下面的月/日情况
            day_layout.addSpacing(self.default_spacing)  # 添加自定义的垂直间距
            day_layout.addWidget(weather_icon)           # 3.添加自定义的天气图标
            day_layout.addSpacing(self.default_spacing_biao_toair)  # 添加自定义的垂直间距
            day_layout.addWidget(temperature_label_max)  # 5.添加自定义的最高温度内容
            day_layout.addSpacing(self.default_spacing_wendu)  ## 添加自定义的垂直间距

            day_layout.addWidget(temperature_label_min)  # 6.添加自定义的最低温度内容
            day_layout.addSpacing(self.default_spacing)  # 添加自定义的垂直间距
            day_layout.addWidget(air_label)              # 4.添加自定义的空气质量
            day_layout.addSpacing(self.default_spacing_kongqi)  # 添加自定义的垂直间距
            day_layout.addWidget(windDirDay)
            day_layout.addSpacing(self.default_spacing_jishu)
            day_layout.addWidget(windSpeedDay)




            days_layout.addLayout(day_layout)

        right_layout.addLayout(days_layout)

        # # 添加折线图显示温度
        # chart_view = QChartView(self.create_temperature_chart_low())
        # right_layout.addWidget(chart_view)


        main_layout.addLayout(right_layout, 6)  # 右侧布局占比6

        # 添加伸缩器，将日期标签推到右上角
        spacer_item = QWidget()
        spacer_item.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(spacer_item)



        self.setLayout(main_layout)

        msg = f"今天天气：{list1[0]['weather_text']} 体感温度{list1[0]['temp_ti'].split('°C')[0]}摄氏度 。主人，今日{list1[0]['msg']}"
        self.voice_thread = VoiceThread(msg)
        self.voice_thread.finished.connect(self.show)
        self.voice_thread.start()

    def fetch_weather_data(self):

        city_name = self.search_edit.text()  # 获取用户输入的城市名称

        from weather_api import QWeatherAPI
        list1 = QWeatherAPI.weather_seven(city_name)
        print(list1)
        # 更新左侧布局中的信息
        data = list1[0]
        search_label = self.findChild(QLabel, 'search_label')
        search_label.setText(f'当前城市名称:{list1[0]["province_name"]}({list1[0]["city_name"]}市)')

        weather_alert_label = self.findChild(QLabel, 'weather_alert_label')
        weather_alert_label.setText(f'{data["msg"]}')

        weather_info_label = self.findChild(QLabel, 'weather_info_label')
        weather_info_label.setText(
            f'体感温度：{data["temp_ti"]}  湿度：{data["humidity"]}  天气：{data["weather_text"]}  空气质量：{data["air_aqi"]}')

        weather_hourlater_label = self.findChild(QLabel, 'weather_hourlater_label')
        weather_hourlater_label.setText(f'{data["hour_later"]}')


    def create_temperature_chart_low(self):
        chart = QChart()
        low_series = QLineSeries()
        # Add data points to the series
        temperatures = ['18°C', '20°C', '22°C', '18°C', '20°C', '22°C', '20°C']
        for i, temp in enumerate(temperatures):
            low_temp = int(temp.split('°C')[0])
            low_series.append(i, low_temp)

        # Add series to the chart
        chart.addSeries(low_series)
        return chart

    def search_weather(self):
        city_name = self.search_edit.text()

        # 在这里添加获取天气信息的功能,例如调用API等

    def closeEvent(self, event):
        event.ignore()  # 忽略默认的关闭事件
        self.hide()  # 隐藏当前窗口，而不是关闭


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherForecastWidget()

    apply_stylesheet(app, theme='light_blue.xml', invert_secondary=True)
    window.show()
    sys.exit(app.exec_())
