# create_user.py
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users (full_name, email, password, is_admin)
VALUES (?, ?, ?, ?)
""", ("Обычный Пользователь", "user@gmail.com", "userpass", 0))

conn.commit()
conn.close()
