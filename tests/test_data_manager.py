#!/usr/bin/python3

import sys
import os
import unittest

# Add the parent directory (project root) to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now 'persistence' should be recognized as a package
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

        # Create sample objects
        self.country = Country("Japan")
        self.city = City("Tokyo", self.country)

        # Generate unique emails dynamically
        email_counter = 1
        self.user1 = User(f"testuser{email_counter}@example.com", "password123", "John", "Doe")
        email_counter += 1
        self.user2 = User(f"testuser{email_counter}@example.com", "password456", "Jane", "Smith")

        self.place = Place("Any Place", "good Place", self.user1)
        self.review = Review(4.5, "Very good Place.", self.user1, self.place)
        self.amenity = Amenity("Wifi")

        # Save entities
        self.data_manager.save(self.country)
        self.data_manager.save(self.city)
        self.data_manager.save(self.user1)
        self.data_manager.save(self.user2)  # Save both users
        self.data_manager.save(self.place)
        self.data_manager.save(self.review)

    def test_country_saved(self):
        # Retrieve and check country
        retrieved_country = self.data_manager.get(self.country.id, "Country")
        self.assertIsNotNone(retrieved_country)
        self.assertEqual(retrieved_country.name, self.country.name)

    def test_user_saved(self):
        # Retrieve and check user
        retrieved_user = self.data_manager.get(self.user.id, "User")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, self.user.email)

    def test_place_saved(self):
        # Retrieve and check place
        retrieved_place = self.data_manager.get(self.place.id, "Place")
        self.assertIsNotNone(retrieved_place)
        self.assertEqual(retrieved_place.name, self.place.name)
        self.assertEqual(retrieved_place.owner.email, self.place.owner.email)

    def test_review_saved(self):
        # Retrieve and check review
        retrieved_review = self.data_manager.get(self.review.id, "Review")
        self.assertIsNotNone(retrieved_review)
        self.assertEqual(retrieved_review.rating, self.review.rating)
        self.assertEqual(retrieved_review.text, self.review.text)

    def test_amenity_saved(self):
        # Retrieve and check amenity
        retrieved_amenity = self.data_manager.get(self.amenity.id, "Amenity")
        self.assertIsNotNone(retrieved_amenity)
        self.assertEqual(retrieved_amenity.name, self.amenity.name)

    def test_update_user(self):
        # Update user's email
        updated_user = User(self.user.email, "newpassword456", "Updated", "User")
        self.data_manager.update(updated_user)

        # Retrieve and check updated user
        retrieved_user = self.data_manager.get(updated_user.id, "User")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, updated_user.email)
        self.assertEqual(retrieved_user.password, updated_user.password)
        self.assertEqual(retrieved_user.first_name, updated_user.first_name)
        self.assertEqual(retrieved_user.last_name, updated_user.last_name)

    def test_delete_review(self):
        # Delete review
        review_id = self.review.id
        self.data_manager.delete(review_id, "Review")

        # Attempt to retrieve deleted review
        retrieved_review = self.data_manager.get(review_id, "Review")
        self.assertIsNone(retrieved_review)

if __name__ == "__main__":
    unittest.main()