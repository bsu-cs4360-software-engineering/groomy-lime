import unittest
import sqlite3
from customer_service import CustomerService
from customer import Customer

class TestCustomerService(unittest.TestCase):
    def setUp(self):
        # creates testing database
        self.conn = sqlite3.connect(':memory:')
        self.customer_service = CustomerService(self.conn)
        self.customer_service.setup_database()

    def test_create_customer(self):
        self.customer_service.create_customer('Lemon', 'Lime', 'lemon@lime.com', '1234567890', '123 Citrus St')
        customer = self.customer_service.get_customer_by_id(1)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.first_name, 'Lemon')
        self.assertEqual(customer.last_name, 'Lime')
        self.assertEqual(customer.email, 'lemon@lime.com')

    def test_create_customer_duplicate_email(self):
        self.customer_service.create_customer('Orange', 'Peach', 'orange@peach.com')
        with self.assertRaises(ValueError):
            self.customer_service.create_customer('Mango', 'Berry', 'orange@peach.com')

    def test_get_all_customers(self):
        self.customer_service.create_customer('Lemon', 'Lime', 'lemon@lime.com')
        self.customer_service.create_customer('Orange', 'Peach', 'orange@peach.com')
        customers = self.customer_service.get_all_customers()
        self.assertEqual(len(customers), 2)

    def test_update_customer(self):
        self.customer_service.create_customer('Lemon', 'Lime', 'lemon@lime.com')
        customer = self.customer_service.get_customer_by_id(1)
        self.customer_service.update_customer(customer.id, first_name='Lemona')
        updated_customer = self.customer_service.get_customer_by_id(1)
        self.assertEqual(updated_customer.first_name, 'Lemona')

    def test_update_customer_duplicate_email(self):
        self.customer_service.create_customer('Lemon', 'Lime', 'lemon@lime.com')
        self.customer_service.create_customer('Orange', 'Peach', 'orange@peach.com')
        customer = self.customer_service.get_customer_by_id(1)
        with self.assertRaises(ValueError):
            self.customer_service.update_customer(customer.id, email='orange@peach.com')

    def test_soft_delete_customer(self):
        self.customer_service.create_customer('Lemon', 'Lime', 'lemon@lime.com')
        self.customer_service.soft_delete_customer(1)
        customer = self.customer_service.get_customer_by_id(1)
        self.assertIsNone(customer)
        customers = self.customer_service.get_all_customers()
        self.assertEqual(len(customers), 0)

    def tearDown(self):
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
