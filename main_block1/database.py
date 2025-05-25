import sqlite3
import database_requests as req
import secrets


class Database:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute(req.init_request_users)
        self.cursor.execute(req.init_request_events)

        self.cursor.execute(req.init_request_registrations)
        self.cursor.execute(req.init_request_user_events)
        self.conn.commit()

    def add_user(self, user_data):
        token = secrets.token_hex(16)
        self.cursor.execute(req.get_users_by_token, (token,))
        occurences = self.cursor.fetchall()
        while occurences != []:
            token = secrets.token_hex(16)
            self.cursor.execute(req.get_users_by_token, (token,))
            occurences = self.cursor.fetchall()

        self.cursor.execute(req.add_user,
                            (user_data['full_name'], user_data['email'], user_data['password_hash'],
                             user_data['is_admin'], token))
        self.conn.commit()

    def get_user_by_email(self, email):
        self.cursor.execute(req.get_users_by_email, (email,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'full_name': row[1],
                'email': row[2],
                'password_hash': row[3],
                'is_admin': bool(row[4]),
                'token': row[5]
            }
        return None

    def get_user_by_token(self, token):
        self.cursor.execute(req.get_users_by_token, (token,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'full_name': row[1],
                'email': row[2],
                'password': row[3],
                'is_admin': bool(row[4]),
                'token': row[5]
            }
        return None

    def get_all_events(self):
        self.cursor.execute(req.all_events)
        return self.cursor.fetchall()

    def get_user_events(self, token):
        self.cursor.execute(req.get_user_events, (token,))
        return self.cursor.fetchall()

    def add_event(self, title, description, full_description, event_format, organizer, location, date):
        token = secrets.token_hex(16)
        self.cursor.execute(req.get_users_by_token, (token,))
        occurences = self.cursor.fetchall()
        while occurences != []:
            token = secrets.token_hex(16)
            self.cursor.execute(req.get_users_by_token, (token,))
            occurences = self.cursor.fetchall()
            #wsaefdasdcasdcasdfasef

        self.cursor.execute(req.add_event, (title, description, full_description, event_format, organizer, location, date, token))
        self.conn.commit()

    def register_for_event(self, user_token, event_token):
        self.cursor.execute(req.register_for_event, (user_token, event_token))
        self.conn.commit()

    def add_event_with_image(self, title, description, full_description, event_format, organizer, location, date, image_filename):
        token = secrets.token_hex(16)
        self.cursor.execute(req.get_users_by_token, (token,))
        occurences = self.cursor.fetchall()
        while occurences != []:
            token = secrets.token_hex(16)
            self.cursor.execute(req.get_users_by_token, (token,))
            occurences = self.cursor.fetchall()
            #wsaefdasdcasdcasdfasef
        self.cursor.execute(req.add_event_with_image, (title, description, date, image_filename))
        self.conn.commit()

    def get_event_by_token(self, event_token):
        self.cursor.execute(req.get_event_by_token, (event_token,))
        return self.cursor.fetchone()

    def delete_event(self, event_token):
        self.cursor.execute(req.delete_event, (event_token,))
        self.conn.commit()


