import sqlite3
import datetime

# 连接到数据库（如果不存在则会创建）
conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')

# 创建游标对象以执行SQL语句
cursor = conn.cursor()

# 创建表格
cursor.execute('''
CREATE TABLE items (
    id INT PRIMARY KEY,
    pid INT,
    name VARCHAR(255),
    state VARCHAR(20),
    last_online DATETIME,
    run_command VARCHAR(255),
    output TEXT
);
''')

# 插入数据
cursor.execute("INSERT INTO items (id, pid, name, state, last_online, run_command, output) VALUES (1, NULL, 'chen', 'OFF', '2024-2-16 09:25:30', NULL, '项目还没有启动过');")

# 提交更改并关闭连接
conn.commit()
conn.close()
