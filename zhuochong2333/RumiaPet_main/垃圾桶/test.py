import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QScrollArea

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("对话窗口")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 创建一个滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # 创建一个文本编辑框，用于显示对话内容
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        # 将文本编辑框放置在滚动区域中
        self.scroll_area.setWidget(self.text_edit)

        # 创建一个按钮，用于添加对话内容
        self.button = QPushButton("添加对话")
        self.button.clicked.connect(self.add_dialogue)

        # 将滚动区域和按钮添加到布局中
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.button)

    def add_dialogue(self):
        # 模拟对话内容
        dialogue = "这是一条对话。" * 10
        self.text_edit.append(dialogue)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
