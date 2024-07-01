from flask import Blueprint, request, jsonify
from models.place import Place  # Import your Place model
from models.city import City    # Import your City model
from models.amenity import Amenity  # Import your Amenity model

# Assuming DataManager or similar class is handling data operations
from data_manager import DataManager  

place_bp = Blueprint('places', __name__)

# Instantiate your data manager or persistence layer
data_manager = DataManager()

# POST /places
@place_bp.route('/places', methods=['POST'])
def create_place():
    data = request.json

    # Validate input fields
    required_fields = ['name', 'city_id', 'latitude', 'longitude', 'amenity_ids']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing '{field}' field"}), 400

    # Validate city_id
    city_id = data.get('city_id')
    city = data_manager.get(city_id, 'City')
    if not city:
        return jsonify({"error": f"City with id '{city_id}' not found"}), 404

    # Validate amenity_ids
    amenity_ids = data.get('amenity_ids', [])
    for amenity_id in amenity_ids:
        amenity = data_manager.get(amenity_id, 'Amenity')
        if not amenity:
            return jsonify({"error": f"Amenity with id '{amenity_id}' not found"}), 404

    # Create new Place instance and save
    new_place = Place(**data)
    data_manager.save(new_place)

    return jsonify(new_place.serialize()), 201

# GET /places
@place_bp.route('/places', methods=['GET'])
def get_all_places():
    all_places = [place.serialize() for place in data_manager.get_all('Place')]
    return jsonify(all_places), 200

# GET /places/{place_id}
@place_bp.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": f"Place with id '{place_id}' not found"}), 404
    return jsonify(place.serialize()), 200

# PUT /places/{place_id}
@place_bp.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    data = request.json
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": f"Place with id '{place_id}' not found"}), 404

    # Update place fields
    for key, value in data.items():
        setattr(place, key, value)

    data_manager.update(place)
    return jsonify(place.serialize()), 200

# DELETE /places/{place_id}
@place_bp.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = data_manager.get(place_id, 'Place')
    if not place:
        return jsonify({"error": f"Place with id '{place_id}' not found"}), 404

    data_manager.delete(place_id, 'Place')
    return jsonify({}), 204

