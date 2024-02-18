import sqlite3

# 连接到数据库
conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')

# 创建一个游标对象
cursor = conn.cursor()

# 执行删除表语句
cursor.execute("DROP TABLE current_time")

# 提交更改
conn.commit()

# 关闭游标和数据库连接
cursor.close()
conn.close()
