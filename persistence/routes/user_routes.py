#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from models.user import User
from persistence.data_manager import DataManager
from datetime import datetime

userRoutes = Blueprint('user_routes', __name__)
dataManager = DataManager()

def userToDict(user):
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'created_at': user.created_at,
        'updated_at': user.updated_at
    }

# Beginning Part of API. If no Endpoint Entered
@userRoutes.route('/')
def greeting():
    return 'Flask App'

# Show all Users
@userRoutes.route('/users', methods=['GET'])
def getUsers():
    users = list(dataManager.dataStore["User"].values())
    return jsonify([userToDict(user) for user in users]), 200

# Add new User
@userRoutes.route('/users', methods=['POST'])
def addUser():
    data = request.json

    # Email Check
    # If email is not string and there is no @ sign in email
    if not isinstance(data.get('email'), str) or '@' not in data['email']:
        return jsonify({"ERROR": "INVALID EMAIL FORMAT"}), 400
    
    # If email exists
    if any(user.email == data['email'] for user in dataManager.dataStore['User'].values()):
        return jsonify({"ERROR": "EMAIL EXISTS"}), 409
    
    # Missing Fields
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({'ERROR': 'MISSING FIELDS'}), 400

    # Create new user
    user = User(email=data['email'], password=data['password'], first_name=data['first_name'], last_name=data['last_name'])
    dataManager.save(user)
    return jsonify(userToDict(user)), 201

# Get Specific User with ID
@userRoutes.route('/users/<uuid:user_id>', methods=['GET'])
def getUser(user_id):
    # Convert uuid to string    
    user = dataManager.get(str(user_id), 'User')
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    return jsonify(userToDict(user)), 200
