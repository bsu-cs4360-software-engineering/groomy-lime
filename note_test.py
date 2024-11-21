import unittest
from note import Note
from datetime import datetime

class TestNote(unittest.TestCase):
    def test_note_initialization(self):
        data = {
            'id': 1,
            'title': 'Test Title',
            'content': 'Test Content',
            'created_at': '2023-10-22 12:34:56'
        }
        note = Note(data)
        self.assertEqual(note.id, 1)
        self.assertEqual(note.title, 'Test Title')
        self.assertEqual(note.content, 'Test Content')
        self.assertEqual(note.created_at, datetime(2023, 10, 22, 12, 34, 56))

    def test_invalid_created_at(self):
        data = {
            'id': 2,
            'title': 'Invalid Date',
            'content': 'Content',
            'created_at': 'invalid-date'
        }
        note = Note(data)
        self.assertIsNone(note.created_at)

    def test_missing_created_at(self):
        data = {
            'id': 3,
            'title': 'No Date',
            'content': 'Content without date',
            'created_at': None
        }
        note = Note(data)
        self.assertIsNone(note.created_at)

if __name__ == '__main__':
    unittest.main()
