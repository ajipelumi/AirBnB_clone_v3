#!/usr/bin/python3
""" Index python file. """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review,
           "states": State, "users": User}


@app_views.route("/status")
def status_method():
    """ Returns the status of our API. """
    json_status = {'status': 'OK'}
    return json_status


@app_views.route("/stats")
def stats_method():
    """ Retrieves the number of each objects by type. """
    json_stats = {}
    for key, value in classes.items():
        count = storage.count(value)
        json_stats[key] = count
    return json_stats
