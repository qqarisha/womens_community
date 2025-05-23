# Users Table
init_request_users = '''CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    auth_token TEXT NOT NULL
)'''

# Events Table (упрощенная версия)
init_request_events = '''CREATE TABLE IF NOT EXISTS Events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    created_by INTEGER
)'''

# Основные запросы
get_users_by_email = '''SELECT * FROM Users WHERE email = ?'''
add_user = '''INSERT INTO Users (full_name, email, password_hash, auth_token, is_admin) 
              VALUES (?, ?, ?, ?, ?)'''
find_token = '''SELECT * FROM Users WHERE auth_token = ?'''
data_by_token = '''SELECT id, full_name, email, is_admin FROM Users WHERE auth_token = ?'''

# Запросы для событий
add_event = '''INSERT INTO Events (title, description, date, created_by) 
               VALUES (?, ?, ?, ?)'''
get_all_events = '''SELECT * FROM Events ORDER BY date DESC'''