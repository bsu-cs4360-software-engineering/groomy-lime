import unittest
import sqlite3
import bcrypt
from user_manager import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        # creates in memory database for SQLite
        self.conn = sqlite3.connect(':memory:')
        self.user_manager = UserManager(conn=self.conn)
        self.user_manager.setup_database()

    def test_hash_password(self):
        password = 'turtle'
        hashed_password = self.user_manager.hash_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')))

    def test_create_user(self):
        self.user_manager.create_user('shrimp', 'fishy', 'crab@lobster.com', 'turkey')
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', ('crab@lobster.com',))
        user = cursor.fetchone()
        self.assertIsNotNone(user)

    def test_check_password(self):
        self.user_manager.create_user('Salmon', 'Cod', 'krill@urchin.com', 'cool_fish')
        self.assertTrue(self.user_manager.check_password('krill@urchin.com', 'cool_fish'))
        self.assertFalse(self.user_manager.check_password('krill@urchin.com', 'uncool_fish'))

if __name__ == '__main__':
    unittest.main()
