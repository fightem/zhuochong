import socket
import os

def send_file(server_host, server_port, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        # 发送文件名所需要的字节长度
        file_name = os.path.basename(file_path)
        file_name_length = len(file_name)# 获取的文件名所需要的字节数
        s.sendall(file_name_length.to_bytes(4, byteorder='big'))# 将文件名所需要的字节数转换成4字节的二进制数

        # 传输文件名
        s.sendall(file_name.encode()) # 传输文件名的二进制数

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

if __name__ == "__main__":
    server_host = '10.85.3.168'  # 服务器主机地址
    server_port = 12345         # 服务器端口号
    file_path = r"C:\Users\29549\Desktop\比赛\AIGC\2.png"  # 要发送的文件路径
    send_file(server_host, server_port, file_path)