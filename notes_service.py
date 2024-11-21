import sqlite3
from note import Note

class NotesService:
    def __init__(self, conn=None):
        self.conn = conn or sqlite3.connect('app.db')
        self.conn.row_factory = sqlite3.Row
        self.setup_database()

    def setup_database(self):
        with self.conn:
            # create notes table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
                )
            ''')
            # create customer_notes table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS customer_notes (
                    customer_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    PRIMARY KEY (customer_id, note_id),
                    FOREIGN KEY (customer_id) REFERENCES customers(id),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                )
            ''')
            # create appointment_notes table
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS appointment_notes (
                    appointment_id INTEGER NOT NULL,
                    note_id INTEGER NOT NULL,
                    PRIMARY KEY (appointment_id, note_id),
                    FOREIGN KEY (appointment_id) REFERENCES appointments(id),
                    FOREIGN KEY (note_id) REFERENCES notes(id)
                )
            ''')

    # create a note for a customer
    def create_note_for_customer(self, customer_id, title, content):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
            note_id = cursor.lastrowid
            self.conn.execute('INSERT INTO customer_notes (customer_id, note_id) VALUES (?, ?)', (customer_id, note_id))
            return self.get_note_by_id(note_id)

    # create a note for an appointment
    def create_note_for_appointment(self, appointment_id, title, content):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
            note_id = cursor.lastrowid
            self.conn.execute('INSERT INTO appointment_notes (appointment_id, note_id) VALUES (?, ?)', (appointment_id, note_id))
            return self.get_note_by_id(note_id)

    # get a note by id
    def get_note_by_id(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        data = cursor.fetchone()
        return Note(dict(data)) if data else None

    # get notes for a customer
    def get_notes_for_customer(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT n.*
            FROM notes n
            JOIN customer_notes cn ON n.id = cn.note_id
            WHERE cn.customer_id = ?
            ORDER BY datetime(n.created_at) DESC
        ''', (customer_id,))
        return [Note(dict(row)) for row in cursor.fetchall()]

    # get notes for an appointment
    def get_notes_for_appointment(self, appointment_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT n.*
            FROM notes n
            JOIN appointment_notes an ON n.id = an.note_id
            WHERE an.appointment_id = ?
            ORDER BY datetime(n.created_at) DESC
        ''', (appointment_id,))
        return [Note(dict(row)) for row in cursor.fetchall()]

    # update a note
    def update_note(self, note_id, title, content):
        with self.conn:
            self.conn.execute('UPDATE notes SET title = ?, content = ? WHERE id = ?', (title, content, note_id))

    # delete a note for a customer
    def delete_note_for_customer(self, customer_id, note_id):
        with self.conn:
            self.conn.execute('DELETE FROM customer_notes WHERE customer_id = ? AND note_id = ?', (customer_id, note_id))
            self.delete_note_if_orphaned(note_id)

    # delete a note for an appointment
    def delete_note_for_appointment(self, appointment_id, note_id):
        with self.conn:
            self.conn.execute('DELETE FROM appointment_notes WHERE appointment_id = ? AND note_id = ?', (appointment_id, note_id))
            self.delete_note_if_orphaned(note_id)

    # delete note if it has no associations
    def delete_note_if_orphaned(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM customer_notes WHERE note_id = ?', (note_id,))
        customer_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM appointment_notes WHERE note_id = ?', (note_id,))
        appointment_count = cursor.fetchone()['count']
        if customer_count == 0 and appointment_count == 0:
            self.conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
