from django.http import HttpResponse
from django.shortcuts import render
from api.api import request_result
from api.p_rint import print_p
from api.wprint import wprint
from django.http import JsonResponse
import subprocess
import os
import sqlite3




from datetime import datetime, timedelta

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





def server_menu(request):
    # 服务器功能选择菜单
    return render(request, 'server_menu.html')

def MCSM_server(request): # MCSM管理
    na = 'server.py里的MCSM_server'
    message_data = {
        'name' : 'mcsm_sw', # 名称 mcsm_sw
        'request_type' : 'check', # 请求类型 task(任务) check(查看)
    }
    # 获取运行状态
    data = request_result(message_data)
    if '超时' in data:
        data = '连接超时，状态拉取失败'
    else:
        if data['data'][0]['switch'] == 'off':
            data = '服务关闭'
        elif data['data'][0]['switch'] == 'on':
            data = '服务运行中'
            
    return render(request, 'MCSM_server.html', {'con' : "function_menu.html", 'state' : data})

# Frp管理   
def Frp_server(request):
    if request.method=='GET':
        na = 'server.py里的MCSM_server'
        message_data = {
            'name' : 'frp_sw', # 名称 mcsm_sw
            'request_type' : 'check', # 请求类型 task(任务) check(查看)
        }
        # 获取运行状态
        data = request_result(message_data)
        if '超时' in data:
            state = '连接超时，状态拉取失败'
            config = '连接超时，状态拉取失败'
        else:
            if data['data'][0]['switch'] == 'off':
                state = '服务关闭'
            elif data['data'][0]['switch'] == 'on':
                state = '服务运行中'
            config = data['data'][0]['config'].replace('\n', '\\n')

        return render(request, 'Frp.html', {'con' : "function_menu.html", 'state' : state, 'config' : config})
    else:
        if request.POST['type'] == 'revise':
            message_data = {
                'name' : 'frp_sw', # 名称 mcsm_sw
                'request_type' : 'revise',
                'data' : [{
                    'config' : request.POST['config']
                }]
            }
            # 保存参数
            data = request_result(message_data)
            return render(request, 'api.html', {})
        elif request.POST['type'] == 'switch':
            message_data = {
                'name' : 'frp_sw', # 名称 mcsm_sw
                'request_type' : 'task',
                'data' : [{
                    'switch' : request.POST['switch']
                }]
            }
            # 保存参数
            data = request_result(message_data)
            return render(request, 'api.html', {})
        elif request.POST['type'] == 'log':
            with open(FRP_PATH + 'frpc/nohup.out', 'r') as file: 
                content = file.read()
            data = {'log' : content}
            return JsonResponse(data)
    


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
                    parsed_time = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')

                    current_dateTime = datetime.now()

                    aa = current_dateTime - parsed_time
                    print(aa.total_seconds())
                    if aa.total_seconds() > 5:
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
                        parsed_time = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')

                        current_dateTime = datetime.now()

                        aa = current_dateTime - parsed_time
                        print(aa.total_seconds())
                        if aa.total_seconds() > 5:
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