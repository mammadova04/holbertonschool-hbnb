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

# Delete user with ID
@userRoutes.route('/users/<uuid:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    # Convert uuid to string
    user = dataManager.get(str(user_id), 'User')
    if not user:
        return jsonify({"ERROR": "USER NOT FOUND"})
    dataManager.delete(str(user_id), 'User')
    return '', 204

# Update user with ID
@userRoutes.route('/users/<uuid:user_id>', methods=['PUT'])
def updateUser(user_id):
    data = request.json
    # Convert UUID to string
    user = dataManager.get(str(user_id), 'User')
    if not user:
        return jsonify({'ERROR': 'USER NOT FOUND'}), 404
    
    # If email is not string and there is no @ sign in email
    if not isinstance(data.get('email'), str) or '@' not in data['email']:
        return jsonify({'ERROR': 'INVALID EMAIL FORMAT'}), 400

    # If email already exists
    if data['email'] != user.email and any(u.email == data['email'] for u in dataManager.dataStore['User'].values()):
        return jsonify({'ERROR': 'EMAIL EXISTS'}), 409

    # Check for required fields
    if not data.get('first_name') or not data.get('last_name'):
        return jsonify({'ERROR': 'FIRST NAME AND LASTNAME REQUIRED'}), 400
    
    # Update user object and save
    user.email = data['email']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.password = data.get('password', user.password)  # Update password if provided
    user.updated_at = datetime.now()
    dataManager.update(user)
    return jsonify(userToDict(user)), 200
