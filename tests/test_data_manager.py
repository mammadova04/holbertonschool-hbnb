#!/usr/bin/python3

import unittest
import sys
import os

# Add parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from persistence.data_manager import DataManager
from models.country import Country
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.data_manager = DataManager()

        # Create objects
        self.country = Country("Japan")
        self.city = City("Tokyo", self.country)
        self.user = User("testuser@example.com", "password123", "Nihad", "Namat")
        self.place = Place("Any Place", "good Place", self.user)
        self.review = Review(4.5, "Very good Place.", self.user, self.place)
        self.amenity = Amenity("Bilmirem")

        # Save entities
        self.data_manager.save(self.country)
        self.data_manager.save(self.city)
        self.data_manager.save(self.user)
        self.data_manager.save(self.place)
        self.data_manager.save(self.review)
        self.data_manager.save(self.amenity)

    def test_country_saved(self):
        # Retrieve and check country
        retrieved_country = self.data_manager.get(self.country.id, "Country")
        self.assertIsNotNone(retrieved_country, "Country retrieval failed")
        self.assertEqual(retrieved_country.name, self.country.name, "Country name mismatch")

    # Add other test methods for city, user, place, review, and amenity

if __name__ == "__main__":
    unittest.main()
