# 引入shell仿真模块
import subprocess

# shell调用
class shell_c:
    def __init__(self) -> None:
        self.end = ""

    # 执行系统命令
    def shell_call(self, shell_command):
        # 执行 shell_command 命令并获取实时输出
        output = []
        process = subprocess.Popen(shell_command, stdout=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout: # 获取结果
            # print(line, end='')
            output.append(line)
        # 等待 shell_command 命令执行完毕
        process.wait()
        
        # 保存结果
        self.end = output
        return self.end


# 系统信息
class sysmsg:
    def __init__(self) -> None:
        self.ram = '' # 内存信息
        self.name = '' # 

    
    # 获取内存信息
    def ram_info(self):
        ram = shell_c() # 注册类
        self.ram = ram.shell_call(['systeminfo']) # 获取内存大小
        return ram.end # 返回结果
    
    # 获取终端名称
    def shell_name(self):
        name_x = shell_c() # 注册类
        self.name = name_x.shell_call(['ping', '127.0.0.1']) # 获取名称
        return name_x.end
    

# 开关操作
class shell_switch:
    def __init__(self) -> None:
        self._mcsm_switch = 'off' # mcsm开关状态

    def mcsm_switch(self, switch_off_on):
        switch = shell_c() # 注册shell控制器
        if switch_off_on == 'no': # 判断用户想要开启还是关闭
            if switch.shell_call(['ipconfig']) in "0":
                # 开启操作
                switch.shell_call(['ping']) # 执行开启命令
                self._mcsm_switch = 'on' # 设置开关变量状态
                return self._mcsm_switch # 执行开启命令
        else:
            if switch.shell_call(['ipconfig']) in "1":
                # 关闭操作
                switch.shell_call(['ping']) # 执行关闭s命令
                self._mcsm_switch = 'off' # 设置开关变量状态
                return self._mcsm_switch # 执行开启命令