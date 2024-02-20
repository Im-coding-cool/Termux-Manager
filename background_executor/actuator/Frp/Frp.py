import os
import wprint
import re
import threading
import time

import actuator.Frp.Frp_api as Frp_api
switch = Frp_api.frp_controller() # 注册控制器

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


# 数据交换目录
根目录 = PATH + 'data'


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
        return switch.state()
    elif data['request_type'] == 'revise': # 修改配置文件
        switch.revise(data)
        return json.dumps(data)

            
            



