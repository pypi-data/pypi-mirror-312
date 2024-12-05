import socket
import json
import time

# 设置服务器参数
host = '127.0.0.1'  # 本地主机地址
port = 65432  # 非保留端口号

# 创建socket对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 绑定地址和端口
    s.bind((host, port))
    s.listen()
    print(f'Server listening on {host}:{port}')

    # 等待连接
    conn, addr = s.accept()

    with conn:
        print(f'Connected by {addr}')
        print("send first command")
        return_data = '{"Operation":"Move","DataType":"","Data":"","Device":0,"Station":1,"CameraType":0,"Result":"OK"}'
        # 发送JSON响应
        conn.sendall(return_data.encode('utf-8'))

        while True:


            # 接收数据
            data = conn.recv(1024)
            if not data:
                continue
            print(f'Received: {data}')
            # 解析JSON请求

            return_data = input("return command: ")
            # 发送JSON响应
            conn.sendall(return_data.encode('utf-8'))