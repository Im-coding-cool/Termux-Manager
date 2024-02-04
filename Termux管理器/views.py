from django.http import HttpResponse
from django.shortcuts import render
 
def Login(request):
    request.encoding='utf-8'
    context          = {}
    if 'key' in request.GET:
        if request.GET['key'] == "chen":
            # context['hint'] = '密钥正确'
            pass
        else:
            context['hint'] = '密钥错误，请重试'
    else:
        context['hint'] = '请输入内测密钥'
    return render(request, 'Login.html', context)