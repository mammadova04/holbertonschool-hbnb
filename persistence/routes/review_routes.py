#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from datetime import datetime
from models.review import Review
from persistence.data_manager import DataManager

reviewRoutes = Blueprint('review_routes', __name__)
dataManager = DataManager()

def reviewToDict(review):
    return {
        'id': review.id,
        'user_id': review.user_id,
        'place_id': review.place_id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    }

# Create a new review for a place
@reviewRoutes.route('/places/<place_id>/reviews', methods=['POST'])
def addReview(place_id):
    try:
        data = request.json
        required_fields = ['user_id', 'rating', 'comment']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Additional validation checks
        # Check if user_id exists
        user_id = data['user_id']
        if not dataManager.get(user_id, 'User'):
            return jsonify({'error': f'User with id {user_id} not found'}), 404
        
        # Check if place_id exists
        place = dataManager.get(place_id, 'Place')
        if not place:
            return jsonify({'error': f'Place with id {place_id} not found'}), 404
        
        # Create review object
        review = Review(user_id=user_id, place_id=place_id, **data)
        review.validate_rating()  # Validate rating
        
        # Save review
        dataManager.save(review)
        
        return jsonify(reviewToDict(review)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Retrieve all reviews for a specific place
@reviewRoutes.route('/places/<place_id>/reviews', methods=['GET'])
def getPlaceReviews(place_id):
    try:
        reviews = dataManager.get_place_reviews(place_id)  # Implement method to get place reviews
        return jsonify([reviewToDict(review) for review in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Retrieve all reviews written by a specific user
@reviewRoutes.route('/users/<user_id>/reviews', methods=['GET'])
def getUserReviews(user_id):
    try:
        reviews = dataManager.get_user_reviews(user_id)  # Implement method to get user reviews
        return jsonify([reviewToDict(review) for review in reviews]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Retrieve a specific review by ID
@reviewRoutes.route('/reviews/<review_id>', methods=['GET'])
def getReview(review_id):
    try:
        review = dataManager.get(review_id, 'Review')
        if not review:
            return jsonify({'error': f'Review with id {review_id} not found'}), 404
        return jsonify(reviewToDict(review)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Update an existing review
@reviewRoutes.route('/reviews/<review_id>', methods=['PUT'])
def updateReview(review_id):
    try:
        data = request.json
        review = dataManager.get(review_id, 'Review')
        if not review:
            return jsonify({'error': f'Review with id {review_id} not found'}), 404
        
        # Update review fields
        for key, value in data.items():
            setattr(review, key, value)
        
        review.updated_at = datetime.utcnow()
        dataManager.update(review)
        
        return jsonify(reviewToDict(review)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Delete a review
@reviewRoutes.route('/reviews/<review_id>', methods=['DELETE'])
def deleteReview(review_id):
    try:
        review = dataManager.get(review_id, 'Review')
        if not review:
            return jsonify({'error': f'Review with id {review_id} not found'}), 404
        
        dataManager.delete(review_id, 'Review')
        
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
