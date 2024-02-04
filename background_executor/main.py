import socket
import threading
import json
import time


# 创建套接字
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名
host = socket.gethostname()
port = 6666

# 绑定端口
server_socket.bind((host, port))

# 设置最大连接数，超过后排队
server_socket.listen()

# 用来存放所有客户端的信息
clients = []
nicknames = []

# 处理客户端请求或响应
def client_processing(id, client_json):
    pass


# 广播消息给所有客户端
def broadcast(message):
    for client in clients:
        client.send(message + '##END##'.encode())

# 处理接收到的消息
def handle(client):
    while True:
        try:
            # 接收消息
            message = client.recv(1024)
            messages = message.decode().split('##END##')
            for message in messages:
                if message != '':
                    # broadcast(message)
                    # 处理消息
                    try:
                        mc = json.loads(message)
                        if mc["name"] == 'mcsm_sw' :
                            if mc['request_type'] == 'task':
                                broadcast('mcsm_sw想要执行任务'.encode())
                                broadcast(message.encode())
                            elif mc['request_type'] == 'check':
                                broadcast('mcsm_sw想要查看后台状态'.encode())
                                broadcast(message.encode())
                        elif mc['name'] == 'mcsm_return':
                            broadcast(message.encode())
                        # 测试=========
                        # 模拟返回数据
                        # message_data = {
                        #     'name' : 'mcsm_return', # 名称 mcsm_sw
                        #     'request_type' : 'return_data', # 请求类型 task(任务) check(查看) return_data(返回数据)

                        #     # 任务详情 data(任务数据)
                        #     'data' : [{
                        #         'switch' : 'off' # 开关 on开启 off关闭
                        #     }], 
                        # }
                        # time.sleep(0.1)
                        # broadcast(json.dumps(message_data).encode())
                        # =============
                    except:
                        print('转换失败')
                        broadcast(message.encode())
                else:
                    broadcast(message.encode())
        except:
            # 如果出错，移除客户端并关闭连接
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} 客户端已关闭.'.encode())
            nicknames.remove(nickname)
            break

# 循环接受新的连接
def receive():
    while True:
        # 接受连接
        client, address = server_socket.accept()
        print(f"连接成功，{str(address)}")

        # 获取用户昵称
        client.send('NICK'.encode()) # 双端确认
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        # 广播新用户加入
        print(f'客户端：{nickname}已连接.') # 后台提示客户端名称
        broadcast(f'{nickname} 成功加入！'.encode()) # 广播客户端名称

        # 开始处理用户消息
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("后端服务已启动")
print('等待连接...')

# 运行主程序
if __name__ == '__main__':
    receive()
