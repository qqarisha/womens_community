import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='database.db'):
        """Инициализация подключения к базе данных"""
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
        self.create_tables()
        print("[DB] База данных подключена")

    def create_tables(self):
        """Создание таблиц, если они не существуют"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    date TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_by INTEGER
                )
            """)
            self.conn.commit()
            print("[DB] Таблица events создана")
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка при создании таблицы: {e}")

    def add_event(self, title, description, date, created_by=None):
        """Добавление нового события в базу данных"""
        try:
            self.cursor.execute(
                "INSERT INTO events (title, description, date, created_by) VALUES (?, ?, ?, ?)",
                (title, description, date, created_by)
            )
            self.conn.commit()
            print(f"[DB] Событие добавлено. ID: {self.cursor.lastrowid}")
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка при добавлении события: {e}")
            return False

    def get_all_events(self):
        """Получение всех событий из базы данных"""
        try:
            self.cursor.execute("""
                SELECT id, title, description, date, created_at 
                FROM events 
                ORDER BY date DESC
            """)
            events = self.cursor.fetchall()
            return [{
                'id': e[0],
                'title': e[1],
                'description': e[2],
                'date': e[3],
                'created_at': e[4]
            } for e in events]
        except sqlite3.Error as e:
            print(f"[DB ERROR] Ошибка при получении событий: {e}")
            return []