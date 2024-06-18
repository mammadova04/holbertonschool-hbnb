#!/usr/bin/python3
import sys
import os

# Add the root directory of your project to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import modules relative to the project root
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity
from persistence.data_manager import DataManager

# Helper function to perform assertions
def assert_equal(actual, expected, message):
    if actual == expected:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")

# Initialize DataManager
data_manager = DataManager()

# Create sample entities
user = User("testuserssssssss@example.com", "password123", "John", "Doe")
place = Place("Hotel", "Luxurious hotel", user)
city = City("Tokyo", "Japan")
review = Review(4.5, "Great place", user, place)
amenity = Amenity("Wi-Fi")

# Save entities to DataManager
data_manager.save(user)
data_manager.save(place)
data_manager.save(city)
data_manager.save(review)
data_manager.save(amenity)

# Test cases
# Test get method
assert_equal(data_manager.get(user.id, "User").email, user.email, "Retrieve user by ID")
assert_equal(data_manager.get(place.id, "Place").name, place.name, "Retrieve place by ID")
assert_equal(data_manager.get(city.id, "City").name, city.name, "Retrieve city by ID")
assert_equal(data_manager.get(review.id, "Review").rating, review.rating, "Retrieve review by ID")
assert_equal(data_manager.get(amenity.id, "Amenity").name, amenity.name, "Retrieve amenity by ID")

# Test update method
updated_user = User(user.email, "newpassword456", "Updated", "User")
data_manager.update(updated_user)
assert_equal(data_manager.get(updated_user.id, "User").password, updated_user.password, "Update user password")

# Test delete method
data_manager.delete(review.id, "Review")
assert data_manager.get(review.id, "Review") is None, "Review should be deleted"

# Output results
print("Tests completed.")