# 声音选择设置
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QDesktopWidget
from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class PetSoundSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("宠物声音设置")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)

        # 字体设置为"微软雅黑", 12号
        font = QFont("等线", 11)
        font.setBold(True)
        font.setWeight(70)

        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        window_width = 280
        window_height = 150
        window_x = (screen.width() - window_width) // 2
        window_y = (screen.height() - window_height) // 2
        self.setGeometry(window_x, window_y, window_width, window_height)

        layout = QVBoxLayout()

        label = QLabel("选择宠物声音：", self)
        label.setFont(font)
        layout.addWidget(label)

        # 下拉菜单的字体设置为"微软雅黑", 8号
        font2 = QFont("等线", 10)
        font2.setBold(True)
        font2.setWeight(40)

        # 下拉菜单
        self.sound_combo_box = QComboBox(self)
        self.sound_combo_box.setFont(font2)

        # 添加character_data中的选项
        character_data = get_character_data()  # 从网络获取角色数据
        if character_data:
            self.sound_combo_box.addItems(character_data)

        # 获取用户之前保存的选择
        previous_selection = get_previous_selection()
        if previous_selection and previous_selection in character_data:
            index = self.sound_combo_box.findText(previous_selection)
            if index != -1:
                self.sound_combo_box.setCurrentIndex(index)

        layout.addWidget(self.sound_combo_box)

        # 保存按钮
        save_button = QPushButton("保存", self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_settings(self):
        selected_sound = self.sound_combo_box.currentText()
        print(f"已选择的宠物声音：{selected_sound}")
        # 保存当前选择
        save_previous_selection(selected_sound)
        # 在这里添加保存设置的代码

    def closeEvent(self, event):
        event.ignore()  # 忽略默认的关闭事件
        self.hide()  # 隐藏当前窗口，而不是关闭



def get_character_data():
    import requests

    url = 'http://127.0.0.1:5000/character_list'

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to retrieve character list. Status code:', response.status_code)
        return None

def get_previous_selection():
    settings = QSettings("MyCompany", "PetSoundSettings")
    return settings.value("previous_selection")

def save_previous_selection(selection):
    settings = QSettings("MyCompany", "PetSoundSettings")
    settings.setValue("previous_selection", selection)



def get_latest_pet_sound():
    settings = QSettings("MyCompany", "PetSoundSettings")
    return settings.value("previous_selection")

if __name__ == "__main__":
    data = get_latest_pet_sound()

    import sys
    app = QApplication(sys.argv)
    window = PetSoundSettings()
    window.show()

    sys.exit(app.exec_())


