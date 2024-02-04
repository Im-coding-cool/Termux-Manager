import subprocess
import os



class mcsm_s:
    def __init__(self) -> None:
        pass

    def get_nodejs_pids():
        try:
            output = subprocess.check_output(['pgrep', '-a', 'node'])
            lines = output.decode('utf-8').split('\n')
            pids = [line.split()[0] for line in lines if 'node app.js' in line]
            return pids
        except subprocess.CalledProcessError:
            return []

    def kill_process(pid):
        try:
            subprocess.run(['kill','-9', pid])
            print(f"已关闭进程PID {pid}")
        except subprocess.CalledProcessError as e:
            print(f"关闭进程PID {pid} 失败：", e)

    def on(self):
        # # 执行连续的命令
        # commands = [
        #     # 登录容器
        #     'proot-distro login ubuntu',
        #     # 执行开启命令
        #     'cd /opt/mcsmanager/ && ./start-daemon.sh & ./start-web.sh & ls'
        # ]
        # # 通过管道连接多个命令
        # process = subprocess.Popen(' && '.join(commands), shell=True)
        # process.wait()
        # print("已开启MCSM")
        pass

    def off(self):
        nodejs_pids = mcsm_s.get_nodejs_pids() # 获取node.js PID
        for pid in nodejs_pids: # 遍历所有node.js进程，包括前后端
            mcsm_s.kill_process(pid) # 关闭对应PID


    def state(self, sw):
        if sw == "on":     
            mcsm_s.on(self) # 开启MCSM面板
        elif sw == "off":
            mcsm_s.off(self) # 关闭MCSM
        else:
            print("传参错误")

