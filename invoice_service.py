import sqlite3
from invoice import Invoice, InvoiceLineItem
from note import Note

class InvoiceService:
    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.setup_database()

    def setup_database(self):
        # if invoice_setup.py already handles table creation, this may be empty
        pass

    def create_invoice(self, customer_id, due_date=None, line_items=None, notes_content=None):
        # line_items is a list of dicts: [{"service_id": x, "service_date": y}, ...]
        # notes_content is a string for optional notes

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO invoice_header (customer_id, created_date, due_date, paid, deleted)
                VALUES (?, datetime('now', 'localtime'), ?, 0, 0)
            ''', (customer_id, due_date))
            invoice_id = cursor.lastrowid

            # add line items if provided
            if line_items:
                for li in line_items:
                    service_id = li["service_id"]
                    service_date = li["service_date"]

                    # you need the service details here, assume you have a method to get service price/name
                    # or you must have logic to fetch that from the services table:
                    svc_cursor = self.conn.cursor()
                    svc_cursor.execute('SELECT name, price FROM services WHERE id = ? AND deleted = 0', (service_id,))
                    svc_data = svc_cursor.fetchone()
                    if not svc_data:
                        raise ValueError("Invalid service_id or service deleted.")
                    service_name = svc_data['name']
                    service_price = svc_data['price']

                    # for now, quantity is 1
                    quantity = 1
                    self.conn.execute('''
                        INSERT INTO invoice_detail (invoice_id, service_id, quantity, service_price, service_name, service_date)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (invoice_id, service_id, quantity, service_price, service_name, service_date))

            # if notes_content is provided, create a note and associate it
            if notes_content and notes_content.strip():
                # insert note into notes table
                n_cur = self.conn.cursor()
                n_cur.execute('INSERT INTO notes (title, content) VALUES (?, ?)', ("Invoice Note", notes_content))
                note_id = n_cur.lastrowid
                self.conn.execute('INSERT INTO invoice_notes (invoice_id, note_id) VALUES (?, ?)', (invoice_id, note_id))

            return self.get_invoice_by_id(invoice_id)

    def get_invoice_by_id(self, invoice_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT ih.id, ih.customer_id, ih.created_date, ih.due_date, ih.paid, ih.deleted,
                   c.first_name, c.last_name, c.email, c.phone_number, c.address
            FROM invoice_header ih
            JOIN customers c ON ih.customer_id = c.id
            WHERE ih.id = ? AND ih.deleted = 0
        ''', (invoice_id,))
        header_data = cursor.fetchone()
        if not header_data:
            return None

        invoice = Invoice(dict(header_data))

        # get line items
        invoice.line_items = self.get_line_items_for_invoice(invoice_id)

        # get notes
        invoice.notes = self.get_notes_for_invoice(invoice_id)

        # calculate total
        invoice.calculate_total()

        return invoice

    def get_line_items_for_invoice(self, invoice_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, invoice_id, service_id, quantity, service_price, service_name, service_date
            FROM invoice_detail
            WHERE invoice_id = ?
        ''', (invoice_id,))
        rows = cursor.fetchall()

        line_items = []
        for row in rows:
            line_item = InvoiceLineItem(dict(row))
            line_items.append(line_item)
        return line_items

    def get_notes_for_invoice(self, invoice_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT n.id, n.title, n.content, n.created_at
            FROM notes n
            JOIN invoice_notes inotes ON n.id = inotes.note_id
            WHERE inotes.invoice_id = ?
            ORDER BY datetime(n.created_at) DESC
        ''', (invoice_id,))
        rows = cursor.fetchall()

        notes = [Note(dict(r)) for r in rows]
        return notes

    def add_note_to_invoice(self, invoice_id, note_id):
        with self.conn:
            self.conn.execute('''
                INSERT INTO invoice_notes (invoice_id, note_id) VALUES (?, ?)
            ''', (invoice_id, note_id))

    def delete_note_for_invoice(self, invoice_id, note_id):
        with self.conn:
            self.conn.execute('DELETE FROM invoice_notes WHERE invoice_id = ? AND note_id = ?', (invoice_id, note_id))
            self.delete_note_if_orphaned(note_id)

    def delete_note_if_orphaned(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM customer_notes WHERE note_id = ?', (note_id,))
        customer_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM appointment_notes WHERE note_id = ?', (note_id,))
        appointment_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM service_notes WHERE note_id = ?', (note_id,))
        service_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM invoice_notes WHERE note_id = ?', (note_id,))
        invoice_count = cursor.fetchone()['count']

        if customer_count == 0 and appointment_count == 0 and service_count == 0 and invoice_count == 0:
            with self.conn:
                self.conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))

    def mark_invoice_paid(self, invoice_id):
        with self.conn:
            self.conn.execute('UPDATE invoice_header SET paid = 1 WHERE id = ?', (invoice_id,))

    def soft_delete_invoice(self, invoice_id):
        with self.conn:
            self.conn.execute('UPDATE invoice_header SET deleted = 1 WHERE id = ?', (invoice_id,))

    def get_invoices(self, show_only_unpaid=True):
        cursor = self.conn.cursor()
        if show_only_unpaid:
            cursor.execute('''
                SELECT id
                FROM invoice_header
                WHERE deleted = 0 AND paid = 0
                ORDER BY datetime(created_date) DESC
            ''')
        else:
            cursor.execute('''
                SELECT id
                FROM invoice_header
                WHERE deleted = 0
                ORDER BY datetime(created_date) DESC
            ''')

        rows = cursor.fetchall()
        invoices = []
        for row in rows:
            inv = self.get_invoice_by_id(row['id'])
            if inv:
                invoices.append(inv)
        return invoices

    def update_invoice(self, invoice_id, customer_id, due_date, line_items, notes_content):
        with self.conn:
            # update header
            self.conn.execute('''
                UPDATE invoice_header
                SET customer_id = ?, due_date = ?
                WHERE id = ?
            ''', (customer_id, due_date, invoice_id))

            # remove old line items
            self.conn.execute('DELETE FROM invoice_detail WHERE invoice_id = ?', (invoice_id,))

            # add new line items
            for li in line_items:
                service_id = li["service_id"]
                service_date = li["service_date"]
                # get service info
                svc_cursor = self.conn.cursor()
                svc_cursor.execute('SELECT name, price FROM services WHERE id = ? AND deleted = 0', (service_id,))
                svc_data = svc_cursor.fetchone()
                if not svc_data:
                    raise ValueError("Invalid service_id or service deleted.")
                service_name = svc_data['name']
                service_price = svc_data['price']
                quantity = 1
                self.conn.execute('''
                    INSERT INTO invoice_detail (invoice_id, service_id, quantity, service_price, service_name, service_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (invoice_id, service_id, quantity, service_price, service_name, service_date))

            self.conn.execute('DELETE FROM invoice_notes WHERE invoice_id = ?', (invoice_id,))

            if notes_content and notes_content.strip():
                # insert new note
                n_cur = self.conn.cursor()
                n_cur.execute('INSERT INTO notes (title, content) VALUES (?, ?)', ("Invoice Note", notes_content))
                note_id = n_cur.lastrowid
                self.conn.execute('INSERT INTO invoice_notes (invoice_id, note_id) VALUES (?, ?)', (invoice_id, note_id))

        return self.get_invoice_by_id(invoice_id)

