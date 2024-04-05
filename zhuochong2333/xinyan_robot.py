from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class WenxinYanyanChat(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文心一言聊天")
        self.setup_ui()
        self.fetch_quote()

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.refresh_button = QtWidgets.QPushButton("刷新")
        self.layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.fetch_quote)

    def fetch_quote(self):
        try:
            response = requests.get("https://v1.hitokoto.cn/")
            if response.status_code == 200:
                data = response.json()
                quote = data.get("hitokoto", "")
                self.text_edit.setText(quote)
            else:
                self.text_edit.setText("获取文心一言失败")
        except Exception as e:
            self.text_edit.setText(f"错误：{str(e)}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    chat_window = WenxinYanyanChat()
    chat_window.show()
    sys.exit(app.exec_())
