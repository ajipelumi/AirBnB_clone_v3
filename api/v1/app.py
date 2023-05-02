#!/usr/bin/python3
""" API design for AirBnB. """
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


# Create a Flask instance
app = Flask(__name__)

# Create cors instance
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Register Blueprint app_views
app.register_blueprint(app_views)


# Handle teardown method
@app.teardown_appcontext
def teardown_method(exception):
    """ Tears down any resource open after request cycle. """
    storage.close()


# Handle error 404
@app.errorhandler(404)
def not_found_method(error):
    """ Returns JSON-formatted 404 status code response. """
    return make_response({"error": "Not found"}, 404)


# Start flask server with declared host and port
if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True)
