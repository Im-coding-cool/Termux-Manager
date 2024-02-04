from django.contrib import admin
from django.urls import path

from . import bg_api_op

urlpatterns = [
    
    path("api/", bg_api_op.get_api), # 功能菜单（开始菜单）
]
