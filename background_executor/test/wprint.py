import os

# 带文件名print
def wprint(data):
    print(os.path.basename(__file__) + ':', data)
