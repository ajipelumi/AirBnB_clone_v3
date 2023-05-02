#!/usr/bin/python3
""" Reviews module that handles all RESTFul API actions. """
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves the list of all Review objects. """
    reviews = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review_object(review_id):
    """ Retrieves a Review object. """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ Creates a Review object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    if 'user_id' not in json_data.keys():
        abort(400, 'Missing user_id')
    if 'text' not in json_data.keys():
        abort(400, 'Missing text')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    user = storage.get(User, json_data['user_id'])
    if not user:
        abort(404)
    new_review = Review(**json_data)
    setattr(new_review, 'place_id', place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Updates a review object. """
    json_data = request.get_json()
    if not json_data:
        abort(400, 'Not a JSON')
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    for key, value in json_data.items():
        if key not in ['id', 'user_id',
                       'place_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Deletes an review object. """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200
