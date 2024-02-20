import requests
import subprocess
import time
import threading
import sqlite3
import configparser
from datetime import datetime
import os

# 加载配置文件
import configparser
import global_configuration
config_path = global_configuration.ROOT_PSTH
config_path = config_path + 'config/config.ini'
global_config = configparser.ConfigParser()
global_config.read(config_path) # 全局配置

# 当前配置
DEFAULT_ROOT_PATH = global_config.get('default', 'root_path')


def get_json_data(url):
    try:
        # 发起GET请求
        response = requests.get(url)

        # 检查响应状态码
        if response.status_code == 200:
            # 解析JSON数据
            json_data = response.json()
            return json_data
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        return None

def download_file_with_progress(url, destination):
    try:
        # 发起GET请求
        response = requests.get(url, stream=True)

        # 检查响应状态码
        if response.status_code == 200:
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            # 保存文件的路径
            with open(destination, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress = (downloaded_size / total_size) * 100
                    print(f"下载进度: {progress:.2f}% complete")

            print(f"\n文件下载成功: {destination}")

        else:
            print(f"文件下载失败，状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"下载文件时发生异常: {e}")

if __name__ == "__main__":
    print('* 预设包安装程序')
    print('[正在获取远程列表]')
    # 替换为你要请求的URL
    api_url = "http://38.6.175.125:8090/api.php"
    # 调用函数获取JSON数据
    result = get_json_data(api_url)
    # 处理获取的JSON数据
    if result:
        install = {}
        ii = 0
        for data in result['data']:
            ii += 1
            install[str(ii)] = data['download']
            print('编号 { ' + str(ii) + ' }' + ' | ID: ' + data['id'] + ' | 名称: ' + data['name'] + ' | 作者: ' + data['author'] + ' | 说明: ' + data['clarification'])
        data_id = str(input('[请输入编号ID] > '))
        download_file_with_progress(install[data_id], DEFAULT_ROOT_PATH + 'installer/f.tar.gz')
        try:
            result = subprocess.run("tar -zxvf " + DEFAULT_ROOT_PATH + 'installer/f.tar.gz -C ' + DEFAULT_ROOT_PATH + 'default/', shell=True, capture_output=True, text=True)
            print('安装完成:' + result.stdout)
            print(result.stderr)
        except:
            print('安装失败:解压出了问题')
    else:
        print("无法获取JSON数据")
