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
        self.country = Country("Japan")
        self.city = City("Tokyo", self.country)
        self.user = User("niahd.nemeto@gmail.com", "password123", "Nihad", "Namat")
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

    def test_city_saved(self):
        # Retrieve and check city
        retrieved_city = self.data_manager.get(self.city.id, "City")
        self.assertIsNotNone(retrieved_city, "City retrieval failed")
        self.assertEqual(retrieved_city.name, self.city.name, "City name mismatch")

    def test_user_saved(self):
        # Retrieve and check user
        retrieved_user = self.data_manager.get(self.user.id, "User")
        self.assertIsNotNone(retrieved_user, "User retrieval failed")
        self.assertEqual(retrieved_user.email, self.user.email, "User email mismatch")

    def test_place_saved(self):
        # Retrieve and check place
        retrieved_place = self.data_manager.get(self.place.id, "Place")
        self.assertIsNotNone(retrieved_place, "Place retrieval failed")
        self.assertEqual(retrieved_place.name, self.place.name, "Place name mismatch")

    def test_review_saved(self):
        # Retrieve and check review
        retrieved_review = self.data_manager.get(self.review.id, "Review")
        self.assertIsNotNone(retrieved_review, "Review retrieval failed")
        self.assertEqual(retrieved_review.text, self.review.text, "Review text mismatch")

    def test_amenity_saved(self):
        # Retrieve and check amenity
        retrieved_amenity = self.data_manager.get(self.amenity.id, "Amenity")
        self.assertIsNotNone(retrieved_amenity, "Amenity retrieval failed")
        self.assertEqual(retrieved_amenity.name, self.amenity.name, "Amenity name mismatch")

if __name__ == "__main__":
    unittest.main()
