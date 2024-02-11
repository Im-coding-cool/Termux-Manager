import subprocess
import os
import wprint

# 执行器
class actuator:
    def __init__(self) -> None:
        pass

    # 查找node.js进程
    def get_nodejs_pids():
        try:
            output = subprocess.check_output(['pgrep', '-a', 'node'])
            lines = output.decode('utf-8').split('\n')
            pids = [line.split()[0] for line in lines if 'node app.js' in line]
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
class mcsm_controller:
    def __init__(self) -> None:
        self.sta = 'off'

    # 开关控制
    def switch(self, sw):
        if sw == 'on':
            # 开启
            subprocess.Popen(["nohup", "sh", "on_mcsm.sh", "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        elif sw == 'off':
            # 关闭
            nodejs_pids = actuator.get_nodejs_pids() # 获取node.js PID
            for pid in nodejs_pids: # 遍历所有node.js进程，包括前后端
                actuator.kill_process(pid) # 关闭对应PID

    # 用于判断是否包含PID
    def contains_digit(input_str):
        for char in input_str:
            if char.isdigit():
                return True
        return False

    # 查看状态
    def state(self):
        wprint.wprint('查看状态')
        self.sta = 'off'
        nodejs_pids = actuator.get_nodejs_pids() # 获取node.js PID
        for pid in nodejs_pids: # 遍历所有node.js进程，包括前后端
            wprint.wprint('发现PID: ' + pid)
            self.sta = 'on'
        return self.sta

    # 修改器
    def revise(self):
        pass



# cd /opt/mcsmanager/ && ./start-daemon.sh & cd /opt/mcsmanager/ && ./start-web.sh &