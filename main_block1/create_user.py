import sqlite3
import database_requests as req
import secrets
import hashlib

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
