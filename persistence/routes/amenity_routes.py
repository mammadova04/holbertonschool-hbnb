#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from persistence.data_manager import DataManager
from models.amenity import Amenity
from datetime import datetime

amenityRoutes = Blueprint('amenity_routes', __name__)
dataManager = DataManager()

# Helper function to convert Amenity object to dictionary
def amenity_to_dict(amenity):
    return {
        'id': amenity.id,
        'name': amenity.name,
        'created_at': amenity.created_at,
        'updated_at': amenity.updated_at
    }

# POST /amenities - Create a new amenity
@amenityRoutes.route('/amenities', methods=['POST'])
def add_amenity():
    data = request.json

    if 'name' not in data:
        return jsonify({'error': 'Missing required field "name"'}), 400

    name = data['name']

    # Check if amenity name already exists
    existing_amenity = next((amenity for amenity in dataManager.dataStore['Amenity'].values() if amenity.name == name), None)
    if existing_amenity:
        return jsonify({'error': 'Amenity with this name already exists'}), 409

    new_amenity = Amenity(name=name, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    dataManager.save_amenity(new_amenity)

    return jsonify(amenity_to_dict(new_amenity)), 201

# GET /amenities - Retrieve all amenities
@amenityRoutes.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity_to_dict(amenity) for amenity in dataManager.get_all_amenities()]
    return jsonify(amenities), 200

# GET /amenities/<amenity_id> - Retrieve a specific amenity
@amenityRoutes.route('/amenities/<int:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = dataManager.get_amenity(amenity_id)

    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404

    return jsonify(amenity_to_dict(amenity)), 200

# PUT /amenities/<amenity_id> - Update an existing amenity
@amenityRoutes.route('/amenities/<int:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.json

    if 'name' not in data:
        return jsonify({'error': 'Missing required field "name"'}), 400

    amenity = dataManager.get_amenity(amenity_id)

    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404

    name = data['name']

    # Check if another amenity with the same name already exists
    existing_amenity = next((a for a in dataManager.dataStore['Amenity'].values() if a.id != amenity_id and a.name == name), None)
    if existing_amenity:
        return jsonify({'error': 'Amenity with this name already exists'}), 409

    amenity.name = name
    amenity.updated_at = datetime.utcnow()
    dataManager.update_amenity(amenity)

    return jsonify(amenity_to_dict(amenity)), 200

# DELETE /amenities/<amenity_id> - Delete a specific amenity
@amenityRoutes.route('/amenities/<int:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = dataManager.get_amenity(amenity_id)

    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404

    dataManager.delete_amenity(amenity_id)

    return '', 204
