# customer_test.py

import unittest
from customer import Customer

class TestCustomer(unittest.TestCase):
    def test_customer_dict(self):
        data = {
            'id': 1,
            'first_name': 'Lemon',
            'last_name': 'Lime',
            'email': 'lemon.lime@kiwi.com',
            'phone_number': '555-1234',
            'address': '123 Orange St',
            'is_active': 1
        }
        customer = Customer(data)
        self.assertEqual(customer.id, 1)
        self.assertEqual(customer.first_name, 'Lemon')
        self.assertEqual(customer.last_name, 'Lime')
        self.assertEqual(customer.email, 'lemon.lime@kiwi.com')
        self.assertEqual(customer.phone_number, '555-1234')
        self.assertEqual(customer.address, '123 Orange St')
        self.assertTrue(customer.is_active)

if __name__ == '__main__':
    unittest.main()
