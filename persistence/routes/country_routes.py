#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.country import Country
from persistence.data_manager import DataManager
from datetime import datetime

countryRoutes = Blueprint('country_routes', __name__)
dataManager = DataManager()

# Give results to variable from countr.py file loadCountries function
countries = Country.loadCountries()

def countryToDict(country):
    return {
        'code': country.code,
        'name': country.name
    }

@countryRoutes.route('/countries', methods=['GET'])
def getCountries():
    return jsonify([countryToDict(country) for country in countries.values()]), 200

