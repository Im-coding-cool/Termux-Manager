import os
import pty
import subprocess

master, slave = pty.openpty()
p = subprocess.Popen(["bash"], preexec_fn=os.setsid, stdin=slave, stdout=slave, stderr=slave)

# 向子进程发送命令并获取输出
def send_command_get_output(command):
    os.write(master, command.encode() + b"\r")
    output = b""
    while True:
        try:
            chunk = os.read(master, 1024)
            if not chunk:
                break
            output += chunk
        except OSError:
            break
    return output.decode()

result = send_command_get_output("ls")
print(result)

# 记得关闭文件描述符和终止子进程
os.close(master)
os.close(slave)
p.terminate()
