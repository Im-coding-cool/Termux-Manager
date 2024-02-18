import sqlite3
import datetime

# 连接到数据库（如果不存在则会创建）
conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')

# 创建游标对象以执行SQL语句
cursor = conn.cursor()

cursor.execute('SELECT * FROM current_time;')

p = cursor.fetchall()
print(p)

# 提交更改并关闭连接
# conn.commit()
conn.close()
