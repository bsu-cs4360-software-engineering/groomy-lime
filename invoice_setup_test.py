import unittest
import sqlite3
from invoice_setup import setup_invoice_tables

class TestInvoiceSetup(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row

    def test_tables_created(self):
        # checking if tables exist
        setup_invoice_tables(self.conn)
        c = self.conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoice_header'")
        self.assertIsNotNone(c.fetchone())
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoice_detail'")
        self.assertIsNotNone(c.fetchone())
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='invoice_notes'")
        self.assertIsNotNone(c.fetchone())

    def test_foreign_keys(self):
        # checking foreign keys on
        setup_invoice_tables(self.conn)
        c = self.conn.cursor()
        c.execute("PRAGMA foreign_keys;")
        val = c.fetchone()[0]
        self.assertEqual(val, 1)

if __name__ == '__main__':
    unittest.main()
