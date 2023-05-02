#!/usr/bin/python3
""" Amenities module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects. """
    amenities = []
    all_objs = storage.all(Amenity)
    for obj in all_objs.values():
        amenities.append(obj.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_object(amenity_id):
    """ Retrieves an Amenity object. """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'name' not in json_data.keys():
        abort(400, 'Missing name')
    new_amenity = Amenity(**json_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an amenity object. """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
