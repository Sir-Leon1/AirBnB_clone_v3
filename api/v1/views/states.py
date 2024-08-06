#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""
from flask import jsonify, request
from models import storage
from models.state import State
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def get_states():
    """Retrieves the list of all state objects
    or creates a new state based on the given data"""
    if request.method == 'GET':
        states = storage.all('State')
        states_list = [state.to_dict() for state in states.values()]
        return jsonify(states_list)
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        if 'name' not in data:
            return "Missing name", 400
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def get_state_id(state_id):
    """Retrieves a state object based on the given ID
    or deletes a state object based on the ID
    """
    state = storage.get(State, state_id)
    if state is None:
        return 404

    if request.method == 'GET':
        return jsonify(BaseModel.to_dict(state))
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return "Not a JSON", 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200

