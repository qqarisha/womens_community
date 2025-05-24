import sqlite3
import database_requests as req
import secrets 
import hashlib

hash_object = hashlib.sha256()
hash_object.update(b'admin1')
password_hash = hash_object.hexdigest()

# Подключаемся к базе
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

token = secrets.token_hex(16)
cursor.execute(req.get_users_by_token, (token,))
occurences = cursor.fetchall()
while occurences != []: 
    token = secrets.token_hex(16)
    cursor.execute(req.get_users_by_token, (token,))
    occurences = cursor.fetchall()

# Добавляем администратора
cursor.execute(req.add_user, ("Admin", "admin@gmail.com", password_hash, 1, token))

conn.commit()
conn.close()

print("Администратор успешно добавлен.")
