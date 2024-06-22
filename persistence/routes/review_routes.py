#!/usr/bin/python3

from flask import Blueprint, jsonify, request
from datetime import datetime
from models.review import Review
from persistence.data_manager import DataManager
from models.user import User
from models.place import Place

reviewRoutes = Blueprint('review_routes', __name__)
dataManager = DataManager()

def reviewToDict(review):
    return {
        'id': review.id,
        'place_id': review.place_id,
        'user_id': review.user_id,
        'rating': review.rating,
        'comment': review.comment,
        'created_at': review.created_at,
        'updated_at': review.updated_at
    }

# Create a new review for a specified place
@reviewRoutes.route('/places/<uuid:place_id>/reviews', methods=['POST'])
def addReview(place_id):
    data = request.json
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')

    # Validate required fields
    if not user_id or not rating or not comment:
        return jsonify({'error': 'user_id, rating, and comment are required'}), 400

    # Check if user exists
    user = dataManager.get(str(user_id), 'User')
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if place exists
    place = dataManager.get(str(place_id), 'Place')
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    # Check if user is the host of the place
    if user.id == place.host_id:
        return jsonify({'error': 'Hosts cannot review their own place'}), 400

    # Validate rating is within range
    if not (1 <= rating <= 5):
        return jsonify({'error': 'Rating must be between 1 and 5'}), 400

    # Check if user has already reviewed this place
    existing_review = next((r for r in dataManager.dataStore['Review'].values() if r.user_id == str(user_id) and r.place_id == str(place_id)), None)
    if existing_review:
        return jsonify({'error': 'User has already reviewed this place'}), 409

    review = Review(place_id=str(place_id), user_id=str(user_id), rating=rating, comment=comment)
    dataManager.save(review)
    return jsonify(reviewToDict(review)), 201

# Retrieve all reviews written by a specific user
@reviewRoutes.route('/users/<uuid:user_id>/reviews', methods=['GET'])
def getUserReviews(user_id):
    user_reviews = [reviewToDict(review) for review in dataManager.dataStore['Review'].values() if review.user_id == str(user_id)]
    return jsonify(user_reviews), 200

# Retrieve all reviews for a specific place
@reviewRoutes.route('/places/<uuid:place_id>/reviews', methods=['GET'])
def getPlaceReviews(place_id):
    place_reviews = [reviewToDict(review) for review in dataManager.dataStore['Review'].values() if review.place_id == str(place_id)]
    return jsonify(place_reviews), 200

# Retrieve detailed information about a specific review
@reviewRoutes.route('/reviews/<uuid:review_id>', methods=['GET'])
def getReview(review_id):
    review = dataManager.get(str(review_id), 'Review')
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    return jsonify(reviewToDict(review)), 200

# Update an existing review
@reviewRoutes.route('/reviews/<uuid:review_id>', methods=['PUT'])
def updateReview(review_id):
    data = request.json
    review = dataManager.get(str(review_id), 'Review')

    if not review:
        return jsonify({'error': 'Review not found'}), 404

    rating = data.get('rating')
    comment = data.get('comment')

    if rating:
        if not (1 <= rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        review.rating = rating
    
    if comment:
        review.comment = comment
    
    review.updated_at = datetime.utcnow()
    dataManager.update(review)
    return jsonify(reviewToDict(review)), 200

# Delete a specific review
@reviewRoutes.route('/reviews/<uuid:review_id>', methods=['DELETE'])
def deleteReview(review_id):
    review = dataManager.get(str(review_id), 'Review')
    if not review:
        return jsonify({'error': 'Review not found'}), 404
    dataManager.delete(str(review_id), 'Review')
    return '', 204

