# add_avatar_column.py

import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN avatar TEXT")
    print("Колонка avatar успешно добавлена.")
except sqlite3.OperationalError:
    print("Колонка avatar уже существует.")

conn.commit()
conn.close()
