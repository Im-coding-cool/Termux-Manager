import requests

url = 'http://127.0.0.1:8000/default_man/'
data = {'name': 'default_man'}

response = requests.post(url, data=data)

print(response.text)