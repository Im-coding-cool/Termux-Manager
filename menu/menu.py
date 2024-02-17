from django.http import HttpResponse
from django.shortcuts import render

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
version = global_config.get('config', 'version')
 
def menu(request):
    
    return render(request, 'state.html', {'con' : "function_menu.html", 'version' : version})

def User_Agreement_txt(request):
    return render(request, 'User_Agreement.html')

def friendly_reminder(request):
    return render(request, 'friendly_reminder.html')