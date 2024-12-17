import unittest
import sqlite3
from invoice_service import InvoiceService
from invoice_setup import setup_invoice_tables

class TestInvoiceService(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')
        # customers
        self.conn.execute('''
            CREATE TABLE customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone_number TEXT,
                address TEXT,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        ''')
        # services
        self.conn.execute('''
            CREATE TABLE services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                price REAL,
                deleted INTEGER NOT NULL DEFAULT 0
            )
        ''')
        # notes
        self.conn.execute('''
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        setup_invoice_tables(self.conn)
        self.service = InvoiceService(self.conn)
        # insert customer "lemon lime"
        self.conn.execute("INSERT INTO customers (first_name, last_name, email, phone_number, address) VALUES ('lemon','lime','ll@example.com','111','citrus ave')")
        self.customer_id = self.conn.execute("SELECT id FROM customers").fetchone()['id']
        # insert a service "citrus cleaning"
        self.conn.execute("INSERT INTO services (name, description, price, deleted) VALUES ('citrus cleaning','cleaning with lime','10.0',0)")
        self.service_id = self.conn.execute("SELECT id FROM services").fetchone()['id']

    def test_create_invoice(self):
        inv = self.service.create_invoice(self.customer_id,'2025-01-01',[{'service_id':self.service_id,'service_date':'2025-01-02'}],"zesty note")
        self.assertIsNotNone(inv)
        self.assertEqual(inv.customer_id, self.customer_id)
        self.assertEqual(len(inv.line_items),1)
        self.assertEqual(len(inv.notes),1)

    def test_get_invoice_by_id(self):
        inv = self.service.create_invoice(self.customer_id,'2025-01-01',[{'service_id':self.service_id,'service_date':'2025-01-02'}],"tart note")
        fetched = self.service.get_invoice_by_id(inv.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.id, inv.id)

    def test_mark_invoice_paid(self):
        inv = self.service.create_invoice(self.customer_id,'2025-01-01',[{'service_id':self.service_id,'service_date':'2025-01-02'}],"sweet note")
        self.service.mark_invoice_paid(inv.id)
        fetched = self.service.get_invoice_by_id(inv.id)
        self.assertTrue(fetched.is_paid())

    def test_soft_delete_invoice(self):
        inv = self.service.create_invoice(self.customer_id,'2025-01-01',[{'service_id':self.service_id,'service_date':'2025-01-02'}],"bitter note")
        self.service.soft_delete_invoice(inv.id)
        gone = self.service.get_invoice_by_id(inv.id)
        self.assertIsNone(gone)

if __name__ == '__main__':
    unittest.main()
