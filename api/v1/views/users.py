#!/usr/bin/python3
""" Users module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Retrieves the list of all User objects. """
    users = []
    all_objs = storage.all(User)
    for obj in all_objs.values():
        users.append(obj.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_object(user_id):
    """ Retrieves a User object. """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'email' not in json_data.keys():
        abort(400, 'Missing email')
    if 'password' not in json_data.keys():
        abort(400, 'Missing password')
    new_user = User(**json_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a user object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    for key, value in json_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ Deletes an user object. """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
