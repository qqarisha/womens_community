init_request = '''CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
full_name TEXT NOT NULL,
email TEXT NOT NULL,
password_hash TEXT NOT NULL,
auth_token TEXT NOT NULL
)'''

get_users_by_email = '''SELECT * FROM Users WHERE email = ?'''

add_user = '''INSERT INTO Users (full_name, email, password_hash, auth_token) VALUES (?, ?, ?, ?)'''