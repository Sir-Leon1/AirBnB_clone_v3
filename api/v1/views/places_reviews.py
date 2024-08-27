#!/usr/bin/python3
"""
    Flask route that returns json status responses
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_by_place(place_id):
    """
        Route to handle returning reviews by specific place
    """
    if request.method == 'GET':
        place_obj = storage.get('Place', place_id)
        if place_obj is None:
            abort(404, 'Not found')
        reviews_list = [review.to_dict() for review in place_obj.review]
        return jsonify(reviews_list)

    if request.method == 'POST':
        place_obj = storage.get('Place', place_id)
        req_json = request.get_json()
        if place_obj is None:
            abort(404, 'Not found')
        if req_json is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in req_json:
            abort(400, 'Missing user_id')
        if 'text' not in req_json:
            abort(400, 'Missing text')
        user_obj = storage.get('User', req_json['user_id'])
        if user_obj is None:
            abort(404, 'Not found')
        new_review = CNC['Review'](**request.json)
        new_review.place_id = place_id
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def reviews_by_id(review_id):
    """
        Route to handle returning reviews by specific id
    """
    if request.method == 'GET':
        review_obj = storage.get('Review', review_id)
        if review_obj is None:
            abort(404, 'Not found')
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj = storage.get('Review', review_id)
        if review_obj is None:
            abort(404, 'Not found')
        storage.delete(review_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        review_obj = storage.get('Review', review_id)
        if review_obj is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        for key, value in req_json.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review_obj, key, value)
        review_obj.save()
        return jsonify(review_obj.to_dict()), 200