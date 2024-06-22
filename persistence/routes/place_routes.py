#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.place import Place
from models.city import City
from models.amenity import Amenity
from persistence.data_manager import DataManager
from datetime import datetime

placeRoutes = Blueprint('place_routes', __name__)
dataManager = DataManager()

def placeToDict(place):
    return {
        'id': place.id,
        'name': place.name,
        'description': place.description,
        'address': place.address,
        'city': cityToDict(place.city),
        'latitude': place.latitude,
        'longitude': place.longitude,
        'host_id': place.host.id if place.host else None,
        'number_of_rooms': place.number_of_rooms,
        'number_of_bathrooms': place.number_of_bathrooms,
        'price_per_night': place.price_per_night,
        'max_guests': place.max_guests,
        'amenities': [amenity.id for amenity in place.amenities],
        'created_at': place.created_at,
        'updated_at': place.updated_at
    }

def cityToDict(city):
    return {
        'id': city.id,
        'name': city.name,
        'country_code': city.country_code,
        'created_at': city.created_at,
        'updated_at': city.updated_at
    }

# Retrieve all places
@placeRoutes.route('/places', methods=['GET'])
def getPlaces():
    places = list(dataManager.dataStore["Place"].values())
    return jsonify([placeToDict(place) for place in places]), 200

# Create a new place
@placeRoutes.route('/places', methods=['POST'])
def addPlace():
    data = request.json

    # Validate required fields
    required_fields = ['name', 'description', 'city_id', 'latitude', 'longitude', 'number_of_rooms', 'number_of_bathrooms', 'price_per_night', 'max_guests', 'amenity_ids']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Validate city_id
    city_id = data.get('city_id')
    city = dataManager.get(city_id, 'City')
    if not city:
        return jsonify({'error': 'City not found'}), 404

    # Validate amenity_ids
    amenity_ids = data.get('amenity_ids', [])
    for amenity_id in amenity_ids:
        if not dataManager.get(amenity_id, 'Amenity'):
            return jsonify({'error': f'Amenity not found: {amenity_id}'}), 404

    # Create new place
    place = Place(
        name=data['name'],
        description=data['description'],
        city=city,
        address=data.get('address', ''),
        latitude=data['latitude'],
        longitude=data['longitude'],
        host=None,  # Assuming host assignment might be handled separately
        number_of_rooms=data['number_of_rooms'],
        number_of_bathrooms=data['number_of_bathrooms'],
        price_per_night=data['price_per_night'],
        max_guests=data['max_guests'],
        amenities=[dataManager.get(amenity_id, 'Amenity') for amenity_id in amenity_ids]
    )
    dataManager.save(place)
    return jsonify(placeToDict(place)), 201

# Retrieve a specific place by ID
@placeRoutes.route('/places/<uuid:place_id>', methods=['GET'])
def getPlace(place_id):
    place = dataManager.get(str(place_id), 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404
    return jsonify(placeToDict(place)), 200

# Update an existing place by ID
@placeRoutes.route('/places/<uuid:place_id>', methods=['PUT'])
def updatePlace(place_id):
    data = request.json

    place = dataManager.get(str(place_id), 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    # Validate city_id
    city_id = data.get('city_id')
    city = dataManager.get(city_id, 'City')
    if not city:
        return jsonify({'error': 'City not found'}), 404

    # Validate amenity_ids
    amenity_ids = data.get('amenity_ids', [])
    for amenity_id in amenity_ids:
        if not dataManager.get(amenity_id, 'Amenity'):
            return jsonify({'error': f'Amenity not found: {amenity_id}'}), 404

    # Update place fields
    place.name = data['name']
    place.description = data['description']
    place.city = city
    place.address = data.get('address', '')
    place.latitude = data['latitude']
    place.longitude = data['longitude']
    place.number_of_rooms = data['number_of_rooms']
    place.number_of_bathrooms = data['number_of_bathrooms']
    place.price_per_night = data['price_per_night']
    place.max_guests = data['max_guests']
    place.amenities = [dataManager.get(amenity_id, 'Amenity') for amenity_id in amenity_ids]
    place.updated_at = datetime.utcnow()

    dataManager.update(place)
    return jsonify(placeToDict(place)), 200

# Delete a specific place by ID
@placeRoutes.route('/places/<uuid:place_id>', methods=['DELETE'])
def deletePlace(place_id):
    place = dataManager.get(str(place_id), 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    dataManager.delete(str(place_id), 'Place')
    return '', 204
