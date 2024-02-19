import sqlite3

# 连接到数据库
conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')
cursor = conn.cursor()

# 执行 SELECT 查询
cursor.execute("SELECT * FROM items WHERE id=?", (1,))
row = cursor.fetchone()

if row:
    # 如果存在就修改
    cursor.execute("UPDATE items SET run_command = ? WHERE id = ?", ('ls',1))
    # cursor.execute("UPDATE items SET run_command = ? WHERE id = ?", (None,1))
else:
    print("条目未找到")

# 关闭连接
conn.commit()
conn.close()
