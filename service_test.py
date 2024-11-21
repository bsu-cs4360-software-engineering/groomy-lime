import unittest
from service import Service

class TestService(unittest.TestCase):
    def test_service_initialization(self):
        data = {
            'id': 1,
            'name': 'Haircut',
            'description': 'Basic haircut service',
            'price': 25.0,
            'deleted': 0
        }
        service = Service(data)
        self.assertEqual(service.id, 1)
        self.assertEqual(service.name, 'Haircut')
        self.assertEqual(service.description, 'Basic haircut service')
        self.assertEqual(service.price, 25.0)
        self.assertEqual(service.deleted, 0)

    def test_service_initialization_with_missing_fields(self):
        data = {
            'name': 'Nail Trim',
            'price': 15.0
        }
        service = Service(data)
        self.assertIsNone(service.id)
        self.assertEqual(service.name, 'Nail Trim')
        self.assertIsNone(service.description)
        self.assertEqual(service.price, 15.0)
        self.assertEqual(service.deleted, 0)

    def test_service_initialization_with_invalid_price(self):
        data = {
            'name': 'Grooming',
            'description': 'Full grooming service',
            'price': 'invalid_price'
        }
        with self.assertRaises(ValueError):
            service = Service(data)

if __name__ == '__main__':
    unittest.main()
