#!/usr/bin/python3

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity
from persistence.data_manager import DataManager

# Set up system path for project
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize DataManager
data_manager = DataManager()

# Create sample entities
user = User("test@example.com", "password123", "John", "Doe")
place = Place("Hotel", "Luxurious hotel", user)
city = City("Tokyo", "Japan")
review = Review(4.5, "Great place", user, place)
amenity = Amenity("Wi-Fi")

# Save entities
data_manager.save(user)
data_manager.save(place)
data_manager.save(city)
data_manager.save(review)
data_manager.save(amenity)

# Test cases: Get and Delete
user_retrieved = data_manager.get(user.id, "User")
place_retrieved = data_manager.get(place.id, "Place")
city_retrieved = data_manager.get(city.id, "City")
review_retrieved = data_manager.get(review.id, "Review")
amenity_retrieved = data_manager.get(amenity.id, "Amenity")

# Print retrieved entities
print("Retrieved entities:")
print(f"User: {user_retrieved}")
print(f"Place: {place_retrieved}")
print(f"City: {city_retrieved}")
print(f"Review: {review_retrieved}")
print(f"Amenity: {amenity_retrieved}")

# Test delete method
data_manager.delete(review.id, "Review")
assert data_manager.get(review.id, "Review") is None

# Output
print("Tests completed.")
