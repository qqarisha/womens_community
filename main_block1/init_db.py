import sqlite3
import database_requests as req
import secrets
import hashlib

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Создаём таблицу с is_admin
cursor.execute(req.init_request_users)

conn.commit()
conn.close()
print("База и таблица 'users' созданы.")

#Создаем таблицу events
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(req.init_request_events)

conn.commit()
conn.close()
print("Таблица 'events' создана.")

# Создаем обычного пользователя
hash_object = hashlib.sha256()
hash_object.update(b'userpass')
password_hash = hash_object.hexdigest()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

token = secrets.token_hex(16)
cursor.execute(req.get_users_by_token, (token,))
occurences = cursor.fetchall()
while occurences != []:
    token = secrets.token_hex(16) 
    cursor.execute(req.get_users_by_token, (token,))
    occurences = cursor.fetchall()

cursor.execute(req.add_user, ("Обычный Пользователь", "user@gmail.com", password_hash, 0, token))

conn.commit()
conn.close()
print("Обычный пользователь успешно добавлен.")

# Создаем админа
hash_object = hashlib.sha256()
hash_object.update(b'admin1')
password_hash = hash_object.hexdigest()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

token = secrets.token_hex(16)
cursor.execute(req.get_users_by_token, (token,))
occurences = cursor.fetchall()
while occurences != []: 
    token = secrets.token_hex(16)
    cursor.execute(req.get_users_by_token, (token,))
    occurences = cursor.fetchall()

cursor.execute(req.add_user, ("Admin", "admin@gmail.com", password_hash, 1, token))

conn.commit()
conn.close()
print("Администратор успешно добавлен.")