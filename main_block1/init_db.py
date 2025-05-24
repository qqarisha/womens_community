import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL
)
""")

conn.commit()
conn.close()
print("Таблица 'events' создана.")
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Добавляем колонку image, если её ещё нет
try:
    cursor.execute("ALTER TABLE events ADD COLUMN image TEXT")
    print("✅ Столбец 'image' успешно добавлен в таблицу events.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("⚠️ Столбец 'image' уже существует.")
    else:
        raise

conn.commit()
conn.close()
