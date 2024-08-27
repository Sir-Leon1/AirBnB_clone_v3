#!/usr/bin/python3
"""
Flask route that returns json status responses
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_no_id(state_id):
    """
        Route to handle retreival of all city objects of a state
    """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        cities_list = [city.to_dict() for city in state_obj.cities]
        return jsonify(cities_list)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        city = CNC.get('City')
        new_city = city(**req_json)
        new_city.state_id = state_id
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def cities_id(city_id):
    """
        Route to handle retrieval of a city by its id
    """
    if request.method == 'GET':
        city_obj = storage.get('City', city_id)
        if city_obj is None:
            abort(404, 'Not found')
        return jsonify(city_obj.to_dict())

    if request.method == 'DELETE':
        city_obj = storage.get('City', city_id)
        if city_obj is None:
            abort(404, "Not found")
        city_obj.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        city_obj = storage.get('City', city_id)
        if city_obj is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'NOT a JSON')
        for key, value in req_json.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city_obj, key, value)
        city_obj.save()
        return jsonify(city_obj.to_dict()), 200
