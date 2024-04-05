import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox
import socket
import os
from PyQt5.QtCore import Qt

class FileTransferWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('文件传输')
        self.resize(400, 200)

        # 创建顶部布局
        top_layout = QHBoxLayout()
        self.ip_label = QLabel('传输IP地址:')
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText('请输入IP地址')
        self.get_ip_button = QPushButton('获取我的IP地址')
        top_layout.addWidget(self.ip_label)
        top_layout.addWidget(self.ip_input)
        top_layout.addWidget(self.get_ip_button)

        # 创建中间布局
        middle_layout = QVBoxLayout()
        self.file_button = QPushButton('选择文件')
        self.submit_button = QPushButton('提交')
        middle_layout.addStretch(1)  # 添加伸缩项，使顶部和底部留有间距
        middle_layout.addWidget(self.file_button)
        middle_layout.addWidget(self.submit_button)
        middle_layout.addStretch(1)  # 添加伸缩项，使顶部和底部留有间距

        # 创建底部布局用于显示IP地址
        self.ip_display_label = QLabel('IP地址将显示在这里')
        self.ip_display_label.setAlignment(Qt.AlignCenter)  # 居中显示

        # 创建主布局并添加子布局
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addWidget(self.ip_display_label)
        main_layout.setContentsMargins(20, 20, 20, 20)  # 设置主布局边距
        main_layout.setSpacing(20)  # 设置布局间距

        self.setLayout(main_layout)

        self.file_button.clicked.connect(self.select_file)
        self.submit_button.clicked.connect(self.show_confirmation_dialog)
        self.get_ip_button.clicked.connect(self.get_my_ip)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, '选择文件', '', 'All Files (*)')
        if file_path:
            self.file_path = file_path
            self.file_button.setText(f'已选择文件: {file_path}')

    def show_confirmation_dialog(self):
        if hasattr(self, 'file_path'):
            file_path = self.file_path
            ip_address = self.ip_input.text()
            confirmation = QMessageBox.question(self, '确认提交', f'传输文件: {file_path} 到 IP 地址: {ip_address}\n确定继续吗？',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirmation == QMessageBox.Yes:

                send_file(server_host=ip_address, server_port=12345, file_path=file_path)
                self.show_transfer_complete_message()  # 在文件传输完成后显示消息框
        else:
            QMessageBox.warning(self, '警告', '请先选择文件')

    def get_my_ip(self):
        local_ip = get_local_ip()
        self.ip_display_label.setText(f'本机IP地址: {local_ip}')

    def show_transfer_complete_message(self):
        QMessageBox.information(self, '传输完成', '文件传输已完成！')

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def send_file(server_host, server_port, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        # 发送文件名所需要的字节长度
        file_name = os.path.basename(file_path)
        file_name_length = len(file_name)  # 获取的文件名所需要的字节数
        s.sendall(file_name_length.to_bytes(4, byteorder='big'))  # 将文件名所需要的字节数转换成4字节的二进制数

        # 传输文件名
        s.sendall(file_name.encode())  # 传输文件名的二进制数

        # 传输文件长度
        file_length = os.path.getsize(file_path)
        s.sendall(file_length.to_bytes(4, byteorder='big'))

        # 发送文件内容
        with open(file_path, "rb") as f:
            while True:
                file_data = f.read(1024)
                if not file_data:
                    break
                s.sendall(file_data)
        print("File sent to server")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = FileTransferWidget()
    widget.show()
    sys.exit(app.exec_())
