import unittest
import sqlite3
from notes_service import NotesService
from note import Note

class TestNotesService(unittest.TestCase):
    def setUp(self):
        # use an in-memory SQLite database for testing
        self.conn = sqlite3.connect(':memory:')
        self.notes_service = NotesService(self.conn)
        self.setup_test_tables()

    def setup_test_tables(self):
        # create customers and appointments tables needed for foreign key constraints
        with self.conn:
            self.conn.execute('''
                CREATE TABLE customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone_number TEXT,
                    address TEXT,
                    deleted INTEGER NOT NULL DEFAULT 0
                )
            ''')
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
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                )
            ''')

    def test_create_note_for_customer(self):
        # Insert a test customer
        with self.conn:
            self.conn.execute('''
                INSERT INTO customers (first_name, last_name, email)
                VALUES (?, ?, ?)
            ''', ('John', 'Doe', 'john.doe@example.com'))
            customer_id = self.conn.execute('SELECT id FROM customers').fetchone()[0]

        # create a note
        note = self.notes_service.create_note_for_customer(customer_id, 'Test Note', 'This is a test note.')
        self.assertIsInstance(note, Note)
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(note.content, 'This is a test note.')

    def test_get_notes_for_customer(self):
        # insert a test customer and notes
        with self.conn:
            self.conn.execute('''
                INSERT INTO customers (first_name, last_name, email)
                VALUES (?, ?, ?)
            ''', ('Jane', 'Smith', 'jane.smith@example.com'))
            customer_id = self.conn.execute('SELECT id FROM customers').fetchone()[0]

        self.notes_service.create_note_for_customer(customer_id, 'Note 1', 'Content 1')
        self.notes_service.create_note_for_customer(customer_id, 'Note 2', 'Content 2')

        notes = self.notes_service.get_notes_for_customer(customer_id)
        self.assertEqual(len(notes), 2)

    def test_delete_note_for_customer(self):
        # insert a test customer and note
        with self.conn:
            self.conn.execute('''
                INSERT INTO customers (first_name, last_name, email)
                VALUES (?, ?, ?)
            ''', ('Alice', 'Johnson', 'alice.johnson@example.com'))
            customer_id = self.conn.execute('SELECT id FROM customers').fetchone()[0]

        note = self.notes_service.create_note_for_customer(customer_id, 'Delete Me', 'To be deleted')

        # deletes the note
        self.notes_service.delete_note_for_customer(customer_id, note.id)

        # verify the note is deleted
        notes = self.notes_service.get_notes_for_customer(customer_id)
        self.assertEqual(len(notes), 0)

    def test_update_note(self):
        # create a note without association
        with self.conn:
            self.conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', ('Old Title', 'Old Content'))
            note_id = self.conn.execute('SELECT id FROM notes').fetchone()[0]

        # update the note
        self.notes_service.update_note(note_id, 'New Title', 'New Content')

        # verify the update
        updated_note = self.notes_service.get_note_by_id(note_id)
        self.assertEqual(updated_note.title, 'New Title')
        self.assertEqual(updated_note.content, 'New Content')

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
