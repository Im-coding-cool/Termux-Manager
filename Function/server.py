from django.http import HttpResponse
from django.shortcuts import render
from api.api import request_result
from api.p_rint import print_p
from api.wprint import wprint
from django.http import JsonResponse
import subprocess
import os
import sqlite3
from django.utils import timezone
from datetime import datetime
import threading



import configparser

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
FRP_PATH = global_config.get('frp', 'root_path')
DEFAULT_ROOT_PATH = global_config.get('default', 'root_path')
TERMUX = global_config.get('config', 'termux')
TIME_RECORDER_PATH = global_config.get('time_recorder', 'time_recorder_root_path')
MCSERVER_ROOT_PATH = global_config.get('mcserver', 'root_path')
FRPSERVER_ROOT_PATH = global_config.get('frpserver', 'root_path')

def calculatetimedifference(tm):
    # 运行sh脚本在django外计算时间差
    result = subprocess.run(['sh', TIME_RECORDER_PATH + 'time_recorder.sh', '-time', tm], stdout=subprocess.PIPE)
    # 获取结果并去掉换行和空格
    output = result.stdout.decode('utf-8').strip()
    output = output.replace("\n", "").replace(" ", "")
    print('时间差: ',output)
    return int(output)

def current_time():
    # 连接到数据库
    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
    cursor = conn.cursor()

    # 执行 SELECT 查询
    cursor.execute("SELECT * FROM current_time WHERE id=?", (1,))
    row = cursor.fetchone()
    im = None

    if row:
        print(row[2])  # 如果存在则输出该条目
        im = row[2]
    else:
        print("当前时间条目未找到")  # 否则输出未找到的消息

    # 关闭连接
    conn.close()
    return im


def server_menu(request):
    # 服务器功能选择菜单
    return render(request, 'server_menu.html')

