import subprocess
import time

# 执行命令并创建伪终端
proc = subprocess.Popen(['bash'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

proc.stdin.write("proot-distro login ubuntu\n")
proc.stdin.flush()