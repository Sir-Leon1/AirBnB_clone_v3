#!/usr/bin/python3
"""
    Flask route that returns json status responses
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC


@app_views.route('/users', methods=['GET', 'POST'])
def users_no_id():
    """
        Route to handle returning all user objects
    """
    if request.method == 'GET':
        users_list = [user.to_dict() for user in storage.all('User').values()]
        return jsonify(users_list)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'NOT a JSON')
        if req_json.get('email') is None:
            abort(400, 'Missing email')
        if req_json.get('password') is None:
            abort(400, 'Missing password')
        user = CNC.get('User')
        new_user = user(**req_json)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def users_with_id(user_id):
    """
        Route to handle requests with user id
    """
    if request.method == 'GET':
        user = storage.get('User', user_id)
        if user is None:
            abort(404, 'Not found')
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user = storage.get('User', user_id)
        if user is None:
            abort(404, 'Not found')
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        user = storage.get('User', user_id)
        if user is None:
            abort(404, 'Not found')
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'NOT a JSON')
        for key, value in req_json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200

