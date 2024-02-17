import os
import wprint
import re
import threading
import time

import mcsm_api
switch = mcsm_api.mcsm_controller() # 注册控制器

import json

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
PATH = global_config.get('rear_end', 'path')
根目录 = PATH + 'data'  # 数据交换目录


def 保存结果(message_data):    
    # 以覆盖方式写入文件，如果没有该文件就创建一个
    with open(根目录 + '/-1-mcsm_return.json', 'w') as file:
        file.write(json.dumps(message_data))

def 执行(data):
    if data['request_type'] == 'task': # 请求类型 task(任务) check(查看)
        # 执行任务
        if data['data'][0]['switch'] == 'on':
            wprint.wprint('-3-开启操作')
            # 开启
            if switch.state() != 'on':
                switch.switch('on')
        elif data['data'][0]['switch'] == 'off':
            wprint.wprint('-4-关闭操作')
            # 关闭
            # wprint.wprint(switch.state())
            if switch.state() != 'off':
                switch.switch('off')
    elif data['request_type'] == 'check':
        wprint.wprint('-5-查看操作')
        # 初始化参数
        message_data = {
            'name' : 'mcsm_return',
            'request_type' : 'return_data',
            'data' : [{
                'switch' : 'on' # 开关 on开启 off关闭
            }], 
        }

        # 查看状态
        if switch.state() == 'on':
            message_data['data'][0]['switch'] = 'on'
        elif switch.state() == 'off':
            message_data['data'][0]['switch'] = 'off'
        
        # 保存结果
        保存结果(message_data)


while True:
    time.sleep(0.1)
    # 遍历文件
    file_list = os.listdir(根目录)
    for file in file_list:
        # wprint.wprint(file)
        if 'mcsm_sw' in file:
            result = re.search(r'-(.*?)-', file)
            if result:
                wprint.wprint(result.group(1))
                with open(根目录 + '/' + file, 'r') as f:
                    data = json.load(f)
                os.remove(根目录 + '/' + file)
                thread1 = threading.Thread(target=执行, args=(data,))
                thread1.start()
            
            
