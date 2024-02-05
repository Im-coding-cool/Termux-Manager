from django.contrib import admin
from django.urls import path

from . import server

urlpatterns = [
    path("server_menu/", server.server_menu), # 服务器功能配置菜单
    path("MCSM_server/", server.MCSM_server), # MCSM服务开关
    path('Frp', server.Frp_server)
]
