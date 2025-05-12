import sqlite3 as sql
import database_requests as reqs 
import secrets 
import threading

class Database:
    def __init__(self, filename):
        self.lock = threading.Lock()                            # Объект – замок 
        self.connection = sql.connect(filename, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.cursor.execute(reqs.init_request)
        
    def find_user(self, email):
        self.lock.acquire()                                     # Закрываем замок: сейчас БДшкой пользоваться будем мы. Но если он уже закрыт (занят другими потоками, мы ждём в этом методе и не идем дальше, пока не откроется)
                         
        self.cursor.execute(reqs.get_users_by_email, (email,))
        self.connection.commit()

        user = self.cursor.fetchone()
        self.lock.release()                                     # Нам больше не нужны операции с БД, поэтому позволяем другим потокам пользоваться find_user, открываем замок
        return user

    def add_user(self, request):
        token = secrets.token_hex(16)
        self.lock.acquire()                                     # Опять работаем с курсором, поэтому замок закрываем 

        # Условие на уникальность токена можно переписать так:
        self.cursor.execute(reqs.find_token, (token,))
        occurences = self.cursor.fetchall()
        while occurences != []: 
            self.cursor.execute(reqs.find_token, (token,))
            occurences = self.cursor.fetchall()

#       while self.cursor.execute(reqs.find_token, (token,)): 
#           token = secrets.token_hex(16)

        self.cursor.execute(reqs.add_user, (request['full_name'], request['email'], request['password'], token))
        self.connection.commit()

        self.lock.release()                                    # Теперь курсор нам не нужен 