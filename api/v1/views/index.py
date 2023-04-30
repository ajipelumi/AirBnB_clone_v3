#!/usr/bin/python3
""" Index python file. """
from api.v1.views import app_views


@app_views.route("/status")
def status_method():
    """ Returns the status of our API. """
    json_status = {'status': 'OK'}
    return json_status
