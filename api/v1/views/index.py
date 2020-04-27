#!/usr/bin/python3

"""Index file of views package"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status")
def get_status():
    """Get status from /status"""

    return jsonify(status="OK")


@app_views.route("/stats")
def get_stats():
    """Get count of all objects in json"""

    clss = {"Amenity": "amenities", "City": "cities",
            "Place": "places", "Review": "reviews",
            "State": "states", "User": "users"}
    count_dict = {}
    for key, value in clss.items():
        count_number = storage.count(key)
        count_dict.update({value: count_number})
    return jsonify(count_dict)
