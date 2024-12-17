import sqlite3

# sets up database tables for invoices
def setup_invoice_tables(conn):
    conn.execute('PRAGMA foreign_keys = ON')

    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS invoice_header (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                created_date TEXT NOT NULL,
                due_date TEXT,
                paid INTEGER NOT NULL DEFAULT 0,
                deleted INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS invoice_detail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER NOT NULL,
                service_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                service_price REAL NOT NULL,
                service_name TEXT NOT NULL,
                service_date TEXT,
                FOREIGN KEY (invoice_id) REFERENCES invoice_header(id) ON DELETE CASCADE,
                FOREIGN KEY (service_id) REFERENCES services(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS invoice_notes (
                invoice_id INTEGER NOT NULL,
                note_id INTEGER NOT NULL,
                PRIMARY KEY (invoice_id, note_id),
                FOREIGN KEY (invoice_id) REFERENCES invoice_header(id) ON DELETE CASCADE,
                FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
            )
        ''')

class Invoice:
    def __init__(self, invoice_id=None, invoice_number=None, created_date=None, due_date=None,
                 customer_id=None, total=0.0, paid=0, deleted=0, line_items=None, notes=None):
        self.id = invoice_id
        self.invoice_number = invoice_number
        self.created_date = created_date
        self.due_date = due_date
        self.customer_id = customer_id
        self.total = total
        self.paid = paid
        self.deleted = deleted
        self.line_items = line_items if line_items is not None else []
        self.notes = notes if notes is not None else []
