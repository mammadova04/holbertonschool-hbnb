#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.place import Place
from models.city import City
from models.amenity import Amenity
from persistence.data_manager import DataManager

placeRoutes = Blueprint('place_routes', __name__)
dataManager = DataManager()

# Retrieve all places
@placeRoutes.route('/places', methods=['GET'])
def get_all_places():
    places = dataManager.get_all_places()
    return jsonify(places), 200

# Retrieve a specific place by ID
@placeRoutes.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = dataManager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': f'Place with id {place_id} not found'}), 404
    return jsonify(place), 200

# Create a new place
@placeRoutes.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()

    # Example validation: Check if required fields are present
    if not all(key in data for key in ('name', 'city_id', 'latitude', 'longitude', 'amenity_ids')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Example: Validate city_id exists
    city_id = data.get('city_id')
    city = dataManager.get(city_id, 'City')
    if not city:
        return jsonify({'error': f'City with id {city_id} not found'}), 404

    # Example: Validate amenity_ids exist
    amenity_ids = data.get('amenity_ids')
    for amenity_id in amenity_ids:
        if not dataManager.get(amenity_id, 'Amenity'):
            return jsonify({'error': f'Amenity with id {amenity_id} not found'}), 404

    # Create Place object and save
    place = Place(**data)
    dataManager.save(place)

    return jsonify(place), 201

# Update an existing place
@placeRoutes.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json()

    # Validate input data and check if place exists
    if not dataManager.get(place_id, 'Place'):
        return jsonify({'error': f'Place with id {place_id} not found'}), 404

    # Update the place object
    place = Place(**data)
    place.id = place_id
    dataManager.update(place)

    return jsonify(place), 200

# Delete a place
@placeRoutes.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    if not dataManager.get(place_id, 'Place'):
        return jsonify({'error': f'Place with id {place_id} not found'}), 404

    # Delete place
    dataManager.delete(place_id, 'Place')

    return '', 204
