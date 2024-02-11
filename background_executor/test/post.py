import requests
import json
 
data = {
    'name' : 'mcsm_sw',
    'request_type' : 'check',
}
url = 'http://127.0.0.1:1234/api'

r = requests.post(url,data=json.dumps(data))
print(r.json())