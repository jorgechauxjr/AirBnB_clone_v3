#!/usr/bin/python3

"""Flask server module"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False

# app_views variable created in api.v1.views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exc):
    """Teardown db"""
    storage.close()


@app.errorhandler(404)
def invalid_route(e):
    """Handle 404 error with json response 404"""
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    import os
    app.config['ENV'] = 'development'
    host = os.getenv("HBNB_API_HOST", '0.0.0.0')
    port = os.getenv("HBNB_API_PORT", '5000')
    app.run(host=host, port=port, threaded=True)
