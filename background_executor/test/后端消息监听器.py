import socket
import threading
import time

# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取服务器主机名和端口号
server_host = socket.gethostname()
server_port = 6666

# 连接服务器
client_socket.connect((server_host, server_port))

# 获取用户昵称
nickname = '后台消息监听器'

# 发送用户昵称给服务器
client_socket.send(nickname.encode())

# 接收消息并打印
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            messages = message.split('##END##')
            for messagea in messages:
                if messagea != '':
                    if messagea == 'NICK':
                        client_socket.send(nickname.encode())
                    else:
                        print(messagea)
        except:
            print("连接出错")
            client_socket.close()
            break

# # 发送消息
# def write():
#     while True:
#         message = f'{nickname}: {input("")}'
#         client_socket.send(message.encode())

# 创建线程来同时处理接收和发送消息
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()
