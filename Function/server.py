from django.http import HttpResponse
from django.shortcuts import render
from api.api import request_result
from api.p_rint import print_p
from api.wprint import wprint

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
    na = 'server.py里的MCSM_server'
    message_data = {
        'name' : 'frp_sw', # 名称 mcsm_sw
        'request_type' : 'check', # 请求类型 task(任务) check(查看)
    }
    # 获取运行状态
    data = request_result(message_data)
    if '超时' in data:
        state = '连接超时，状态拉取失败'
    else:
        if data['data'][0]['switch'] == 'off':
            state = '服务关闭'
        elif data['data'][0]['switch'] == 'on':
            state = '服务运行中'
    config = data['data'][0]['config'].replace('\n', '\\n')

    return render(request, 'Frp.html', {'con' : "function_menu.html", 'state' : state, 'config' : config})