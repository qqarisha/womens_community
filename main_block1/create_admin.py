import sqlite3

def create_admin():
    try:
        # Подключаемся к базе
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Проверяем, существует ли уже администратор
        cursor.execute("SELECT 1 FROM users WHERE email = ?", ("admin@gmail.com",))
        admin_exists = cursor.fetchone()

        if admin_exists:
            print("Администратор admin@gmail.com уже существует")
            return

        # Добавляем администратора
        cursor.execute("""
        INSERT INTO users (full_name, email, password, is_admin)
        VALUES (?, ?, ?, ?)
        """, ("Admin", "admin@gmail.com", "admin1", 1))

        conn.commit()
        print("Администратор успешно добавлен")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_admin()