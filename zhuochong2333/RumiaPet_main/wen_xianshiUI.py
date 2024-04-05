import sys
import pyttsx3
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from multiprocessing import Process
from TTS_bachongshenzi import tts_and_play
character_name = '八重神子'

def speak(text):
    tts_and_play(text=text)
    # engine = pyttsx3.init()
    # engine.say(text)
    # engine.runAndWait()


class VoiceChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.should_continue = True  # 实例属性，用于控制循环
        self.voice_process = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Voice Chat")
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setFixedSize(300, 180)

        self.layout = QVBoxLayout(self)
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet("font: 12pt 'Arial';")
        self.text_edit.setAlignment(Qt.AlignCenter)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        self.layout.addWidget(self.text_edit)

        icon_path = "data/iconay.png"
        icon = QIcon(icon_path)
        self.icon_button = QPushButton(self)
        self.icon_button.setIcon(icon)
        self.icon_button.setIconSize(QPixmap(icon_path).size() * 0.1)
        self.layout.addWidget(self.icon_button, alignment=Qt.AlignCenter)

        background_path = "data/rumia/bkg36.png"
        self.setStyleSheet(
            f"border: none; background-image: url('{background_path}'); background-repeat: no-repeat; background-position: 320px 220px;")

        self.icon_button.clicked.connect(self.icon_button_clicked)

    def closeEvent(self, event):
        self.should_continue = False
        if self.voice_process and self.voice_process.is_alive():
            self.voice_process.terminate()
            self.voice_process.join()
        event.ignore()  # 忽略默认的关闭事件
        self.hide()  # 隐藏窗口，不关闭

    def set_text(self, text):
        self.text_edit.setPlainText(text)
        self.start_voice_process(text)

    def icon_button_clicked(self):
        print("Icon button clicked!")

    def start_voice_process(self, text):
        if self.voice_process and self.voice_process.is_alive():
            self.voice_process.terminate()
            self.voice_process.join()
        self.voice_process = Process(target=speak, args=(text,))
        self.voice_process.start()

    def is_voice_playing(self):
        return self.voice_process is not None and self.voice_process.is_alive()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceChatWindow()
    window.show()

    # 例子：在外部代码中调用set_text方法更新文本内容
    window.set_text("Hello, this is a test message. This text will automatically wrap to the next line if it exceeds the width of the window.")

