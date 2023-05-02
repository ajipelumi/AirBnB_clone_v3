#!/usr/bin/python3
""" States module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects. """
    states = []
    all_objs = storage.all(State)
    for obj in all_objs.values():
        states.append(obj.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_object(state_id):
    """ Retrieves a State object. """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a state. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'name' not in json_data.keys():
        abort(400, 'Missing name')
    new_state = State(**json_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a state object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200



@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ Delete a state object. """
    obj = storage.get(State, state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
