#!/usr/bin/python3
"""Importing Libraries"""
import unittest
from models.user import User

class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user1 = User(email="test_user_creation1@example.com", password="password123", first_name="John", last_name="Doe")
        self.assertIsNotNone(user1.id)
        self.assertEqual(user1.email, "test_user_creation1@example.com")

    def test_unique_email(self):
        user1 = User(email="test_unique_email1@example.com", password="password123", first_name="John", last_name="Doe")
        user2 = User(email="test_unique_email2@example.com", password="password456", first_name="Jane", last_name="Smith")
        # Ensure the same email can't be reused
        with self.assertRaises(ValueError):
            user3 = User(email="test_unique_email1@example.com", password="password789", first_name="Jack", last_name="Brown")

if __name__ == '__main__':
    unittest.main()
