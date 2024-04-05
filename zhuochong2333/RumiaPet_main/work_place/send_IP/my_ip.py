import socket

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("Local IP address:", local_ip)