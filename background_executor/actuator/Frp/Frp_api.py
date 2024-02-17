import subprocess
import os
import time

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
PATH = global_config.get('rear_end', 'path')
根目录 = PATH + 'data'# 数据交换目录
frp_path = PATH + 'actuator/Frp/frpc' # frp可执行文件根路径


# 执行器
class actuator:
    def __init__(self) -> None:
        pass

    # 查找frpc进程
    def get_frp_pids():
        try:
            output = subprocess.check_output(['pgrep', '-a', 'frpc'])
            lines = output.decode('utf-8').split('\n')
            pids = [line.split()[0] for line in lines if '/home/chen/termux-manager/background_executor/actuator/Frp/frpc/frpc -c /home/chen/termux-manager/background_executor/actuator/Frp/frpc/frpc.toml' in line]
            return pids
        except subprocess.CalledProcessError:
            return []
            
    # 通过PID强制关闭进程
    def kill_process(pid):
        try:
            subprocess.run(['kill','-9', pid])
            print(f"已关闭进程PID {pid}")
        except subprocess.CalledProcessError as e:
            print(f"关闭进程PID {pid} 失败：", e)


# MCSM控制器
class frp_controller:
    def __init__(self) -> None:
        self.sta = 'off'

    # 开关控制
    def switch(self, sw):
        if sw == 'on':
            # 开启
            print('frp开启')
            subprocess.run("nohup sh /home/chen/termux-manager/background_executor/actuator/Frp/frpc/qi.sh > /home/chen/termux-manager/background_executor/actuator/Frp/frpc/nohup.out 2>&1 &", shell=True)
        elif sw == 'off':
            # 关闭
            print('frp关闭')
            nodejs_pids = actuator.get_frp_pids() # 获取frp PID
            for pid in nodejs_pids: # 遍历所有frp进程，包括前后端
                actuator.kill_process(pid) # 关闭对应PID

    # 用于判断是否包含PID
    def contains_digit(input_str):
        for char in input_str:
            if char.isdigit():
                return True
        return False

    # 查看状态
    def state(self):
        print('查看状态')
        self.sta = 'off'
        nodejs_pids = actuator.get_frp_pids() # 获取frp.js PID
        for pid in nodejs_pids: # 遍历所有frpc进程，包括前后端
            print('发现PID:', pid)
            self.sta = 'on'
        
        # 返回数据
        message_data = {
            'name' : 'frp_return',
            'request_type' : 'return_data',
            'data' : [{
                'switch' : 'off',
                'config' : '# 错误',
            }], 
        }

        # 查看状态
        if self.sta == 'on':
            message_data['data'][0]['switch'] = 'on'
        elif self.sta == 'off':
            message_data['data'][0]['switch'] = 'off'

        # 查看配置文件
        with open(frp_path + '/' + 'frpc.ini', 'r', encoding='utf-8') as file:
            content = file.read()
        message_data['data'][0]['config'] = content

        return message_data

    # 修改器
    def revise(self, data):
        with open(frp_path + '/frpc.ini', 'w', encoding='utf-8') as file:
            file.write(data['data'][0]['config'])



# cd /opt/mcsmanager/ && ./start-daemon.sh & cd /opt/mcsmanager/ && ./start-web.sh &