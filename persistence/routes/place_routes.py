# place_routes.py

from flask import Blueprint, jsonify, request
from models.place import Place
from models.city import City
from models.amenity import Amenity
from data_manager import DataManager

place_bp = Blueprint('place', __name__)
data_manager = DataManager()

@place_bp.route('/places', methods=['POST'])
def create_place():
    data = request.get_json()
    # Validate input data
    # Example validation: Check if required fields are present
    if not all(key in data for key in ('name', 'city_id', 'latitude', 'longitude', 'amenity_ids')):
        return jsonify({'error': 'Missing required fields'}), 400

    # Example: Validate city_id exists
    city_id = data.get('city_id')
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({'error': f'City with id {city_id} not found'}), 404

    # Example: Validate amenity_ids exist
    amenity_ids = data.get('amenity_ids')
    for amenity_id in amenity_ids:
        if not data_manager.get(amenity_id, 'Amenity'):
            return jsonify({'error': f'Amenity with id {amenity_id} not found'}), 404

    # Create Place object and save
    place = Place(**data)
    data_manager.save(place)

    return jsonify(place), 201

@place_bp.route('/places', methods=['GET'])
def get_all_places():
    # Retrieve all places from data manager
    places = data_manager.get_all_places()
    return jsonify(places), 200

@place_bp.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    # Retrieve specific place by ID
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({'error': f'Place with id {place_id} not found'}), 404
    return jsonify(place), 200

@place_bp.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.get_json()
    # Validate input data and check if place exists
    if not data_manager.get(place_id, 'Place'):
        return jsonify({'error': f'Place with id {place_id} not found'}), 404

    # Update the place object
    place = Place(**data)
    place.id = place_id
    data_manager.update(place)

    return jsonify(place), 200

@place_bp.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    # Check if place exists
    if not data_manager.get(place_id, 'Place'):
        return jsonify({'error': f'Place with id {place_id} not found'}), 404

    # Delete place
    data_manager.delete(place_id, 'Place')

    return '', 204

