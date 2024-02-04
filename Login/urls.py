from django.contrib import admin
from django.urls import path

from . import Login

urlpatterns = [
    
    path("", Login.Login), # 登录界面
    # path("menu/", function_list.menu), # 功能菜单（开始菜单）
]
