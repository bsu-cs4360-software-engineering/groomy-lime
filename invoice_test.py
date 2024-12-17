import unittest
from invoice import Invoice, InvoiceLineItem

class TestInvoice(unittest.TestCase):
    def setUp(self):
        data = {
            'id':1,
            'customer_id':99,
            'created_date':'2025-01-10',
            'due_date':'2025-02-10',
            'paid':0,
            'deleted':0,
            'first_name':'lemon',
            'last_name':'lime',
            'email':'citrus@example.com',
            'phone_number':'555',
            'address':'citrus lane'
        }
        self.invoice = Invoice(data)

    def test_initial_state(self):
        self.assertEqual(self.invoice.id,1)
        self.assertEqual(self.invoice.customer_id,99)
        self.assertFalse(self.invoice.is_paid())

    def test_calculate_total(self):
        item_data = {
            'id':1,
            'invoice_id':1,
            'service_id':5,
            'quantity':2,
            'service_price':10.0,
            'service_name':'citrus service',
            'service_date':'2025-01-15'
        }
        li = InvoiceLineItem(item_data)
        self.invoice.line_items.append(li)
        self.invoice.calculate_total()
        self.assertEqual(self.invoice.total,20.0)

    def test_get_customer_full_name(self):
        self.assertEqual(self.invoice.get_customer_full_name(),'lemon lime')

    def test_mark_paid_unpaid(self):
        self.invoice.mark_paid()
        self.assertTrue(self.invoice.is_paid())
        self.invoice.mark_unpaid()
        self.assertFalse(self.invoice.is_paid())

if __name__ == '__main__':
    unittest.main()
