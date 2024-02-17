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

def cl(name, sh):
    # 打开日志文件以追加模式写入
    with open(LOG_PATH + name + '.log', 'a') as f:
        # 使用Popen执行命令并实时记录输出
        process = subprocess.Popen(sh, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='', file=f, flush=True)  # 将输出写入日志文件


if __name__ == "__main__":
    th = threading.Thread(target=cl, args=('front_end','python3 ' + front_end_path + 'manage.py runserver 0.0.0.0:8000'))
    th.start()

    th2 = threading.Thread(target=cl, args=('rear_end','python3 ' + rear_end_path + 'main.py'))
    th2.start()

    print('服务开启完毕')


