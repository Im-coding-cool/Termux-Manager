import socket
import threading
import json
import time


# 创建套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取服务器主机名和端口号
server_host = socket.gethostname()
server_port = 6666

# 连接服务器
client_socket.connect((server_host, server_port))

# 获取客户端类型
nickname = "mcsm_sw##END##"

# 发送用户昵称给服务器
client_socket.send(nickname.encode())

# 发送消息
def write():
    sw = {
        'name' : 'mcsm_sw', # 名称 mcsm_sw
        'request_type' : 'task', # 请求类型 task(任务) check(查看)

        # 任务详情 data(任务数据)
        'data' : [{
            'switch' : 'on' # 开关 on开启 off关闭
        }], 
    }
    client_socket.send(json.dumps(sw).encode() + '##END##'.encode())
    time.sleep(0.5)
    client_socket.close()

write_thread = threading.Thread(target=write)
write_thread.start()

