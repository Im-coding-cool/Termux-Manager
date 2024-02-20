import requests

url = 'http://localhost:8090/statistics.php'
data = {'param1': 'value1', 'param2': 'value2'}

try:
    response = requests.post(url, data=data)
    response.raise_for_status()  # 检查是否有错误的响应
    print(response.text)
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")
