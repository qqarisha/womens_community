import sqlite3 as sql
import database_requests as reqs 
from tools import generate_token 

class Database:
    def __init__(self, filename):
        self.connection = sql.connect(filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(reqs.init_request)

    def find_user(self, email):
        print(reqs.get_users_by_email, email)
        self.cursor.execute(reqs.get_users_by_email, (email,))
        self.connection.commit()
        return self.cursor.fetchall()

    def add_user(self, request):
        self.cursor.execute(reqs.add_user, (request['full_name'], request['email'], request['password'], generate_token()))
        self.connection.commit()