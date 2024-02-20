import os
import wprint
import re




# 获取当前目录下的所有文件
file_list = os.listdir('E:\\项目\\Termux\\Termux-Manager\\background_executor\\test')

# 打印文件列表
for file in file_list:
    # wprint.wprint(file)
    if 'mcsm_sw' in file:
        result = re.search(r'-(.*?)-', file)
        if result:
            wprint.wprint(result.group(1))
            
