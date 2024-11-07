import unittest
from appointment import Appointment
from datetime import datetime

class TestAppointment(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_initialization_with_valid_data(self):
        data = {
            'id': 1,
            'customer_id': 5,
            'title': 'Grooming Large Size',
            'description': 'Large sized golden lab grooming.',
            'start_time': '2024-11-10 10:00:00',
            'end_time': '2024-11-10 12:00:00',
            'location': '123 Lemon Lime Street',
            'is_active': 1
        }
        appointment = Appointment(data)

        self.assertEqual(appointment.id, 1)
        self.assertEqual(appointment.customer_id, 5)
        self.assertEqual(appointment.title, 'Grooming Large Size')
        self.assertEqual(appointment.description, 'Large sized golden lab grooming.')
        self.assertEqual(appointment.start_time, datetime(2024, 11, 10, 10, 0, 0))
        self.assertEqual(appointment.end_time, datetime(2024, 11, 10, 12, 0, 0))
        self.assertEqual(appointment.location, '123 Lemon Lime Street')
        self.assertEqual(appointment.is_active, 1)

    def test_date_parsing_with_invalid_dates(self):
        data = {
            'id': 2,
            'customer_id': 6,
            'title': '1000 corgi grooming',
            'start_time': 'lime time',
            'end_time': None
        }
        appointment = Appointment(data)

        self.assertIsNone(appointment.start_time)
        self.assertIsNone(appointment.end_time)

    def test_missing_fields(self):
        data = {
            'title': 'giant red dog grooming'
            # purposeful missing of other needed fields
        }
        appointment = Appointment(data)

        self.assertIsNone(appointment.id)
        self.assertIsNone(appointment.customer_id)
        self.assertEqual(appointment.title, 'giant red dog grooming')
        self.assertIsNone(appointment.description)
        self.assertIsNone(appointment.start_time)
        self.assertIsNone(appointment.end_time)
        self.assertIsNone(appointment.location)
        self.assertEqual(appointment.is_active, 1)

    def test_repr_method(self):
        data = {
            'id': 3,
            'title': 'Small Green Dog Recalibration',
            'start_time': '2024-12-01 09:00:00'
        }
        appointment = Appointment(data)

        expected_repr = "Appointment(id=3, title='Small Green Dog Recalibration', start_time=2024-12-01 09:00:00)"
        self.assertEqual(repr(appointment), expected_repr)

    def test_date_parsing_correct_format(self):
        data = {
            'start_time': '2024-11-15 14:30:00',
            'end_time': '2024-11-15 16:00:00'
        }
        appointment = Appointment(data)

        expected_start = datetime(2024, 11, 15, 14, 30, 0)
        expected_end = datetime(2024, 11, 15, 16, 0, 0)

        self.assertEqual(appointment.start_time, expected_start)
        self.assertEqual(appointment.end_time, expected_end)

    def test_date_parsing_edge_cases(self):
        # Leap year date
        data_leap_year = {
            'start_time': '2024-02-29 12:00:00'
        }
        appointment_leap_year = Appointment(data_leap_year)
        expected_leap_year = datetime(2024, 2, 29, 12, 0, 0)
        self.assertEqual(appointment_leap_year.start_time, expected_leap_year)

        # End of year date
        data_end_year = {
            'start_time': '2024-12-31 23:59:59'
        }
        appointment_end_year = Appointment(data_end_year)
        expected_end_year = datetime(2024, 12, 31, 23, 59, 59)
        self.assertEqual(appointment_end_year.start_time, expected_end_year)

    def test_invalid_data_types(self):
        data = {
            'id': 'not-an-integer',
            'customer_id': 'also-not-an-integer',
            'is_active': 'not-an-integer'
        }
        appointment = Appointment(data)

        self.assertEqual(appointment.id, 'not-an-integer')
        self.assertEqual(appointment.customer_id, 'also-not-an-integer')
        self.assertEqual(appointment.is_active, 'not-an-integer')


if __name__ == '__main__':
    unittest.main()
