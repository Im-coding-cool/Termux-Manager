import configparser

# 创建ConfigParser对象
config = configparser.ConfigParser()

# 读取INI文件
config.read('/home/chen/termux-manager/Function/test/example.ini')

# 获取特定section中的值
value = config.get('section_name', 'key1')

# 获取所有的section
sections = config.sections()
print(value)
