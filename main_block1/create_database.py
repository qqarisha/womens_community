import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создаём таблицу с is_admin
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    is_admin INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("✅ База и таблица users созданы.")
