from datetime import datetime
import pytz

# 创建中国时区对象
china_tz = pytz.timezone('Asia/Shanghai')

# 使用中国时区信息解析日期时间字符串
parsed_time = china_tz.localize(datetime.strptime('2024-02-18 10:16:34', '%Y-%m-%d %H:%M:%S'))

# 获取当前时间并加上中国时区信息
current_dateTime = datetime.now(china_tz)

# 计算时间差并获取秒数
time_difference = current_dateTime - parsed_time
time_difference_in_seconds = time_difference.total_seconds()

print(time_difference_in_seconds)