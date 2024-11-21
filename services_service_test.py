import unittest
import sqlite3
from services_service import ServicesService
from service import Service
from note import Note

class TestServicesService(unittest.TestCase):
    def setUp(self):
        # use an in-memory SQLite database for testing
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute('PRAGMA foreign_keys = ON')  # Enable foreign key support
        self.services_service = ServicesService(self.conn)
        self.setup_test_tables()

    def setup_test_tables(self):
        # Drop tables if they already exist
        with self.conn:
            self.conn.execute('DROP TABLE IF EXISTS service_notes')
            self.conn.execute('DROP TABLE IF EXISTS services')
            self.conn.execute('DROP TABLE IF EXISTS notes')
            self.conn.execute('DROP TABLE IF EXISTS customer_notes')
            self.conn.execute('DROP TABLE IF EXISTS customers')
            self.conn.execute('DROP TABLE IF EXISTS appointment_notes')
            self.conn.execute('DROP TABLE IF EXISTS appointments')

        # create tables needed for testing
        with self.conn:
            # services table
            self.conn.execute('''
                CREATE TABLE services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    deleted INTEGER NOT NULL DEFAULT 0
                )
            ''')

            # Notes table
            self.conn.execute('''
                CREATE TABLE notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # service_notes table
            self.conn.execute('''
                CREATE TABLE service_notes (
                    service_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    PRIMARY KEY (service_id, note_id),
                    FOREIGN KEY (service_id) REFERENCES services(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                )
            ''')

            # customers table
            self.conn.execute('''
                CREATE TABLE customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT,
                    phone_number TEXT,
                    address TEXT,
                    deleted INTEGER NOT NULL DEFAULT 0
                )
            ''')

            # customer_notes table
            self.conn.execute('''
                CREATE TABLE customer_notes (
                    customer_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    PRIMARY KEY (customer_id, note_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                )
            ''')

            # appointments table
            self.conn.execute('''
                CREATE TABLE appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    location TEXT,
                    deleted INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
                )
            ''')

            # appointment_notes table
            self.conn.execute('''
                CREATE TABLE appointment_notes (
                    appointment_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    PRIMARY KEY (appointment_id, note_id),
                    FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
                )
            ''')

    def test_create_service(self):
        service = self.services_service.create_service('Bath', 'Full bath service', 30.0)
        self.assertIsInstance(service, Service)
        self.assertEqual(service.name, 'Bath')
        self.assertEqual(service.description, 'Full bath service')
        self.assertEqual(service.price, 30.0)
        self.assertEqual(service.deleted, 0)

    def test_get_service_by_id(self):
        # first creates service
        created_service = self.services_service.create_service('Trimming', 'Hair trimming', 20.0)
        service_id = created_service.id

        # retrieves service
        retrieved_service = self.services_service.get_service_by_id(service_id)
        self.assertIsNotNone(retrieved_service)
        self.assertEqual(retrieved_service.name, 'Trimming')

    def test_get_all_services(self):
        self.services_service.create_service('Service 1', 'Description 1', 10.0)
        self.services_service.create_service('Service 2', 'Description 2', 20.0)
        services = self.services_service.get_all_services()
        self.assertEqual(len(services), 2)

    def test_update_service(self):
        service = self.services_service.create_service('Old Name', 'Old Description', 50.0)
        self.services_service.update_service(service.id, 'New Name', 'New Description', 60.0)
        updated_service = self.services_service.get_service_by_id(service.id)
        self.assertEqual(updated_service.name, 'New Name')
        self.assertEqual(updated_service.description, 'New Description')
        self.assertEqual(updated_service.price, 60.0)

    def test_soft_delete_service(self):
        service = self.services_service.create_service('To be deleted', 'Will be deleted', 40.0)
        self.services_service.soft_delete_service(service.id)
        deleted_service = self.services_service.get_service_by_id(service.id)
        self.assertIsNone(deleted_service)

    def test_get_notes_for_service(self):
        # creates service and note
        service = self.services_service.create_service('Service with Notes', 'Test Service', 70.0)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', ('Note Title', 'Note Content'))
            note_id = cursor.lastrowid
            # associate  note with service
            self.services_service.add_note_to_service(service.id, note_id)

        notes = self.services_service.get_notes_for_service(service.id)
        self.assertEqual(len(notes), 1)
        self.assertIsInstance(notes[0], Note)
        self.assertEqual(notes[0].title, 'Note Title')

    def test_delete_note_for_service(self):
        # creates service and a note
        service = self.services_service.create_service('Service with Notes', 'Test Service', 70.0)
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', ('Note to Delete', 'Content'))
            note_id = cursor.lastrowid
            # associates the note with the service
            self.services_service.add_note_to_service(service.id, note_id)

        # delete the note association
        self.services_service.delete_note_for_service(service.id, note_id)
        notes = self.services_service.get_notes_for_service(service.id)
        self.assertEqual(len(notes), 0)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
