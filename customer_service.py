import sqlite3
from customer import Customer

class CustomerService:
    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            self.conn = sqlite3.connect('app.db')
        self.conn.row_factory = sqlite3.Row  # return dictionary
        self.conn.execute('PRAGMA foreign_keys = ON')
        self.setup_database()

    def setup_database(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone_number TEXT,
                    address TEXT,
                    is_active INTEGER DEFAULT 1
                )
            ''')

    def create_customer(self, first_name, last_name, email, phone_number=None, address=None):
        if self.email_exists(email):
            raise ValueError("Another customer already has this email")
        with self.conn:
            self.conn.execute('''
                INSERT INTO customers (first_name, last_name, email, phone_number, address)
                VALUES (?, ?, ?, ?, ?)
            ''', (first_name, last_name, email, phone_number, address))

    def email_exists(self, email):
        cursor = self.conn.cursor()
        cursor.execute('SELECT 1 FROM customers WHERE email = ? AND is_active = 1', (email,))
        return cursor.fetchone() is not None

    def get_customer_by_id(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ? AND is_active = 1', (customer_id,))
        data = cursor.fetchone()
        if data:
            customer_data = dict(data) # converts rows to dictionary
            return Customer(customer_data)
        return None

    def update_customer(self, customer_id, **kwargs):
        if 'email' in kwargs:
            # makes sure email is unique from other existing customers
            cursor = self.conn.cursor()
            cursor.execute('SELECT id FROM customers WHERE email = ? AND id != ? AND is_active = 1',
                           (kwargs['email'], customer_id))
            if cursor.fetchone():
                raise ValueError('A customer with this email already exists.')
        columns = ', '.join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values())
        values.append(customer_id)
        with self.conn:
            self.conn.execute(f'''
                UPDATE customers SET {columns}
                WHERE id = ? AND is_active = 1
            ''', values)

    def soft_delete_customer(self, customer_id):
        with self.conn:
            self.conn.execute('''
                UPDATE customers SET is_active = 0 WHERE id = ?
            ''', (customer_id,))

    def get_all_customers(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE is_active = 1')
        rows = cursor.fetchall()
        customers = [Customer(dict(row)) for row in rows]
        return customers

