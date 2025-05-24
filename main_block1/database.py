import sqlite3

class Database:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                avatar TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                image TEXT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                user_id INTEGER,
                event_id INTEGER,
                PRIMARY KEY (user_id, event_id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                user_id INTEGER,
                event_id INTEGER,
                PRIMARY KEY (user_id, event_id)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_events (
                user_id INTEGER,
                event_id INTEGER,
                PRIMARY KEY (user_id, event_id)
            )
        """)
        self.conn.commit()

    def add_user(self, user_data):
        query = """
            INSERT INTO users (full_name, email, password, is_admin, avatar)
            VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query,
                            (user_data['full_name'], user_data['email'], user_data['password'],
                             user_data['is_admin'], user_data.get('avatar')))
        self.conn.commit()

    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'full_name': row[1],
                'email': row[2],
                'password': row[3],
                'is_admin': bool(row[4]),
                'avatar': row[5]
            }
        return None

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'full_name': row[1],
                'email': row[2],
                'password': row[3],
                'is_admin': bool(row[4]),
                'avatar': row[5]
            }
        return None

    def update_user_avatar(self, user_id, filename):
        self.cursor.execute("UPDATE users SET avatar = ? WHERE id = ?", (filename, user_id))
        self.conn.commit()

    def get_all_events(self):
        self.cursor.execute("SELECT * FROM events ORDER BY date DESC")
        return self.cursor.fetchall()

    def get_user_events(self, user_id):
        self.cursor.execute("""
            SELECT events.* FROM events
            JOIN user_events ON events.id = user_events.event_id
            WHERE user_events.user_id = ?
            ORDER BY events.date DESC
        """, (user_id,))
        return self.cursor.fetchall()

    def get_user_favorites(self, user_id):
        self.cursor.execute("""
            SELECT events.* FROM events
            JOIN favorites ON events.id = favorites.event_id
            WHERE favorites.user_id = ?
            ORDER BY events.date DESC
        """, (user_id,))
        return self.cursor.fetchall()

    def add_event(self, title, description, date):
        self.cursor.execute("INSERT INTO events (title, description, date) VALUES (?, ?, ?)",
                            (title, description, date))
        self.conn.commit()

    def register_for_event(self, user_id, event_id):
        self.cursor.execute("""
            INSERT OR IGNORE INTO user_events (user_id, event_id)
            VALUES (?, ?)
        """, (user_id, event_id))
        self.conn.commit()

    def add_to_favorites(self, user_id, event_id):
        self.cursor.execute("""
            INSERT OR IGNORE INTO favorites (user_id, event_id)
            VALUES (?, ?)
        """, (user_id, event_id))
        self.conn.commit()

    def remove_from_favorites(self, user_id, event_id):
        self.cursor.execute("""
            DELETE FROM favorites WHERE user_id = ? AND event_id = ?
        """, (user_id, event_id))
        self.conn.commit()

    def add_event_with_image(self, title, description, date, image_filename):
            self.cursor.execute("""
                INSERT INTO events (title, description, date, image)
                VALUES (?, ?, ?, ?)
            """, (title, description, date, image_filename))
            self.conn.commit()

    def get_event_by_id(self, event_id):
        self.cursor.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        return self.cursor.fetchone()

    def add_event_with_image(self, title, description, date, image_filename):
        self.cursor.execute("""
            INSERT INTO events (title, description, date, image)
            VALUES (?, ?, ?, ?)
        """, (title, description, date, image_filename))
        self.conn.commit()

    def delete_event(self, event_id):
        self.cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
        self.conn.commit()


