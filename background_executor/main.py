from flask import Flask, request, jsonify
import json
import wprint
import os
import re
import time
import threading

# 数据交换目录
根目录 = 'E:\\项目\\Termux\\Termux-Manager\\background_executor\\test\\data'

# 临时储存返回结果
return_res = 'f'

# 倒计时器临时返回
tie = 5

# 倒计时器
def timerr(te):
    global tie
    time.sleep(te)
    tie = 0
    

# 写入任务
def 写入任务(file, message_data):    
    # 以覆盖方式写入文件，如果没有该文件就创建一个
    with open(根目录 + '\\' + file, 'w') as filee:
        filee.write(json.dumps(message_data))

app = Flask(__name__)
app.debug = True


# 获取返回结果
def return_results():
    global return_res
    global tie
    i = 0
    while tie > 0:
        file_list = os.listdir(根目录)
        for file in file_list:
            if 'mcsm_return' in file:
                result = re.search(r'-(.*?)-', file)
                if result:
                    wprint.wprint(result.group(1))
                    while True:
                        try:
                            with open(根目录 + '\\' + file, 'r') as f:
                                data = json.load(f)
                            os.remove(根目录 + '\\-1-mcsm_return.json')
                            return_res = data
                            i = 1
                            break
                        except:
                            pass
        if i == 1:
            break

    


# 任务处理
def task_processor(student_json):
    global tie
    global return_res
    mc = student_json
    if mc["name"] == 'mcsm_sw' :
        if mc['request_type'] == 'task':
            wprint.wprint('mcsm_执行任务')
            file_list = os.listdir(根目录)
            number = 1
            for file in file_list:
                if 'mcsm_sw' in file:
                    result = re.search(r'-(.*?)-', file)
                    if result:
                        wprint.wprint(result.group(1))
                        if int(result.group(1)) > number:
                            number = result.group(1)
            # 写入任务
            写入任务('-' + str(number) + '-mcsm_sw.json', student_json)
            return student_json
        elif mc['request_type'] == 'check':
            wprint.wprint('mcsm_查看状态')
            file_list = os.listdir(根目录)
            number = 1
            for file in file_list:
                if 'mcsm_sw' in file:
                    result = re.search(r'-(.*?)-', file)
                    if result:
                        wprint.wprint(result.group(1))
                        if int(result.group(1)) > number:
                            number = result.group(1)
            # 写入任务
            写入任务('-' + str(number) + '-mcsm_sw.json', student_json)
            tie = 5
            return_res = 'f'
            wprint.wprint('线程1')
            thread1 = threading.Thread(target=return_results)
            thread1.start() # 获取返回结果

            wprint.wprint('线程2')
            thread2 = threading.Thread(target=timerr, args=(5,))
            thread2.start()
            while tie > 0:
                time.sleep(0.1)
                if return_res != 'f':
                    student_json = return_res
                    break
            else:
                student_json = '超时'
            
            thread1.join()
            return student_json
    elif mc['name'] == '???':
        pass
 
@app.route('/api',methods=['post'])
def add_stu():
    if  not request.data:   #检测是否有数据
        return ('fail')
    student = request.data.decode('utf-8')    #获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    student_json = json.loads(student)    #把区获取到的数据转为JSON格式。

    # 处理操作
    student_json = task_processor(student_json)

    return jsonify(student_json)
    #返回JSON数据。
 
if __name__ == '__main__':
    app.run(port=1234)
    #这里指定了地址和端口号。