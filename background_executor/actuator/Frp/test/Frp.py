# mcsm控制器
import Frp_api

import socket
import threading
import json

# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取服务器主机名和端口号
server_host = socket.gethostname()
server_port = 6666

# 连接服务器
client_socket.connect((server_host, server_port))

# 客户端类型
nickname = "frpcontroller" # frp 译：frp控制器

# 发送用户昵称给服务器
client_socket.send(nickname.encode())


# 接收消息并处理
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            messages = message.split('##END##')
            for message in messages:
                if message != '':
                    if message == 'NICK':
                        # 发送name
                        client_socket.send(nickname.encode())
                    else:
                        print('内容',message)
                        # 转换格式
                        try:
                            data = json.loads(message)
                            print('收到任务')
                            switch = Frp_api.frp_controller() # 注册控制器
                            print('操作1')
                            # 判断是否需要运行执行器
                            if data['name'] == 'frp_sw': # 判断名称是否符合
                                print('操作2')
                                if data['request_type'] == 'task': # 请求类型 task(任务) check(查看)
                                    # 执行任务
                                    if data['data'][0]['switch'] == 'on':
                                        print('操作3')
                                        # 开启
                                        if switch.state() != 'on':
                                            switch.switch('on')
                                    elif data['data'][0]['switch'] == 'off':
                                        print('操作4')
                                        # 关闭
                                        print(switch.state())
                                        if switch.state() != 'off':
                                            switch.switch('off')
                                elif data['request_type'] == 'check':
                                    print('操作5')
                                    # 初始化参数
                                    message_data = {
                                        'name' : 'frp_return', # 名称 mcsm_sw
                                        'request_type' : 'return_data', # 请求类型 task(任务) check(查看) return_data(返回数据)
                                        # 任务详情 data(任务数据)
                                        'data' : [{
                                            'switch' : 'off' # 开关 on开启 off关闭
                                        }], 
                                    }

                                    # 查看状态
                                    if switch.state() == 'on':
                                        message_data['data'][0]['switch'] = 'on'
                                    elif switch.state() == 'off':
                                        message_data['data'][0]['switch'] = 'off'
                                    
                                    # 提交数据
                                    client_socket.send(json.dumps(message_data).encode() + '##END##'.encode())
                        except:
                            print('检测到消息：', message ,'但没有正确识别.')
        except:
            print("连接出错")
            client_socket.close()
            break

# 发送消息
# def write():
#     # while True:
#         # message = f'{nickname}: {input("")}'
#         # client_socket.send(message.encode())
#     sw = {'name' : 'mcsm_sw', 'sw' : 'on'}
#     client_socket.send(json.dumps(sw).encode())

# 使用多线程接收消息
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()
