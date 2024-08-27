#!/usr/bin/python3
"""
    Flask route that returns json status responses
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_by_city(city_id):
    """
        Route to handle returning places by specific city
    """
    if request.method == 'GET':
        city_obj = storage.get('City', city_id)
        if city_obj is None:
            abort(404, 'Not found')
        places_list = [place.to_dict() for place in city_obj.place]
        return jsonify(places_list)

    if request.method == 'POST':
        city_obj = storage.get('City', city_id)
        req_json = request.get_json()
        if city_obj is None:
            abort(404, 'Not found')
        if req_json is None:
            abort(400, 'Not a JSON')
        if 'user_id' not in req_json:
            abort(400, 'Missing user_id')
        if 'name' not in req_json:
            abort(400, 'Missing name')
        user_obj = storage.get('User', req_json['user_id'])
        if user_obj is None:
            abort(404, 'Not found')
        new_place = CNC['Place'](**request.json)
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE'])
def places_by_id(place_id):
    """
        Route to handle returning places by specific id
    """
    if request.method == 'GET':
        place_obj = storage.get('Place', place_id)
        if place_obj is None:
            abort(404, 'Not found')
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        place_obj = storage.get('Place', place_id)
        if place_obj is None:
            abort(404, 'Not found')
        storage.delete(place_obj)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        place_obj = storage.get('Place', place_id)
        if place_obj is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        for key, value in req_json.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place_obj, key, value)
        place_obj.save()
        return jsonify(place_obj.to_dict()), 200
