import requests
import json

def start_task(message_data):
    data = message_data
    url = 'http://127.0.0.1:1234/api'
    try:
        r = requests.post(url,data=json.dumps(data))
        return r.json()
    except:
        return '错误'

if __name__ == '__main__':
    message_data = {
        'name' : 'frp_sw',
        'request_type' : 'revise',
        'data' : [{
            'config' : '# 测试1\n# 测试2', 
        }],
    }
    print(start_task(message_data))