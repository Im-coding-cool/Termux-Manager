import socket
import socket
import threading
import json
import time
from api.p_rint import print_p
from api.wprint import wprint


# 链接服务器
def link_server(nickname):
    # 创建套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取服务器主机名和端口号
    server_host = socket.gethostname()
    server_port = 6666

    # 连接服务器
    client_socket.connect((server_host, server_port))

    # 发送用户昵称给服务器
    client_socket.send(nickname.encode())

    return client_socket


# 发送消息
def send_message(message_data):
    # 调用链接函数
    client_socket = link_server(message_data['name'])

    time.sleep(0.1)
    # 发送消息
    client_socket.send(json.dumps(message_data).encode() + '##END##'.encode())
    time.sleep(0.1)
    client_socket.close()



f_return_data = '' # 用于获取结果
# 获得返回结果
def return_data(client_socket):
    global f_return_data 

    while True:
        try:
            # 接收消息
            message = client_socket.recv(1024)
            wprint(message.decode())
            messages = message.decode().split('##END##')
            for message in messages:
                if message != '':
                    # 处理消息
                    try:
                        data = json.loads(message) # 转换格式
                        # 判断是否是返回的消息
                        if data['name'] == 'mcsm_return': # 判断名称是否符合
                            if data['request_type'] == 'return_data': # 请求类型 task(任务) check(查看) return_data(返回数据)
                                wprint('获取到结果')
                                wprint(data['data'])
                                
                                # 返回结果
                                
                                f_return_data= data['data']
                                client_socket.close()
                                return data['data']
                    except:
                        wprint('json转换失败可能不是json数据')
        except:
            wprint("连接出错")
            client_socket.close()
            f_return_data = "连接出错"
            return "连接出错"
        


# 获得后端返回值
def send_request_data(message_data):
    global f_return_data 
    # 调用链接函数
    client_socket = link_server(message_data['name'])
    time.sleep(0.1)

    # 发送消息
    client_socket.send(json.dumps(message_data).encode() + '##END##'.encode())
    time.sleep(0.1)


    write_thread = threading.Thread(target=return_data, args=(client_socket, ))
    write_thread.start()

    time.sleep(10)
    if f_return_data == '':
        f_return_data = '超时'
        client_socket.close()
    elif f_return_data == '连接出错':
        f_return_data = '连接出错'
    # write_thread.join



    return f_return_data
    # return return_data(client_socket)

    






# 发起任务
def start_task(message_data):
    # message_data = {
    #     'name' : 'mcsm_sw', # 名称 mcsm_sw
    #     'request_type' : 'task', # 请求类型 task(任务) check(查看) return_data(返回数据)

    #     # 任务详情 data(任务数据)
    #     'data' : [{
    #         'switch' : 'on' # 开关 on开启 off关闭
    #     }], 
    # }

    # 调用send_message发送任务
    write_thread = threading.Thread(target=send_message, args=(message_data, ))
    write_thread.start()
    write_thread.join
    return 0


# 请求返回值
def request_result(message_data):
    # message_data = {
    #     'name' : 'mcsm_sw', # 名称 mcsm_sw
    #     'request_type' : 'task', # 请求类型 task(任务) check(查看) return_data(返回数据)

    #     # 任务详情 data(任务数据)
    #     'data' : [{
    #         'switch' : 'on' # 开关 on开启 off关闭
    #     }], 
    # }
    
    return send_request_data(message_data)



# 测试======================测试

# message_data = {
#         'name' : 'mcsm_sw', # 名称 mcsm_sw
#         'request_type' : 'task', # 请求类型 task(任务) check(查看) return_data(返回数据)

#         # 任务详情 data(任务数据)
#         'data' : [{
#             'switch' : 'on' # 开关 on开启 off关闭
#         }], 
#     }

# start_task(message_data)


# message_data = {
#         'name' : 'mcsm_sw', # 名称 mcsm_sw
#         'request_type' : 'check', # 请求类型 task(任务) check(查看)
#     }

# data = request_result(message_data)
# print_p(na, data)