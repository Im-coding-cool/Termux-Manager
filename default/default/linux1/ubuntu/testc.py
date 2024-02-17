import sqlite3

# 连接到数据库
conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')
cursor = conn.cursor()

# 执行 SELECT 查询
cursor.execute("SELECT * FROM items WHERE id=?", (1,))
row = cursor.fetchone()

if row:
    print(row[6])  # 如果存在则输出该条目
else:
    print("条目未找到")  # 否则输出未找到的消息

# 关闭连接
conn.close()
