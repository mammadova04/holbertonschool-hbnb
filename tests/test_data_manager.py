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
user1 = User("test@example.com", "password123", "John", "Doe")
user2 = User("another@example.com", "securepassword", "Alice", "Smith")
place = Place("Hotel", "Luxurious hotel", user1)
city = City("Tokyo", "Japan")
review = Review(4.5, "Great place", user1, place)
amenity = Amenity("Wi-Fi")

# Save entities
data_manager.save(user1)
data_manager.save(user2)
data_manager.save(place)
data_manager.save(city)
data_manager.save(review)
data_manager.save(amenity)

# Test cases: Get and Delete
user1_retrieved = data_manager.get(user1.id, "User")
user2_retrieved = data_manager.get(user2.id, "User")
place_retrieved = data_manager.get(place.id, "Place")
city_retrieved = data_manager.get(city.id, "City")
review_retrieved = data_manager.get(review.id, "Review")
amenity_retrieved = data_manager.get(amenity.id, "Amenity")

# Print retrieved entities
print("Retrieved entities:")
print(f"User 1: {user1_retrieved}")
print(f"User 2: {user2_retrieved}")
print(f"Place: {place_retrieved}")
print(f"City: {city_retrieved}")
print(f"Review: {review_retrieved}")
print(f"Amenity: {amenity_retrieved}")

# Test delete method
data_manager.delete(review.id, "Review")
print(f"Review with ID {review.id} deleted.")

# Retrieve all entities again
user1_retrieved = data_manager.get(user1.id, "User")
user2_retrieved = data_manager.get(user2.id, "User")
place_retrieved = data_manager.get(place.id, "Place")
city_retrieved = data_manager.get(city.id, "City")
review_retrieved = data_manager.get(review.id, "Review")
amenity_retrieved = data_manager.get(amenity.id, "Amenity")

# Print updated entities
print("\nUpdated entities after delete:")
print(f"User 1: {user1_retrieved}")
print(f"User 2: {user2_retrieved}")
print(f"Place: {place_retrieved}")
print(f"City: {city_retrieved}")
print(f"Review: {review_retrieved}")
print(f"Amenity: {amenity_retrieved}")

# Add another entity for testing
new_user = User("newuser@example.com", "newpassword", "Jane", "Doe")
data_manager.save(new_user)

# Retrieve and print all entities again
user1_retrieved = data_manager.get(user1.id, "User")
user2_retrieved = data_manager.get(user2.id, "User")
new_user_retrieved = data_manager.get(new_user.id, "User")
place_retrieved = data_manager.get(place.id, "Place")
city_retrieved = data_manager.get(city.id, "City")
review_retrieved = data_manager.get(review.id, "Review")
amenity_retrieved = data_manager.get(amenity.id, "Amenity")

# Print all entities after adding new user
print("\nAll entities after adding new user:")
print(f"User 1: {user1_retrieved}")
print(f"User 2: {user2_retrieved}")
print(f"New User: {new_user_retrieved}")
print(f"Place: {place_retrieved}")
print(f"City: {city_retrieved}")
print(f"Review: {review_retrieved}")
print(f"Amenity: {amenity_retrieved}")

# Output
print("\nTests completed.")
