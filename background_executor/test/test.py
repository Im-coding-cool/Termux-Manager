import subprocess

# 执行proot-distro login ubuntu命令
proc = subprocess.Popen(['proot-distro', 'login', 'ubuntu'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 进入proot的shell之后执行 cd /opt/mcsmanager/ && 在后台运行 start-daemon.sh 和 start-web.sh，并执行 ls 命令
output, error = proc.communicate(b'cd /opt/mcsmanager/ && ./start-daemon.sh > /dev/null 2>&1 & ./start-web.sh > /dev/null 2>&1 & ls\n')
print(output.decode('utf-8'))
