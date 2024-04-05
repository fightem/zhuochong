
import requests
import json
import datetime
import random

"""
    该类是父类，通过继承该类，可以实现输入对应的choice(相应选择)与tips(提示信息)，来随机从相应tips中选择一条信息
    继承要完成的工作：
        1. __init__()调用generateChoice()、generateTips()
        2. 实现generateChoice、generateTips()
        3. 如果出现了提示信息，可以通过修改继承类的generateReminder()的逻辑实现跳转，比如出现天气提示信息在桌宠旁边后，
        可以通过点击那个提示信息，去查看最近的天气。或者日程表中某个代办事件的deadline快到了出现提示，可以点击提示信息进行跳转
    比如： 
        choice = 雨天
        # tips有2类，分别是雨天和雪天两类提示信息
        tips = [
            # 雨天相应的提示信息共3条
            [今天有雨，记得带伞哦！", "今天有雨，记得添衣！","在下雨喵，记得带伞喵"]
            # 雪天相应的提示信息,共两条
            ["今天有雪，记得带伞哦！", "今天有雪，记得添衣！"]
        ]
        输出是从[今天有雨，记得带伞哦！", "今天有雨，记得添衣！","在下雨喵，记得带伞喵"]这3条数据中随机选择一条进行输出
"""
class RandomReminder():
    def __init__(self, *args, **kwargs):
        self.choice = -1
        self.tips = []
    def generateChoice(self, *args, **kwargs)->None:
        pass

    # 根据不同场景选择不同的输入
    def generateTips(self, *args, **kwargs)->None:
        pass

    def generateRemind(self, *args, **kwargs)->str:
        # choice大于tips的个数或者choice没有生成则返回None
        if self.choice == -1 or self.choice > len(self.tips):
            return
        return random.choice(self.tips[self.choice])


### 天气情况提示信息
class WeatherReminder(RandomReminder):
    def __init__(self, city, **kwargs):
        super().__init__(**kwargs)
        self.city = city
        self.KEY = '20c4f5de754b4b2a9b475d12ccf88bd9'
        # 生成choice与Tips
        self.generateChoice()
        self.generateTips()
    def get_city_id(self) -> str:
        url_v2 = f'https://geoapi.qweather.com/v2/city/lookup?location={self.city}&key={self.KEY}'  # 城市地理信息
        city_id = requests.get(url_v2).json()['location'][0]['id']
        return city_id

    def generateChoice(self) -> None:
        # 内容返回一个int类型的值
        city_id = self.get_city_id()
        url = f'https://devapi.qweather.com/v7/weather/now?location={city_id}&key={self.KEY}'  # 每日的数据（包含体感温度和相对湿度）
        response = requests.get(url)
        data = response.json()['now']["text"]  # 获取当日情况

        # 生成choice
        if "雨" in data:
            self.choice = 0
        elif "雪" in data:
            self.choice = 1
        else:
            self.choice = 2
    def generateTips(self) -> None:
        # 命名格式  choice + 数字命名，数字最好与Choice的值对应
        # 内容格式  ["str1", "str2", ... , "strn"]
        choice0 = ["今天有雨，记得带伞哦！", "今天有雨，记得添衣！","在下雨喵，记得带伞喵"]
        choice1 = ["今天有雪，记得带伞哦！", "今天有雪，记得添衣！", "在下雪喵，记得带伞喵"]
        choice2 = ["今天天气不错，出门记得享受阳光！"]

        for i in range(3):
            tip = locals()[f"choice{i}"]  # 获取局部变量
            self.tips.append(tip)  # 添加到其中

    def generateRemind(self) -> str:
        return super().generateRemind()


### 代办事项提示信息
class TodoReminder(RandomReminder):
    def __init__(self):
        super().__init__()



if __name__ == "__main__":
    w = WeatherReminder("武汉")
    print(w.generateRemind())
