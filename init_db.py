import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Таблица пользователей
cursor.execute('''
CREATE TABLE IF NOT EXISTS пользователи (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
)
''')

# Таблица мероприятий
cursor.execute('''
CREATE TABLE IF NOT EXISTS мероприятия (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL
)
''')

connection.commit()
connection.close()

print("✅ Таблицы созданы успешно!")
