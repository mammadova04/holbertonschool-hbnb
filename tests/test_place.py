#!/usr/bin/python3
"""Importing Libraries"""
import unittest
from models.user import User
from models.place import Place

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.user = User(email="test_place_creation@example.com", password="password123", first_name="Host", last_name="User")

    def test_place_creation(self):
        place = Place(name="Cozy House", description="A lovely place to stay", host=self.user)
        self.assertIsNotNone(place.id)
        self.assertEqual(place.host, self.user)

    def test_host_must_be_user(self):
        with self.assertRaises(ValueError):
            place = Place(name="Invalid Host Place", description="This should fail", host="not_a_user")

if __name__ == '__main__':
    unittest.main()
