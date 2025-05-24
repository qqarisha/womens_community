import sqlite3

# Подключаемся к базе
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Добавляем администратора
cursor.execute("""
INSERT INTO users (full_name, email, password, is_admin)
VALUES (?, ?, ?, ?)
""", ("Admin", "admin@gmail.com", "admin1", 1))

conn.commit()
conn.close()

print("✅ Администратор успешно добавлен.")
