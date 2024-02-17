import psutil
print(psutil.cpu_count(logical=False))  # 返回核心数14
print(psutil.cpu_count())               # 进程数20
print(psutil.cpu_freq())                # CPU频率
# scpufreq(current=2600.0, min=0.0, max=2600.0)
