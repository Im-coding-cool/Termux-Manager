import subprocess
import threading
import global_configuration

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

    print('\033[32m+服务开启完毕\033[0m')
    print('请访问:\033[4m\033[31mhttp://0.0.0.0:8000/\033[0m\033[24m进入配置')
    print('默认密钥为:\033[31mchen\033[0m')



