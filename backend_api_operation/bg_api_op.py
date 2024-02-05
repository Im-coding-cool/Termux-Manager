from django.http import HttpResponse
from django.shortcuts import render
from api.api import start_task, request_result
 
def get_api(request): # 后端API_GET接口
    if request.method=='GET':
        request.encoding='utf-8'
        if 'type' in request.GET:
            if request.GET['type'] == "mcsm_off_on":
                if request.GET['call'] == "no":
                    context = "开启MCSM"
                    message_data = {
                        'name' : 'mcsm_sw', # 名称 mcsm_sw
                        'request_type' : 'task', # 请求类型 task(任务) check(查看)

                        # 任务详情 data(任务数据)
                        'data' : [{
                            'switch' : 'on' # 开关 on开启 off关闭
                        }], 
                    }
                    # 发送任务到后台
                    start_task(message_data)
                elif request.GET['call'] == "off":
                    context = "关闭MCSM"
                    message_data = {
                        'name' : 'mcsm_sw', # 名称 mcsm_sw
                        'request_type' : 'task', # 请求类型 task(任务) check(查看)

                        # 任务详情 data(任务数据)
                        'data' : [{
                            'switch' : 'off' # 开关 on开启 off关闭
                        }], 
                    }
                    # 发送任务到后台
                    start_task(message_data)
            elif request.GET['type'] == "frp": # Frp操作
                if request.GET['call'] == "no":
                    context = "开启frp"
                    message_data = {
                        'name' : 'frp_sw', # 名称
                        'request_type' : 'task', # 请求类型 task(任务) check(查看)

                        # 任务详情 data(任务数据)
                        'data' : [{
                            'switch' : 'on' # 开关 on开启 off关闭
                        }], 
                    }
                    # 发送任务到后台
                    start_task(message_data)
                elif request.GET['call'] == "off":
                    context = "关闭frp"
                    message_data = {
                        'name' : 'frp_sw', # 名称
                        'request_type' : 'task', # 请求类型 task(任务) check(查看)

                        # 任务详情 data(任务数据)
                        'data' : [{
                            'switch' : 'off' # 开关 on开启 off关闭
                        }], 
                    }
                    # 发送任务到后台
                    start_task(message_data)
            else:
                context = '未注册类型'
        else:
            context = ''
    else:
        if request.POST['name'] == 'frp_write':
            message_data = {
                'name' : 'frp_write', # 名称
                'request_type' : 'write',

                # 任务详情 data(任务数据)
                'data' : request.POST['data'], 
            }
            # 发送任务到后台
            start_task(message_data)

    return render(request, 'api.html', {'api' : context})