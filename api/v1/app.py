#!/usr/bin/python3
""" API design for AirBnB. """
from flask import Flask
from models import storage
from api.v1.views import app_views
import os


# Create a Flask instance
app = Flask(__name__)


# Register Blueprint app_views
app.register_blueprint(app_views)


# Handle teardown method
@app.teardown_appcontext
def teardown_method(exception):
    """ Tears down any resource open after request cycle. """
    storage.close()


# Start flask server with declared host and port
if __name__ == "__main__":
    # Get host and port from environment variables
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    # Run the Flask app
    app.run(host=host, port=port, threaded=True)
