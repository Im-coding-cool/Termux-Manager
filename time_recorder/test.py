import subprocess

tm = '2024-02-18 20:48:00'

# 运行 Linux 命令
result = subprocess.run(['sh', '/home/chen/termux-manager/time_recorder/time_recorder.sh', '-time', tm], stdout=subprocess.PIPE)

# 获取结果并去掉换行和空格
output = result.stdout.decode('utf-8').strip()
output = output.replace("\n", "").replace(" ", "")
print(int(output))