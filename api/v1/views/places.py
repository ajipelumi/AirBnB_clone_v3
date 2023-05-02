#!/usr/bin/python3
""" Places module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects. """
    places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place_object(place_id):
    """ Retrieves a Place object. """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a Place object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data.keys():
        abort(400, 'Missing user_id')
    if 'name' not in json_data.keys():
        abort(400, 'Missing name')
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    user = storage.get(User, json_data['user_id'])
    if not user:
        abort(404)
    new_place = Place(**json_data)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a place object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    for key, value in json_data.items():
        if key not in ['id', 'user_id',
                       'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Deletes an place object. """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