def MCSM_server(request): # MCSM管理
    if request.method=='GET':
        request.encoding='utf-8'
        if 'id' in request.GET:
            html = render(request, 'mcserver_editing.html', {'con' : "function_menu.html", 'id' : request.GET['id']})
        else:
            html = render(request, 'MCSM_server.html', {'con' : "function_menu.html"})
    else:
        if request.POST['name'] == 'editing':
            if request.POST['type'] == 'terminal':
                # 连接到数据库
                conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                cursor = conn.cursor()

                # 执行 SELECT 查询
                cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                row = cursor.fetchone()

                if row:
                    # print(row[6])  # 如果存在则输出该条目
                    # 计算时间差
                    aa = calculatetimedifference(row[4])

                    if aa > 5:
                        html = JsonResponse({'data' : '暂无输出或终端内容过期\n'})
                    else:
                        html = JsonResponse({'data' : row[6]})
                else:
                    print("条目未找到")  # 否则输出未找到的消息
                    html = JsonResponse({'data' : 'NULL'})
                # 关闭连接
                conn.close()
            elif request.POST['type'] == 'run_command':
                # 连接到数据库
                conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                cursor = conn.cursor()

                # 执行 SELECT 查询
                cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                row = cursor.fetchone()

                if row:
                    # 如果存在就修改
                    cursor.execute("UPDATE items SET run_command = ? WHERE id = ?", (request.POST['command'], request.POST['id']))
                else:
                    print("条目未找到")

                # 关闭连接
                conn.commit()
                conn.close()
                data = {'OK': 'OK'}
                html = JsonResponse(data)
            elif request.POST['type'] == 'sw':
                if request.POST['sw'] == 'ON':
                    # 连接到数据库
                    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                    cursor = conn.cursor()

                    # 执行 SELECT 查询
                    cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                    row = cursor.fetchone()

                    if row:
                        # print(row[6])  # 如果存在则输出该条目
                        # 计算时间差
                        aa = calculatetimedifference(row[4])

                        if aa > 5:
                            print('MCSM_server:', '启动')
                            html = JsonResponse({'sw' : '已执行开启命令\n', 'NULL' : aa})
                            subprocess.Popen(["python3", MCSERVER_ROOT_PATH + "main/start.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        else:
                            print('MCSM_server:', '已经在运行中')
                            html = JsonResponse({'sw' : '已经在运行中', 'NULL' : aa})
                    else:
                        print('MCSM_server:', '启动2')
                        html = JsonResponse({'sw' : '已执行开启命令2\n'})
                        subprocess.Popen(["python3", MCSERVER_ROOT_PATH + "main/start.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # 关闭连接
                    conn.close()
                elif request.POST['sw'] == 'OFF':
                    # 连接到数据库
                    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                    cursor = conn.cursor()

                    # 执行 SELECT 查询
                    cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                    row = cursor.fetchone()

                    if row:
                        # print(row[6])  # 如果存在则输出该条目
                        try:
                            print('PID:', row[1])
                            subprocess.run(['kill','-9', str(row[1])])
                            print(f"已关闭进程PID {row[1]}")
                            html = JsonResponse({'sw' : f"已关闭进程PID {row[1]}"})
                        except subprocess.CalledProcessError as e:
                            print(f"关闭进程PID {row[1]} 失败：", e)
                            html = JsonResponse({'sw' : f"关闭进程PID {row[1]} 失败："})
                    else:
                        print("条目未找到")  # 否则输出未找到的消息
                        html = JsonResponse({'sw' : 'NULL'})
        else:
            data = {'NULL': 'NULL'}
            print('ser:', 'NULL')
            html = JsonResponse(data)
    return html

# Frp管理   
def Frp_server(request):
    if request.method=='GET':
        request.encoding='utf-8'
        if 'id' in request.GET:
            html = render(request, 'frpserver_editing.html', {'con' : "function_menu.html", 'id' : request.GET['id']})
        else:
            html = render(request, 'Frp.html', {'con' : "function_menu.html"})
        return html
    else:
        if request.POST['name'] == 'editing':
            if request.POST['type'] == 'terminal':
                # 连接到数据库
                conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                cursor = conn.cursor()

                # 执行 SELECT 查询
                cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                row = cursor.fetchone()

                if row:
                    # print(row[6])  # 如果存在则输出该条目
                    # 计算时间差
                    aa = calculatetimedifference(row[4])

                    if aa > 5:
                        html = JsonResponse({'data' : '暂无输出或终端内容过期\n'})
                    else:
                        html = JsonResponse({'data' : row[6]})
                else:
                    print("条目未找到")  # 否则输出未找到的消息
                    html = JsonResponse({'data' : 'NULL'})
                # 关闭连接
                conn.close()
            elif request.POST['type'] == 'run_command':
                # 连接到数据库
                conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                cursor = conn.cursor()

                # 执行 SELECT 查询
                cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                row = cursor.fetchone()

                if row:
                    # 如果存在就修改
                    cursor.execute("UPDATE items SET run_command = ? WHERE id = ?", (request.POST['command'], request.POST['id']))
                else:
                    print("条目未找到")

                # 关闭连接
                conn.commit()
                conn.close()
                data = {'OK': 'OK'}
                html = JsonResponse(data)
            elif request.POST['type'] == 'sw':
                if request.POST['sw'] == 'ON':
                    # 连接到数据库
                    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                    cursor = conn.cursor()

                    # 执行 SELECT 查询
                    cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                    row = cursor.fetchone()

                    if row:
                        # print(row[6])  # 如果存在则输出该条目
                        # 计算时间差
                        aa = calculatetimedifference(row[4])

                        if aa > 5:
                            print('frpserver:', '启动')
                            html = JsonResponse({'sw' : '已执行开启命令\n', 'NULL' : aa})
                            subprocess.Popen(["python3", FRPSERVER_ROOT_PATH + "main/start.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        else:
                            print('frpserver:', '已经在运行中')
                            html = JsonResponse({'sw' : '已经在运行中', 'NULL' : aa})
                    else:
                        print('frpserver:', '启动2')
                        html = JsonResponse({'sw' : '已执行开启命令2\n'})
                        subprocess.Popen(["python3", FRPSERVER_ROOT_PATH + "main/start.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    # 关闭连接
                    conn.close()
                elif request.POST['sw'] == 'OFF':
                    # 连接到数据库
                    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                    cursor = conn.cursor()

                    # 执行 SELECT 查询
                    cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                    row = cursor.fetchone()

                    if row:
                        # print(row[6])  # 如果存在则输出该条目
                        try:
                            print('PID:', row[1])
                            subprocess.run(['kill','-9', str(row[1])])
                            print(f"已关闭进程PID {row[1]}")
                            html = JsonResponse({'sw' : f"已关闭进程PID {row[1]}"})
                        except subprocess.CalledProcessError as e:
                            print(f"关闭进程PID {row[1]} 失败：", e)
                            html = JsonResponse({'sw' : f"关闭进程PID {row[1]} 失败："})
                    else:
                        print("条目未找到")  # 否则输出未找到的消息
                        html = JsonResponse({'sw' : 'NULL'})
        elif request.POST['name'] == 'config':
            if request.POST['type'] == 'r': # 读取
                if TERMUX == 'true':
                    with open(FRPSERVER_ROOT_PATH + 'frpc/termux/frpc.toml', 'r', encoding='utf-8') as file: 
                        content = file.read() 
                elif TERMUX == 'false':
                    with open(FRPSERVER_ROOT_PATH + 'frpc/wsl/frpc.toml', 'r', encoding='utf-8') as file: 
                        content = file.read() 
                data = {'r': content}
                html = JsonResponse(data)
            elif request.POST['type'] == 'w': # 写入
                if TERMUX == 'true':
                    with open(FRPSERVER_ROOT_PATH + 'frpc/termux/frpc.toml', 'w', encoding='utf-8') as f:
                        f.write(request.POST['data'])
                elif TERMUX == 'false':
                    with open(FRPSERVER_ROOT_PATH + 'frpc/wsl/frpc.toml', 'w', encoding='utf-8') as f:
                        f.write(request.POST['data'])
                data = {'OK': 'W_OK'}
                html = JsonResponse(data)
            else:
                data = {'config': 'NULL'}
                html = JsonResponse(data)
        else:
            data = {'NULL': 'NULL'}
            print('ser:', 'NULL')
            html = JsonResponse(data)
    return html
    


def default_man(request):
    
    if request.method=='GET':
        request.encoding='utf-8'
        if 'id' in request.GET:
            i = False
            list_dir = os.listdir(DEFAULT_ROOT_PATH + 'default/')
            for temp in list_dir:
                fe = DEFAULT_ROOT_PATH + 'default/' + temp + '/config.ini'
                if os.path.exists(fe):
                    # 创建ConfigParser对象
                    config = configparser.ConfigParser()
                    # 读取INI文件
                    config.read(fe)
                    # 获取特定section中的值
                    if config.get('config', 'id') == request.GET['id']:
                        i = True
                        html = render(request, 'default_editing.html', {'con' : "function_menu.html", 'id' : request.GET['id']})
            if i == False:
                html = render(request, 'default_management.html', {'con' : "function_menu.html"})
        else:
            html = render(request, 'default_management.html', {'con' : "function_menu.html"})
    else:
        if request.POST['name'] == 'default_man':
            print('ser:', 'POST')
            data = {}
            list_dir = os.listdir(DEFAULT_ROOT_PATH + 'default/')
            for temp in list_dir:
                fe = DEFAULT_ROOT_PATH + 'default/' + temp + '/config.ini'
                if os.path.exists(fe):
                    # 创建ConfigParser对象
                    config = configparser.ConfigParser()
                    # 读取INI文件
                    config.read(fe)
                    # 获取特定section中的值
                    value = config.get('config', 'name')
                    data[temp] = {
                        'name' : value,
                        'id' : config.get('config', 'id'),
                        'introduce' : config.get('config', 'introduce')
                    }
            html = JsonResponse(data)
        elif request.POST['name'] == 'default_editing':
            if request.POST['type'] == 'terminal':
                # 连接到数据库
                conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                cursor = conn.cursor()

                # 执行 SELECT 查询
                cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                row = cursor.fetchone()

                if row:
                    # print(row[6])  # 如果存在则输出该条目
                    # 计算时间差
                    aa = calculatetimedifference(row[4])

                    print(aa)
                    if aa > 5:
                        html = JsonResponse({'data' : '暂无输出或终端内容过期\n'})
                    else:
                        html = JsonResponse({'data' : row[6]})
                else:
                    print("条目未找到")  # 否则输出未找到的消息
                    html = JsonResponse({'data' : 'NULL'})
                # 关闭连接
                conn.close()
            elif request.POST['type'] == 'run_command':
                # 连接到数据库
                conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                cursor = conn.cursor()

                # 执行 SELECT 查询
                cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                row = cursor.fetchone()

                if row:
                    # 如果存在就修改
                    cursor.execute("UPDATE items SET run_command = ? WHERE id = ?", (request.POST['command'], request.POST['id']))
                else:
                    print("条目未找到")

                # 关闭连接
                conn.commit()
                conn.close()
                data = {'OK': 'OK'}
                html = JsonResponse(data)
            elif request.POST['type'] == 'sw':
                if request.POST['sw'] == 'ON':
                    # 连接到数据库
                    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                    cursor = conn.cursor()

                    # 执行 SELECT 查询
                    cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                    row = cursor.fetchone()

                    if row:
                        # print(row[6])  # 如果存在则输出该条目
                        # 计算时间差
                        aa = calculatetimedifference(row[4])

                        print(aa)
                        if aa > 5:
                            html = JsonResponse({'sw' : '已执行开启命令\n'})
                            list_dir = os.listdir(DEFAULT_ROOT_PATH + 'default/')
                            for temp in list_dir:
                                fe = DEFAULT_ROOT_PATH + 'default/' + temp + '/config.ini'
                                if os.path.exists(fe):
                                    # 创建ConfigParser对象
                                    config = configparser.ConfigParser()
                                    # 读取INI文件
                                    config.read(fe)
                                    if config.get('config', 'id') == request.POST['id']:
                                        subprocess.Popen(["python3", DEFAULT_ROOT_PATH + "default/" + temp + "/start.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                        # subprocess.Popen(["cd",'/home/chen/termux-manager/default/default/' + temp + '/', '&&',"nohup", "python3", "start.py", "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
                        else:
                            html = JsonResponse({'sw' : '已经在运行中'})
                    else:
                        html = JsonResponse({'sw' : '已执行开启命令\n'})
                        list_dir = os.listdir(DEFAULT_ROOT_PATH + 'default/')
                        for temp in list_dir:
                            fe = DEFAULT_ROOT_PATH + 'default/' + temp + '/config.ini'
                            if os.path.exists(fe):
                                # 创建ConfigParser对象
                                config = configparser.ConfigParser()
                                # 读取INI文件
                                config.read(fe)
                                if config.get('config', 'id') == request.POST['id']:
                                    print(["cd", DEFAULT_ROOT_PATH + 'default/' + temp + '/', '&&',"nohup", "python3", "start.py", "&"])
                                    # 后台运行 Python 脚本
                                    subprocess.Popen(["python3", DEFAULT_ROOT_PATH + "default/" + temp + "/start.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                                    # subprocess.Popen(["cd",'/home/chen/termux-manager/default/default/' + temp + '/', '&&',"nohup", "python3", "start.py", "&"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
                    # 关闭连接
                    conn.close()
                elif request.POST['sw'] == 'OFF':
                    # 连接到数据库
                    conn = sqlite3.connect(DEFAULT_ROOT_PATH + 'database/data.db')
                    cursor = conn.cursor()

                    # 执行 SELECT 查询
                    cursor.execute("SELECT * FROM items WHERE id=?", (request.POST['id'],))
                    row = cursor.fetchone()

                    if row:
                        # print(row[6])  # 如果存在则输出该条目
                        try:
                            print('PID:', row[1])
                            subprocess.run(['kill','-9', str(row[1])])
                            print(f"已关闭进程PID {row[1]}")
                            html = JsonResponse({'sw' : f"已关闭进程PID {row[1]}"})
                        except subprocess.CalledProcessError as e:
                            print(f"关闭进程PID {row[1]} 失败：", e)
                            html = JsonResponse({'sw' : f"关闭进程PID {row[1]} 失败："})
                    else:
                        print("条目未找到")  # 否则输出未找到的消息
                        html = JsonResponse({'sw' : 'NULL'})
        else:
            data = {'NULL': 'NULL'}
            print('ser:', 'NULL')
            html = JsonResponse(data)
    return html
