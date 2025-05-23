import sqlite3

def create_database():
    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Создаём таблицу пользователей с полем is_admin
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            auth_token TEXT
        )
        """)

        # Создаём таблицу мероприятий
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            created_by INTEGER,
            FOREIGN KEY(created_by) REFERENCES users(id)
        )
        """)

        conn.commit()
        print("[SUCCESS] База данных и таблицы успешно созданы")
        
        # Создаём администратора по умолчанию
        try:
            cursor.execute(
                "INSERT INTO users (full_name, email, password, is_admin) VALUES (?, ?, ?, ?)",
                ("Admin", "admin@gmail.com", "admin123", 1)
            )
            conn.commit()
            print("[SUCCESS] Создан администратор по умолчанию: admin@gmail.com / admin123")
        except sqlite3.IntegrityError:
            print("[INFO] Администратор уже существует")

    except Exception as e:
        print(f"[ERROR] Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_database()