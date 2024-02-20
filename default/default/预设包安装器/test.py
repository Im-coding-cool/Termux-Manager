import requests

def download_file_with_progress(url, destination):
    try:
        # 发起GET请求
        response = requests.get(url, stream=True)

        # 检查响应状态码
        if response.status_code == 200:
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0

            # 保存文件的路径
            with open(destination, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress = (downloaded_size / total_size) * 100
                    print(f"下载进度: {progress:.2f}% complete")

            print(f"\n文件下载成功: {destination}")

        else:
            print(f"文件下载失败，状态码: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"下载文件时发生异常: {e}")

if __name__ == "__main__":
    # 替换为你要下载的文件的URL和目标路径
    file_url = "http://192.168.110.230:8090/res/%E9%A2%84%E8%AE%BE1/def-1.tar.gz"
    destination_path = "def-1.tar.gz"

    # 调用函数下载文件
    download_file_with_progress(file_url, destination_path)
    print('ok')
