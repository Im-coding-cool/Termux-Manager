import subprocess
import time
import threading
import sqlite3
import configparser
from datetime import datetime
import os

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
ROOT_PATH = global_config.get('mcserver', 'root_path')
PROOT_PATH = global_config.get('mcserver', 'proot_path')
DEFAULT_ROOT_PATH = global_config.get('default', 'root_path')

# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取INI文件
config.read(ROOT_PATH + 'main/config.ini')

# 执行命令并创建伪终端
proc = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# 初始化终端输出
data = ''
whether_run = True

def listener():
    global data
    id = config.get('config', 'id')
    
    while whether_run:
        output = proc.stdout.readline() # 获取输出
        if output == '' and proc.poll() is not None:
            break
        data = data + output
        wdatabase(id, data)

def error_monitoring():
    global data
    id = config.get('config', 'id')
    while whether_run:
        error_output = proc.stderr.readline() # 获取错误输出
        if error_output:
            data = data + error_output
            wdatabase(id, data)

def wdatabase(id, output):
    # 链接数据库
    dlink = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
    cur = dlink.cursor()

    # 执行 SELECT 查询
    cur.execute("SELECT * FROM items WHERE id=?", (id,))
    row = cur.fetchone()

    if row:
        # 如果存在就修改
        cur.execute("UPDATE items SET output = ?, state = ? WHERE id = ?", (output, 'ON', id))
    else:
        # 如果不存在就创建
        name = config.get('config', 'name')
        id = config.get('config', 'id')
        pid = os.getpid()
        current_time = datetime.now()
        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO items (id, pid, name, state, last_online, run_command, output) VALUES (?, ?, ?, ?, ?, ?, ?);", (id, pid, name, 'ON', formatted_current_time, None, '项目还没有启动过'))
    dlink.commit()
    dlink.close()


def record_time():
    id = config.get('config', 'id')
    while whether_run:
        time.sleep(1)
        current_time = datetime.now()
        formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        pid = os.getpid()
        print(formatted_current_time,'> pid:',pid)
        # 链接数据库
        dlink = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
        cur = dlink.cursor()

        # 执行 SELECT 查询
        cur.execute("SELECT * FROM items WHERE id=?", (id,))
        row = cur.fetchone()

        if row:
            # 如果存在就修改
            cur.execute("UPDATE items SET last_online = ?, pid = ?, state = ? WHERE id = ?", (formatted_current_time, pid, 'ON', id))
        else:
            # 如果不存在就创建
            name = config.get('config', 'name')
            id = config.get('config', 'id')
            pid = os.getpid()
            current_time = datetime.now()
            formatted_current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("INSERT INTO items (id, pid, name, state, last_online, run_command, output) VALUES (?, ?, ?, ?, ?, ?, ?);", (id, pid, name, 'ON', formatted_current_time, None, '项目还没有启动过'))
        dlink.commit()
        dlink.close()

def run_command():
    global data
    id = config.get('config', 'id')
    while whether_run:
        time.sleep(0.05)
        # 链接数据库
        dlink = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
        cur = dlink.cursor()
        # 执行 SELECT 查询
        cur.execute("SELECT * FROM items WHERE id=?", (id,))
        row = cur.fetchone()

        if row:
            # 如果存在就读取
            cur.execute("SELECT * FROM items WHERE id=?", (id,))
            row = cur.fetchone()
            if row[5] != None:
                id = config.get('config', 'id')
                cur.execute("UPDATE items SET run_command = ? WHERE id = ?", (None, id))
                dlink.commit()
                print('>', row[5])
                data = data + '> ' + row[5] + '\n'
                wdatabase(id, data)
                dlink.commit()
                proc.stdin.write(row[5] + "\n")
                proc.stdin.flush()
        else:
            pass
        dlink.close()
        


if __name__ == "__main__":
    # 初始化清空数据库
    wdatabase(config.get('config', 'id'), '')

    # 记录命令输出
    th = threading.Thread(target=listener)
    th.start()

    # 记录错误输出
    error_mon = threading.Thread(target=error_monitoring)
    error_mon.start()

    # 刷新时间
    rtime = threading.Thread(target=record_time)
    rtime.start()

    # 执行命令
    runcom = threading.Thread(target=run_command)
    runcom.start()

    # 执行命令
    proc.stdin.write("sudo proot -0 -r /home/chen/proot/ubuntu/ -w /root bash")
    proc.stdin.flush()








