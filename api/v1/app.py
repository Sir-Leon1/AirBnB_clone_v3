#!/usr/bin/python3
"""
Starts a web flask application
"""
from os import getenv
from flask import Flask
from models import storage
from api.v1.views.index import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Error handler for 404 error"""
    return {"error": "Not found"}, 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', 5000)),
            threaded=True, debug=True)
