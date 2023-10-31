#!/usr/bin/python3
"""Review API views"""

from api.v1.views import (app_views,
                          Review, storage, User, Place)
from flask import abort, jsonify, request


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Create a new Review"""
    data = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    user_id = data.get('user_id')
    text = data.get('text')
    if user_id is None:
        abort(400, description="Missing user_id")
    if text is None:
        abort(400, description="Missing text")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    review = Review(user_id=user_id, place_id=place_id, text=text)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Get all reviews for a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Get a specific review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Update a review"""
    data = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})
