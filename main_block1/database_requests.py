init_request_users = '''CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
full_name TEXT NOT NULL,
email TEXT NOT NULL,
password_hash TEXT NOT NULL,
auth_token TEXT NOT NULL
)'''

get_users_by_email = '''SELECT * FROM Users WHERE email = ?'''

add_user = '''INSERT INTO Users (full_name, email, password_hash, auth_token) VALUES (?, ?, ?, ?)'''

find_token = '''SELECT * FROM Users WHERE auth_token = ?'''

data_by_token = '''SELECT full_name, email FROM Users WHERE auth_token = ?'''

init_request_events = '''CREATE TABLE IF NOT EXISTS Events (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
date DATETIME NOT NULL,
place TEXT NOT NULL,
price TEXT NOT NULL,
description TEXT NOT NULL,
more_description TEXT NOT NULL
)'''

events_description = '''CREATE TABLE IF NOT EXISTS EventsDescription (
id INTEGER PRIMARY KEY,
name TEXT NOT NULL,
date DATETIME NOT NULL,
place TEXT NOT NULL,
price TEXT NOT NULL,
full_description TEXT NOT NULL,
event_token TEXT NOT NULL
)'''
