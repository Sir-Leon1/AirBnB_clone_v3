#!/usr/bin/python3
"""
    Flask route that returns json status responses
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities_no_id():
    """
        Route to handle returning all amenity objects
    """
    if request.method == 'GET':
        amenities_list = [amenity.to_dict() for amenity in storage.all('Amenity').values()]
        return jsonify(amenities_list)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        amenity = CNC.get('Amenity')
        new_amenity = amenity(**req_json)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_id(amenity_id):
    """
        Route to handle returning a specific amenity object
    """
    if request.method == 'GET':
        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404, 'Not found')
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404, 'Not found')
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        amenity = storage.get('Amenity', amenity_id)
        if amenity is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'NOT a JSON')
        for key, value in req_json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
