import sqlite3
import bcrypt

class UserManager:
    def __init__(self, db_name='users.db'):
        self.db_name = db_name
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )''')
        conn.commit()
        conn.close()

    def create_user(self, first_name, last_name, email, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        hashed_password = self.hash_password(password)
        cursor.execute('''INSERT INTO users (first_name, last_name, email, password)
                          VALUES (?, ?, ?, ?)''',
                          (first_name, last_name, email, hashed_password))

        conn.commit()
        conn.close()

    def hash_password(self, password):
        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed.decode('utf-8')

    def check_password(self, email, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()

        if row:
            stored_hashed_password = row[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
        return False