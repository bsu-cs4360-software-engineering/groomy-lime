import sqlite3
from service import Service
from note import Note

class ServicesService:
    def __init__(self, conn=None):
        self.conn = conn or sqlite3.connect('app.db')
        self.conn.row_factory = sqlite3.Row
        self.setup_database()

    def setup_database(self):
        with self.conn:
            # create services table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    deleted INTEGER NOT NULL DEFAULT 0
                )
            ''')
            # create service_notes table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS service_notes (
                    service_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    PRIMARY KEY (service_id, note_id),
                    FOREIGN KEY (service_id) REFERENCES services(id),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                )
            ''')

    # CRUD methods
    def create_service(self, name, description, price):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO services (name, description, price) VALUES (?, ?, ?)', (name, description, price))
            service_id = cursor.lastrowid
            return self.get_service_by_id(service_id)

    def get_service_by_id(self, service_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM services WHERE id = ? AND deleted = 0', (service_id,))
        data = cursor.fetchone()
        return Service(dict(data)) if data else None

    def get_all_services(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM services WHERE deleted = 0')
        return [Service(dict(row)) for row in cursor.fetchall()]

    def update_service(self, service_id, name, description, price):
        with self.conn:
            self.conn.execute('UPDATE services SET name = ?, description = ?, price = ? WHERE id = ?', (name, description, price, service_id))

    def soft_delete_service(self, service_id):
        with self.conn:
            self.conn.execute('UPDATE services SET deleted = 1 WHERE id = ?', (service_id,))

    # notes-related methods
    def get_notes_for_service(self, service_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT n.*
            FROM notes n
            JOIN service_notes sn ON n.id = sn.note_id
            WHERE sn.service_id = ?
            ORDER BY datetime(n.created_at) DESC
        ''', (service_id,))
        return [Note(dict(row)) for row in cursor.fetchall()]

    def add_note_to_service(self, service_id, note_id):
        with self.conn:
            self.conn.execute('INSERT INTO service_notes (service_id, note_id) VALUES (?, ?)', (service_id, note_id))

    def delete_note_for_service(self, service_id, note_id):
        with self.conn:
            self.conn.execute('DELETE FROM service_notes WHERE service_id = ? AND note_id = ?', (service_id, note_id))
            # optionally delete note if it's orphaned
            self.delete_note_if_orphaned(note_id)

    def delete_note_if_orphaned(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM customer_notes WHERE note_id = ?', (note_id,))
        customer_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM appointment_notes WHERE note_id = ?', (note_id,))
        appointment_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM service_notes WHERE note_id = ?', (note_id,))
        service_count = cursor.fetchone()['count']
        if customer_count == 0 and appointment_count == 0 and service_count == 0:
            self.conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
