import sqlite3
from datetime import datetime

# 连接到数据库（如果不存在则会创建）
conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')

# 创建游标对象以执行SQL语句
cursor = conn.cursor()

# 创建表格
cursor.execute('''
CREATE TABLE current_time (
    id INT PRIMARY KEY,
    pid INT,
    current_time DATETIME
);
''')

current_dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 插入数据
cursor.execute("INSERT INTO current_time (id, pid, current_time) VALUES (1, NULL, '" + current_dateTime + "');")

# 提交更改并关闭连接
conn.commit()
conn.close()
