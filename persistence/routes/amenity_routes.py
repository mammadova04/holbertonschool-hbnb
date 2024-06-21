#!/usr/bin/python3

from flask import Blueprint, request, jsonify
from models.amenity import Amenity
from persistence.data_manager import DataManager
from datetime import datetime

data_manager = DataManager()
amenityRoutes = Blueprint('amenityRoutes', __name__)

@amenityRoutes.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrieve a list of all amenities"""
    amenities = data_manager.get_all_amenities()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200

@amenityRoutes.route('/amenities/<string:amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieve detailed information about a specific amenity"""
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        return jsonify({'message': 'Amenity not found'}), 404
    return jsonify(amenity.to_dict()), 200

@amenityRoutes.route('/amenities', methods=['POST'])
def create_amenity():
    """Create a new amenity"""
    data = request.get_json()
    if data_manager.get_amenity_by_name(data['name']):
        return jsonify({'message': 'Amenity already exists'}), 409
    amenity = Amenity(**data)
    data_manager.save(amenity)
    return jsonify({'message': 'Amenity created successfully'}), 201

@amenityRoutes.route('/amenities/<string:amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update an existing amenity"""
    amenity = data_manager.get(amenity_id, 'Amenity')
    if not amenity:
        return jsonify({'message': 'Amenity not found'}), 404
    data = request.get_json()
    amenity.update(data)
    data_manager.update(amenity)
    return jsonify({'message': 'Amenity updated successfully'}), 200

@amenityRoutes.route('/amenities/<string:amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Delete a specific amenity"""
    if not data_manager.get(amenity_id, 'Amenity'):
        return jsonify({'message': 'Amenity not found'}), 404
    data_manager.delete(amenity_id, 'Amenity')
    return '', 204

