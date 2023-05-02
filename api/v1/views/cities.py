#!/usr/bin/python3
""" Cities module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects. """
    cities = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_object(city_id):
    """ Retrieves a City object. """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a city. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in json_data.keys():
        abort(400, 'Missing name')
    new_city = City(**json_data)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a city object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    for key, value in json_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a city object. """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
