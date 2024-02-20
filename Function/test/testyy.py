from datetime import datetime, timedelta


parsed_time = datetime.strptime('2024-02-16 23:31:11', '%Y-%m-%d %H:%M:%S')

current_dateTime = datetime.now()

aa = current_dateTime - parsed_time

if aa.total_seconds() > 5:
    pass
else:
    pass
