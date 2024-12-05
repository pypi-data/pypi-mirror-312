# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import socket
import json
import threading
import time


def send_command(cmd):
    # json_data = json.dumps(cmd)
    s.sendall(cmd.encode('utf-8'))

def recv():
    while True:
        data = s.recv(1024)
        response = json.loads(data.decode('utf-8'))
        print(f"Received: {response}")
        time.sleep(0.5)


# 设置服务器参数
host = '192.168.1.20'  # 服务器的主机地址
port = 2024  # 服务器的非保留端口号
Thread = threading.Thread(target=recv)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 连接到服务器
    s.connect((host, port))
    Thread.start()

    print("Type 'exit' to quit")
    while True:
        # 获取输入命令
        cmd = input("Enter command: ")
        if cmd.lower() == 'exit':
            Thread.join()
            break

        # 发送命令并接收响应
        send_command(cmd)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
