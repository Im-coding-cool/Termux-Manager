from django.http import HttpResponse
from django.shortcuts import render
from api.api import request_result
from api.p_rint import print_p

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
    while True:
        try:
            if data[0]['switch'] == 'on':
                data = '运行中'
                break
            elif data[0]['switch'] == 'off':
                data = '已关闭'
                break
        except:
            if data == '超时':
                data = '状态获取失败,超时'
                break
            elif data == '连接出错':
                data = '连接出错'
            
    return render(request, 'function_menu.html', {'con' : "MCSM_server.html", 'state' : data})

# Frp管理
def Frp_server(request):
    pass
    return render(request, 'Frp.html') # , {'con' : "MCSM_server.html", 'state' : data}