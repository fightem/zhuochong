from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QLabel, QPushButton, QComboBox, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt
import requests
import random
from hashlib import md5

class TranslationWindow(QWidget):
    def __init__(self):
        super(TranslationWindow, self).__init__()
        self.setWindowTitle("翻译服务")
        self.setGeometry(100, 100, 600, 500)

        # 创建垂直布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 标题
        title_label = QLabel("翻译服务", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # 输入框和按钮区域
        input_group = QGroupBox("", self)
        input_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; border: 2px solid gray; border-radius: 10px; margin-top: 20px; }")
        input_layout = QVBoxLayout()
        input_group.setLayout(input_layout)

        input_label = QLabel("输入", self)
        input_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        input_layout.addWidget(input_label)

        self.input_textedit = QLineEdit(self)
        self.input_textedit.setMinimumHeight(50)  # 增大输入框的高度
        input_layout.addWidget(self.input_textedit)

        translate_button = QPushButton("translate", self)
        translate_button.clicked.connect(self.translate)
        input_layout.addWidget(translate_button)

        layout.addWidget(input_group)

        # 源语言和目标语言选择
        languages_group = QGroupBox("", self)
        languages_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; border: 2px solid gray; border-radius: 10px; margin-top: 20px; }")
        languages_layout = QVBoxLayout()
        languages_group.setLayout(languages_layout)

        languages_label = QLabel("语言选择", self)
        languages_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        languages_layout.addWidget(languages_label)

        self.source_language_combo = QComboBox()
        self.target_language_combo = QComboBox()



        # 添加语言选项
        languages = ["中文", "日文", "英文"]
        self.source_language_combo.addItems(languages)
        self.target_language_combo.addItems(languages)

        languages_layout.addWidget(QLabel("源语言:", self))
        languages_layout.addWidget(self.source_language_combo)
        languages_layout.addWidget(QLabel("目标语言:", self))
        languages_layout.addWidget(self.target_language_combo)

        layout.addWidget(languages_group)

        # 翻译结果区域
        output_group = QGroupBox("", self)
        output_group.setStyleSheet("QGroupBox { font-weight: bold; font-size: 16px; border: 2px solid gray; border-radius: 10px; margin-top: 20px; }")
        output_layout = QVBoxLayout()
        output_group.setLayout(output_layout)

        output_label = QLabel("翻译结果", self)
        output_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        output_layout.addWidget(output_label)

        self.translation_result_textedit = QTextEdit(self)
        output_layout.addWidget(self.translation_result_textedit)

        layout.addWidget(output_group)

        # 让翻译页面显示在屏幕中央
        desktop_rect = QApplication.desktop().availableGeometry()
        self.move(desktop_rect.center() - self.rect().center())

    def translate(self):

        # 添加语言选项映射关系
        languages_mapping = {
            "中文": "zh",
            "日文": "jp",
            "英文": "en"
        }

        source_language = self.source_language_combo.currentText()
        target_language = self.target_language_combo.currentText()

        # 获取语言选项的映射值
        from_lang = languages_mapping.get(source_language)
        to_lang = languages_mapping.get(target_language)

        text_to_translate = self.input_textedit.text()

        translation = translate_text(text_to_translate, from_lang, to_lang)
        self.translation_result_textedit.setText("\n".join(translation))  # 将翻译结果按行显示

def translate_text(query, from_lang='en', to_lang='zh'):
    # 设置你自己的 appid/appkey。
    appid = '20240222001970292'
    appkey = 'uCBTLM_IlM9hf916fA2r'

    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path

    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    # 解析JSON数据，选择目标内容
    trans_result = result.get('trans_result', [])
    filtered_results = [item['dst'] for item in trans_result]

    return filtered_results

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    translation_window = TranslationWindow()
    translation_window.show()
    sys.exit(app.exec_())
