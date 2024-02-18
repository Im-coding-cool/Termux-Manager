import subprocess
import time

# 执行命令并创建伪终端
proc = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# 读取终端返回内容并记录到文件
with open('aa.txt', 'w') as file:
    # 向终端发送命令
    proc.stdin.write("proot-distro login ubuntu\n")
    proc.stdin.flush()

    # 发送额外的命令
    proc.stdin.write("ls\n")
    proc.stdin.flush()

    proc.stdin.write("exit\n")
    proc.stdin.flush()

    proc.stdin.write("echo 结束-----------------\n")
    proc.stdin.flush()

    proc.stdin.write("ls\n")
    proc.stdin.flush()

    while True:
        output = proc.stdout.readline()
        if output == '' and proc.poll() is not None:
            break
        file.write(output)


# proc.terminate() # 退出进程