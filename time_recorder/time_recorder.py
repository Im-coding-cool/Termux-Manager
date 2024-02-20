import sqlite3
from datetime import datetime
import time

while True:
    # 连接到数据库
    conn = sqlite3.connect('/home/chen/termux-manager/default/database/data.db')
    cursor = conn.cursor()

    # 执行 SELECT 查询
    cursor.execute("SELECT * FROM current_time WHERE id=?", (1,))
    row = cursor.fetchone()

    if row:
        # 如果存在就修改
        current_dateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE current_time SET current_time=? WHERE id = ?", (current_dateTime, 1))
    else:
        print("条目未找到")

    # 关闭连接
    conn.commit()
    conn.close()
    time.sleep(0.3)
