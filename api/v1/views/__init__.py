#!/usr/bin/python3
""" Blueprint design module for views. """
from flask import Blueprint


# Create a Blueprint instance for app_views
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


# Import all views from all modules
from api.v1.views.index import *
from api.v1.views.states import *
