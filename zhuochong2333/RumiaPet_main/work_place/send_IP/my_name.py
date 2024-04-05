import socket
import threading
import os

def handle_client(conn, addr):
    print('Connected by', addr)
    with conn:
        # 接收文件名长度
        file_name_length_bytes = conn.recv(4) # 接收文件名所需要的长度的二进制数
        file_name_length = int.from_bytes(file_name_length_bytes, byteorder='big') # 将其转换为int类型的整数

        # 接收文件名
        file_name = conn.recv(file_name_length).decode()# 根据所需要的文件名字节数，取出文件名
        file_path = f"received_files/{file_name}" # 增加addr内容，防止不同用户上传同名文件

        # 接收文件长度，可以用于实现进度条
        file_length_bytes = conn.recv(4)
        file_length = int.from_bytes(file_length_bytes, byteorder='big')
        # 接收文件内容，分块写入，增加安全性
        with open(file_path, "wb") as f:
            received_data = 0 # 记录已经下载的数据字节数
            while True:
                data = conn.recv(1024)
                received_data += len(data)
                print(received_data / file_length)
                if not data:
                    break
                f.write(data)
        print(f'File "{file_name}" received from', addr)

def start_server(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server listening on port", port)
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

import socket

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("Local IP address:", local_ip)
    if not os.path.exists("received_files"):
        os.makedirs("received_files")
    start_server('0.0.0.0', 12345)
