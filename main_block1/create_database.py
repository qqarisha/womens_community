import sqlite3
import database_requests as req

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создаём таблицу с is_admin
cursor.execute(req.init_request_users)

conn.commit()
conn.close()

print("База и таблица users созданы.")
