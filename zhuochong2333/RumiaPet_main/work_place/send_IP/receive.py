import socket
import threading
import os

class FileReceiver:
    def __init__(self):
        self.host = '0.0.0.0'  # 监听所有网络接口
        self.port = 12345
        self.save_path = ""

    def handle_client(self, conn, addr):
        print('Connected by', addr)
        with conn:
            # 接收文件名长度
            file_name_length_bytes = conn.recv(4)
            file_name_length = int.from_bytes(file_name_length_bytes, byteorder='big')

            # 接收文件名
            file_name = conn.recv(file_name_length).decode()
            file_path = f"{self.save_path}/{addr}_{file_name}"  # 增加addr内容，防止不同用户上传同名文件

            print(file_path)
            # 接收文件长度，可以用于实现进度条
            # file_length_bytes = conn.recv(4)
            # file_length = int.from_bytes(file_length_bytes, byteorder='big')

            # 接收文件内容，分块写入，增加安全性
            with open(file_path, "wb") as f:
                received_data = 0
                while True:
                    data = conn.recv(1024)
                    received_data += len(data)
                    # print(received_data / file_length)
                    if not data:
                        break
                    f.write(data)
            return f'File "{file_name}" received from', addr

    def start_server(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print("Server listening on port", self.port)
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
