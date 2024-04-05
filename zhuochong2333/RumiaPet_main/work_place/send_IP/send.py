import socket
import threading
import os
import re

class FileSender:
    def __init__(self):
        self.server_host = ""
        self.file_path = ""
        self.server_port = 12345

    def check_ip(self,ipAddr):
        compile_ip = re.compile(
            '^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
        if compile_ip.match(ipAddr):
            return True
        else:
            return False

    def send_file(self):
        if self.check_ip(self.server_host) is False:
            return "请正确输入IP地址！"
        if len(self.file_path) <1 :
            return "请正确选择文件发送路径！"

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_host, self.server_port))

                # 发送文件名所需要的字节长度
                file_name = os.path.basename(self.file_path)
                file_name_length = len(file_name)
                s.sendall(file_name_length.to_bytes(4, byteorder='big'))

                # 传输文件名
                s.sendall(file_name.encode())

                # 传输文件长度
                file_length = os.path.getsize(self.file_path)
                s.sendall(file_length.to_bytes(4, byteorder='big'))

                # 发送文件内容
                with open(self.file_path, "rb") as f:
                    while True:
                        file_data = f.read(1024)
                        if not file_data:
                            break
                        s.sendall(file_data)
                return "File sent to server"
        except ConnectionRefusedError:
            return "Connection refused. Please check the server IP and port."
        except Exception as e:
            return f"An error occurred: {str(e)}"

