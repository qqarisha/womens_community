import sqlite3
import database_requests as req

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(req.init_request_events)

conn.commit()
conn.close()
print("Таблица 'events' создана.")
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Добавляем колонку image, если её ещё нет
try:
    cursor.execute(req.add_image_column)
    print("Столбец 'image' успешно добавлен в таблицу events.")
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print("Столбец 'image' уже существует.")
    else:
        raise

conn.commit()
conn.close()
