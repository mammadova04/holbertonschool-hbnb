#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.city import City
from models.country import Country
from persistence.data_manager import DataManager
from datetime import datetime

cityRoutes = Blueprint('city_routes', __name__)
dataManager = DataManager()

countries = Country.loadCountries()
def cityToDict(city):
    return {
        'id': city.id,
        'name': city.name,
        'country_code': city.country_code,
        'created_at': city.created_at,
        'updated_at': city.updated_at
    }

# Get all cities
@cityRoutes.route('/cities', methods=['GET'])
def getCities():
    cities = list(dataManager.dataStore["City"].values())
    return jsonify([cityToDict(city) for city in cities]), 200

# Add City
@cityRoutes.route('/cities', methods=['POST'])
def addCity():
    data = request.json
    country_code = data.get('country_code')
    
    # Get Country Code
    country = countries.get(country_code)
    
    # If there is no Country Code like that
    if not country:
        return jsonify({"ERROR": "INVALID COUNTRY CODE"}), 400
    
    # Ig city already exists
    if any(city.name == data['name'] and city.country_code == country_code for city in dataManager.dataStore['City'].values()):
        return jsonify({"ERROR": "CITY EXISTS IN THIS COUNTRY"}), 409

    city = City(name=data['name'], country=country, country_code=country_code)
    dataManager.save(city)
    return jsonify(cityToDict(city)), 201

# Get City With Specific ID
@cityRoutes.route('/cities/<uuid:city_id>', methods=['GET'])
def getCity(city_id):
    # Convert uuid into string
    city = dataManager.get(str(city_id), 'City')

    # If there is no City
    if not city:
        return jsonify({'ERROR': 'CITY NOT FOUND'}), 404
    return jsonify(cityToDict(city)), 200

# Delete City with Specific ID
@cityRoutes.route('/cities/<uuid:city_id>', methods=['DELETE'])
def deleteCity(city_id):
    
    # Convert uuid into string
    city = dataManager.get(str(city_id), 'City')
    
    # If there is no City like That
    if not city:
        return jsonify({"ERROR": "CITY NOT FOUND"}), 404
    dataManager.delete(str(city_id), 'City')
    return '', 204

# Update City with ID
@cityRoutes.route('/cities/<uuid:city_id>', methods=['PUT'])
def updateCity(city_id):
    data = request.json

    # Convert uuid into string
    city = dataManager.get(str(city_id), 'City')
    
    # If there is no City like That
    if not city:
        return jsonify({'ERROR': 'CITY NOT FOUND'}), 404

    country_code = data.get('country_code')

    # If there is no Country Code
    if country_code not in countries:
        return jsonify({'ERROR': 'INVALID COUNTRY CODE'}), 400

    # City already Exists
    if any(c.id != city.id and c.name == data['name'] and c.country_code == country_code for c in dataManager.dataStore['City'].values()):
        return jsonify({'ERROR': 'CITY EXISTS IN THIS COUNTRY'}), 409

    city.name = data['name']
    city.country_code = country_code
    city.updated_at = datetime.utcnow()
    dataManager.update(city)
    return jsonify(cityToDict(city)), 200

# Retrieve all cities belonging to a specific country
@cityRoutes.route('/countries/<string:country_code>/cities', methods=['GET'])
def getCitiesByCountry(country_code):
    if country_code not in countries:
        return jsonify({'ERROR': 'COUNTRY NOT FOUND'}), 404

    cities = [cityToDict(city) for city in dataManager.dataStore['City'].values() if city.country_code == country_code]
    return jsonify(cities), 200
