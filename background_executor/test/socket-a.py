import socket
import threading

# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
port = 5555

# 绑定端口
server_socket.bind((host, port))

# 设置最大连接数，超过后排队
server_socket.listen()

# 用来存放所有客户端的信息
clients = []
nicknames = []

# 广播消息给所有客户端
def broadcast(message):
    for client in clients:
        client.send(message)

# 处理接收到的消息
def handle(client):
    while True:
        try:
            # 接收消息
            message = client.recv(1024)
            broadcast(message)
        except:
            # 如果出错，移除客户端并关闭连接
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} 离开了聊天室！'.encode())
            nicknames.remove(nickname)
            break

# 循环接受新的连接
def receive():
    while True:
        # 接受连接
        client, address = server_socket.accept()
        print(f"连接成功，{str(address)}")

        # 获取用户昵称
        client.send('NICK'.encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        # 广播新用户加入
        print(f'用户昵称为：{nickname}')
        broadcast(f'{nickname} 加入了聊天室！'.encode())

        # 开始处理用户消息
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("服务器启动中...")
receive()
