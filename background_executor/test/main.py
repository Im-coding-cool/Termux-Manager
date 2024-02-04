# 服务器端代码
import socket

def main():
    # 创建socket对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 获取本地主机名
    host = socket.gethostname()
    port = 12345  # 设置端口号

    # 绑定端口
    server_socket.bind((host, port))

    # 设置最大连接数，超过后排队
    server_socket.listen(5)

    while True:
        # 建立客户端连接
        client_socket, addr = server_socket.accept()
        print('连接地址：', addr)

        # 接收客户端数据
        data = client_socket.recv(1024)
        print('接收到的数据：', data.decode('utf-8'))

        # 发送数据到客户端
        if data.decode('utf-8') == "请求状态":
            client_socket.send("停止运行".encode('utf-8'))
        elif data.decode('utf-8') == "开启MCSM":
            print("开启MCSM")
        elif data.decode('utf-8') == "关闭MCSM":
            print("关闭MCSM")

        # 关闭连接
        client_socket.close()

if __name__ == '__main__':
    main()
