from django.contrib import admin
from django.urls import path

from . import menu

urlpatterns = [
    
    # path("", Login.Login), # 登录界面
    path("User_Agreement.txt/", menu.User_Agreement_txt), 
    path("menu/", menu.menu), # 功能菜单（开始菜单）
]
