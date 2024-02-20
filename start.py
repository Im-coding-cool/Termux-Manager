import subprocess
import threading
import global_configuration
import requests
import os
import random
import time

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
LOG_PATH = global_config.get('start', 'log_path')
front_end_path = global_config.get('start', 'front_end')
rear_end_path = global_config.get('start', 'rear_end')
time_recorder_root_path = global_config.get('time_recorder', 'time_recorder_root_path')

def cl(name, sh):
    # 打开日志文件以追加模式写入
    with open(LOG_PATH + name + '.log', 'a') as f:
        # 使用Popen执行命令并实时记录输出
        process = subprocess.Popen(sh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='', file=f, flush=True)  # 将输出写入日志文件

# 生成随机id
def generate_random_id():
    return ''.join(str(random.randint(0, 9)) for _ in range(15))

# 读取id如果不存在就创建
def read_or_create_id(filename=global_configuration.ROOT_PSTH + 'config/id'):
    if os.path.exists(filename):
        # 如果文件存在，则读取其中的内容
        with open(filename, 'r') as file:
            user_id = file.read().strip()
    else:
        # 如果文件不存在，则生成一个随机id并写入文件
        user_id = generate_random_id()
        with open(filename, 'w') as file:
            file.write(user_id)

    return user_id



def cloud_online_statistics(url):
    result = subprocess.run('whoami', shell=True, capture_output=True, text=True).stdout
    user_id = read_or_create_id()

    while True:
        # POST数据
        data = {
            'name': user_id,
            'device_id': result,
        }
        # 发送POST请求
        try:
            response = requests.post(url, data=data)
        except:
            print('\033[31m错误: 服务器连接失败，但您任然可以使用本地功能。\033[0m')
        time.sleep(20)




if __name__ == "__main__":
    # 前端web程序
    th = threading.Thread(target=cl, args=('front_end','python3 ' + front_end_path + 'manage.py runserver 0.0.0.0:8000'))
    th.start()
    print('\033[1m\033[35m|=> 前端web程序: \033[22m\033[32m已启动\033[0m')

    # 后端异步程序
    th2 = threading.Thread(target=cl, args=('rear_end','python3 ' + rear_end_path + 'main.py'))
    th2.start()
    print('\033[1m\033[35m|=> 后端异步程序: \033[22m\033[32m已启动\033[0m')

    # 时间校准记录器
    th3 = threading.Thread(target=cl, args=('time_recorder','python3 ' + time_recorder_root_path + 'time_recorder.py'))
    th3.start()
    print('\033[1m\033[35m|=> 时间校准记录器: \033[22m\033[32m已启动\033[0m')

    # 云端在线统计
    th4 = threading.Thread(target=cloud_online_statistics, args=('http://38.6.175.125:8090/statistics.php',))
    th4.start()
    print('\033[1m\033[35m|=> 云端在线统计: \033[22m\033[32m已启动\033[0m')

    print('\033[32m+服务开启完毕\033[0m')
    print('请访问:\033[4m\033[31mhttp://0.0.0.0:8000/\033[0m\033[24m进入配置')
    print('默认密钥为:\033[31mchen\033[0m')



