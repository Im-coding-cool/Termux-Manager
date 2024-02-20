import configparser

# 创建ConfigParser对象
config = configparser.ConfigParser()

# 添加section和键值对
config['section_name'] = {'key1': 'value1', 'key2': 'value2'}

# 写入到INI文件
with open('/home/chen/termux-manager/Function/test/example.ini', 'w') as configfile:
    config.write(configfile)
