# persistence/routes/place_routes.py

from flask import Blueprint, jsonify, request
from models.place import Place
from models.city import City  # Assuming City model exists
from models.amenity import Amenity  # Assuming Amenity model exists
from persistence.data_manager import DataManager

place_bp = Blueprint('place', __name__)
data_manager = DataManager()

@place_bp.route('/places', methods=['POST'])
def create_place():
    try:
        data = request.get_json()
        required_fields = ['name', 'city_id', 'latitude', 'longitude', 'amenity_ids']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate city_id
        city_id = data.get('city_id')
        city = data_manager.get(city_id, 'City')
        if not city:
            return jsonify({'error': f'City with id {city_id} not found'}), 404
        
        # Validate amenity_ids
        amenity_ids = data.get('amenity_ids', [])
        for amenity_id in amenity_ids:
            if not data_manager.get(amenity_id, 'Amenity'):
                return jsonify({'error': f'Amenity with id {amenity_id} not found'}), 404
        
        # Create and save Place object
        place = Place(**data)
        data_manager.save(place)

        return jsonify(place), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@place_bp.route('/places', methods=['GET'])
def get_all_places():
    try:
        places = data_manager.get_all_places()
        return jsonify(places), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@place_bp.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    try:
        place = data_manager.get(place_id, 'Place')
        if not place:
            return jsonify({'error': f'Place with id {place_id} not found'}), 404
        return jsonify(place), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@place_bp.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    try:
        data = request.get_json()
        if not data_manager.get(place_id, 'Place'):
            return jsonify({'error': f'Place with id {place_id} not found'}), 404
        
        # Update place object
        place = Place(**data)
        place.id = place_id
        data_manager.update(place)

        return jsonify(place), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@place_bp.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    try:
        if not data_manager.get(place_id, 'Place'):
            return jsonify({'error': f'Place with id {place_id} not found'}), 404
        
        data_manager.delete(place_id, 'Place')

        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
