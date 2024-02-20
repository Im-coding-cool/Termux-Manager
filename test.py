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

# 生成随机id
def generate_random_id():
    return ''.join(str(random.randint(0, 9)) for _ in range(15))

# 读取id如果不存在就创建
def read_or_create_id(filename=global_configuration.ROOT_PSTH + 'id'):
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
        response = requests.post(url, data=data)
        time.sleep(20)

cloud_online_statistics('http://192.168.110.230:8090/statistics.php')