import sqlite3
from appointment import Appointment

class AppointmentService:
    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            self.conn = sqlite3.connect('app.db')
        self.conn.row_factory = sqlite3.Row  # rows are returned as dictionaries
        self.conn.execute('PRAGMA foreign_keys = ON')  # allows for foreign keys to be passed through
        self.setup_database()

    def setup_database(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    location TEXT,
                    is_active INTEGER DEFAULT 1,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            ''')

    def create_appointment(self, customer_id, title, description, start_time, end_time, location):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO appointments (customer_id, title, description, start_time, end_time, location)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (customer_id, title, description, start_time, end_time, location))
            appointment_id = cursor.lastrowid
            return self.get_appointment_by_id(appointment_id)

    def get_appointment_by_id(self, appointment_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE id = ? AND is_active = 1', (appointment_id,))
        data = cursor.fetchone()
        if data:
            return Appointment(dict(data))
        return None

    def get_upcoming_appointments(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM appointments
            WHERE is_active = 1
            ORDER BY datetime(start_time)
            LIMIT ?
        ''', (limit,))
        rows = cursor.fetchall()
        print(f"Retrieved {len(rows)} upcoming appointments.")
        return [Appointment(dict(row)) for row in rows]

    def update_appointment(self, appointment_id, **kwargs):
        # ensures that the appointment being updated exists, raised error if not
        if not self.get_appointment_by_id(appointment_id):
            raise ValueError('Appointment not found.')

        columns = ', '.join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values())
        values.append(appointment_id)
        with self.conn:
            self.conn.execute(f'''
                UPDATE appointments SET {columns}
                WHERE id = ? AND is_active = 1
            ''', values)

    def soft_delete_appointment(self, appointment_id):
        with self.conn:
            self.conn.execute('''
                UPDATE appointments SET is_active = 0 WHERE id = ?
            ''', (appointment_id,))
