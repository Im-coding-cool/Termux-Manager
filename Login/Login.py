from django.http import HttpResponse
from django.shortcuts import render
 
def Login(request):
    request.encoding='utf-8'
    if 'key' in request.GET:
        if request.GET['key'] == "chen":
            context = '设备已注册，点击跳转到管理菜单>>><a href="/menu">点我进入管理</a>'
            pass
        else:
            context = '密钥错误，请重试'
    else:
        context = '请输入内测密钥'

    return render(request, 'Login.html', {"context": context})