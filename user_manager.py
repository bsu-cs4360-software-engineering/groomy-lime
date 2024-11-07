import sqlite3
import bcrypt

class UserManager:
    def __init__(self, db_name='users.db', conn=None):
        self.conn = conn or sqlite3.connect(db_name)
        self.setup_database()

    def setup_database(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL
                        )''')
        self.conn.commit()

    def create_user(self, first_name, last_name, email, password):
        hashed_password = self.hash_password(password)
        with self.conn:
            self.conn.execute('''INSERT INTO users (first_name, last_name, email, password)
                          VALUES (?, ?, ?, ?)''',
                          (first_name, last_name, email, hashed_password))
    @staticmethod
    def hash_password(password):
        password = password.encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed.decode('utf-8')

    def check_password(self, email, password):
        cursor = self.conn.execute('SELECT password FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        if row:
            stored_hashed_password = row[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
        return False