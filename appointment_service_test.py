import unittest
import sqlite3
from appointment_service import AppointmentService
from customer_service import CustomerService
from appointment import Appointment
from customer import Customer

class TestAppointmentService(unittest.TestCase):
    def setUp(self):
        # testing memory
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row
        self.conn.execute('PRAGMA foreign_keys = ON')

        # creates services
        self.customer_service = CustomerService(self.conn)
        self.appointment_service = AppointmentService(self.conn)

        # builds lemon test customer
        self.customer_service.create_customer('Lemon', 'Lime', 'lemon@lime.com')
        self.customer = self.customer_service.get_customer_by_id(1)

    def tearDown(self):
        self.conn.close()

    def test_create_appointment(self):
        appointment = self.appointment_service.create_appointment(
            customer_id=self.customer.id,
            title='Grooming For One Giant Orange Pug',
            description='mohawk style grooming.',
            start_time='2024-11-15 10:00:00',
            end_time='2024-11-15 12:00:00',
            location='1141414141 Lime Street 2'
        )
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.title, 'Grooming For One Giant Orange Pug')
        self.assertEqual(appointment.customer_id, self.customer.id)

    def test_get_appointment_by_id(self):
        # Create an appointment
        created_appointment = self.appointment_service.create_appointment(
            customer_id=self.customer.id,
            title='Vet Visit',
            description='Annual checkup.',
            start_time='2024-11-20 09:00:00',
            end_time='2024-11-20 10:00:00',
            location='Vet Clinic'
        )
        # Retrieve the appointment
        appointment = self.appointment_service.get_appointment_by_id(created_appointment.id)
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.title, 'Vet Visit')

    def test_get_upcoming_appointments(self):
        # Create past and future appointments
        self.appointment_service.create_appointment(
            customer_id=self.customer.id,
            title='Past Appointment',
            description='This is in the past.',
            start_time='2022-01-01 10:00:00',
            end_time='2022-01-01 11:00:00',
            location='Old Location'
        )
        self.appointment_service.create_appointment(
            customer_id=self.customer.id,
            title='Future Appointment',
            description='This is in the future.',
            start_time='2024-12-01 10:00:00',
            end_time='2024-12-01 11:00:00',
            location='Future Location'
        )
        appointments = self.appointment_service.get_upcoming_appointments()
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0].title, 'Future Appointment')

    def test_update_appointment(self):
        # Create an appointment
        appointment = self.appointment_service.create_appointment(
            customer_id=self.customer.id,
            title='Original Title',
            description='Original description.',
            start_time='2024-11-25 14:00:00',
            end_time='2024-11-25 15:00:00',
            location='Original Location'
        )
        # Update the appointment
        self.appointment_service.update_appointment(
            appointment.id,
            title='Updated Title',
            location='Updated Location'
        )
        # Retrieve the updated appointment
        updated_appointment = self.appointment_service.get_appointment_by_id(appointment.id)
        self.assertEqual(updated_appointment.title, 'Updated Title')
        self.assertEqual(updated_appointment.location, 'Updated Location')

    def test_soft_delete_appointment(self):
        # Create an appointment
        appointment = self.appointment_service.create_appointment(
            customer_id=self.customer.id,
            title='To Be Deleted',
            description='Will be deleted.',
            start_time='2024-11-30 10:00:00',
            end_time='2024-11-30 11:00:00',
            location='Delete Location'
        )
        # Delete the appointment
        self.appointment_service.soft_delete_appointment(appointment.id)
        # Attempt to retrieve the appointment
        deleted_appointment = self.appointment_service.get_appointment_by_id(appointment.id)
        self.assertIsNone(deleted_appointment)

    def test_update_nonexistent_appointment(self):
        with self.assertRaises(ValueError):
            self.appointment_service.update_appointment(
                appointment_id=999,
                title='Nonexistent Appointment'
            )

    def test_create_appointment_with_invalid_customer(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.appointment_service.create_appointment(
                customer_id=999,  # Nonexistent customer ID
                title='Invalid Customer',
                description='This should fail.',
                start_time='2024-11-15 10:00:00',
                end_time='2024-11-15 11:00:00',
                location='The abyss'
            )

if __name__ == '__main__':
    unittest.main()
