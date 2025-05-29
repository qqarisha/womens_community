get_users_by_email = '''SELECT * FROM Users WHERE email = ?'''

add_user = '''INSERT INTO users (full_name, email, password_hash, is_admin, token) VALUES (?, ?, ?, ?, ?)'''

get_users_by_token = '''SELECT * FROM Users WHERE token = ?'''

get_event_by_token = '''SELECT * FROM events WHERE token = ?'''

data_by_token = '''SELECT full_name, email FROM Users WHERE token = ?'''
 
all_events = '''SELECT * FROM events ORDER BY date DESC'''

add_event = '''INSERT INTO events (title, description, full_description, event_format, organizer, location, date, token) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

delete_event = '''DELETE FROM events WHERE token = ?'''

register_for_event = """
INSERT OR IGNORE INTO user_events (user_token, event_token)
VALUES (?, ?)
"""

add_event_with_image = """
INSERT INTO events (title, description, date, image)
VALUES (?, ?, ?, ?)
"""

get_user_events = """
SELECT events.* FROM events
JOIN user_events ON events.token = user_events.event_token
WHERE user_events.user_token = ?
ORDER BY events.date DESC
"""

init_request_users = """
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT NOT NULL,
email TEXT NOT NULL UNIQUE,
password_hash TEXT NOT NULL,
is_admin INTEGER DEFAULT 0,
token TEXT NOT NULL
)
"""

init_request_events = """
CREATE TABLE IF NOT EXISTS events (
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
description TEXT NOT NULL,
full_description TEXT NOT NULL,
event_format TEXT NOT NULL,
organizer TEXT NOT NULL, 
location TEXT NOT NULL,
date TEXT NOT NULL,
image TEXT,
token TEXT NOT NULL
)
"""

init_request_registrations = """
CREATE TABLE IF NOT EXISTS registrations (
user_token INTEGER,
event_token INTEGER,
PRIMARY KEY (user_token, event_token)
)
"""

init_request_user_events = """
CREATE TABLE IF NOT EXISTS user_events (
user_token INTEGER,
event_token INTEGER,
PRIMARY KEY (user_token, event_token)
)
"""

add_image_column = '''ALTER TABLE events ADD COLUMN image TEXT'''

get_event_by_token = """
SELECT * FROM events WHERE token = ?
"""

if_register =  "SELECT 1 FROM user_events WHERE user_token = ? AND event_token = ?"

register_for_event = """
INSERT INTO user_events (user_token, event_token) VALUES (?, ?)
"""