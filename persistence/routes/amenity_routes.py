#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from datetime import datetime
from models.amenity import Amenity
from persistence.data_manager import DataManager

amenityRoutes = Blueprint('amenity_routes', __name__)
dataManager = DataManager()

def amenityToDict(amenity):
    return {
        'id': amenity.id,
        'name': amenity.name,
        'created_at': amenity.created_at,
        'updated_at': amenity.updated_at
    }

# Create a new amenity
@amenityRoutes.route('/amenities', methods=['POST'])
def addAmenity():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Amenity name is required'}), 400
    
    # Check if amenity with the same name already exists
    existing_amenity = next((amenity for amenity in dataManager.dataStore['Amenity'].values() if amenity.name == name), None)
    if existing_amenity:
        return jsonify({'error': 'Amenity with this name already exists'}), 409
    
    amenity = Amenity(name=name)
    dataManager.save(amenity)
    return jsonify(amenityToDict(amenity)), 201

# Retrieve all amenities
@amenityRoutes.route('/amenities', methods=['GET'])
def getAmenities():
    amenities = list(dataManager.dataStore['Amenity'].values())
    return jsonify([amenityToDict(amenity) for amenity in amenities]), 200

# Retrieve a specific amenity by ID
@amenityRoutes.route('/amenities/<uuid:amenity_id>', methods=['GET'])
def getAmenity(amenity_id):
    amenity = dataManager.get(str(amenity_id), 'Amenity')
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    return jsonify(amenityToDict(amenity)), 200

# Update an existing amenity
@amenityRoutes.route('/amenities/<uuid:amenity_id>', methods=['PUT'])
def updateAmenity(amenity_id):
    data = request.json

    amenity = dataManager.get(str(amenity_id), 'Amenity')
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Amenity name is required'}), 400
    
    # Check for duplicate name
    existing_amenity = next((a for a in dataManager.dataStore['Amenity'].values() if a.name == name and a.id != str(amenity_id)), None)
    if existing_amenity:
        return jsonify({'error': 'Amenity with this name already exists'}), 409
    
    amenity.name = name
    amenity.updated_at = datetime.utcnow()
    dataManager.update(amenity)
    return jsonify(amenityToDict(amenity)), 200

# Delete an amenity
@amenityRoutes.route('/amenities/<uuid:amenity_id>', methods=['DELETE'])
def deleteAmenity(amenity_id):
    amenity = dataManager.get(str(amenity_id), 'Amenity')
    if not amenity:
        return jsonify({'error': 'Amenity not found'}), 404
    
    dataManager.delete(str(amenity_id), 'Amenity')
    return '', 204
