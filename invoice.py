from datetime import datetime

class InvoiceLineItem:
    def __init__(self, data):
        # data is expected to be a dict with keys:
        # id, invoice_id, service_id, quantity, service_price, service_name, service_date
        self.id = data.get('id')
        self.invoice_id = data.get('invoice_id')
        self.service_id = data.get('service_id')
        self.quantity = data.get('quantity', 1)
        self.service_price = data.get('service_price', 0.0)
        self.service_name = data.get('service_name', '')
        self.service_date = data.get('service_date', '')

    def get_line_total(self):
        # returns total for this line item (price * quantity)
        return self.service_price * self.quantity

class Invoice:
    # this class represents an invoice
    def __init__(self, data):
        # data is expected to be a dict with keys:
        # id, customer_id, created_date, due_date, paid, deleted
        # plus customer info fields (from the join), like first_name, last_name, email, phone_number, address
        self.id = data.get('id')
        self.customer_id = data.get('customer_id')
        self.created_date = data.get('created_date')
        self.due_date = data.get('due_date')
        self.paid = data.get('paid', 0)
        self.deleted = data.get('deleted', 0)

        # customer info
        self.customer_first_name = data.get('first_name', '')
        self.customer_last_name = data.get('last_name', '')
        self.customer_email = data.get('email', '')
        self.customer_phone = data.get('phone_number', '')
        self.customer_address = data.get('address', '')

        self.line_items = []
        self.notes = []

        self.total = 0.0

    def calculate_total(self):
        # calculates the total of all line items
        total = 0.0
        for item in self.line_items:
            total += item.get_line_total()
        self.total = total

    def is_paid(self):
        # returns true if invoice is paid
        return self.paid == 1

    def mark_paid(self):
        # just sets the paid flag internally, actual db update in invoice_service
        self.paid = 1

    def mark_unpaid(self):
        # sets the invoice as unpaid
        self.paid = 0

    def get_customer_full_name(self):
        return f"{self.customer_first_name} {self.customer_last_name}"

