import requests
import json
 
data = {
    'name' : 'default_man',
}
url = 'http://127.0.0.1:8000/default_man/'

r = requests.post(url,data=json.dumps(data))
print(r.json())