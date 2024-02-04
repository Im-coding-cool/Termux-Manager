"""
URL configuration for Termux管理器 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from . import views, function_list


urlpatterns = [
    path("", include('Login.urls')), # 登录注册界面
    path("", include('menu.urls')), # 功能菜单（开始菜单）
    path("", include('Function.urls')), # 功能
    path("", include('backend_api_operation.urls')), # 后端操作API
]
