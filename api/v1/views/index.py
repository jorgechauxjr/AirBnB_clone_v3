#!/usr/bin/python3

"""Index file of views package"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """Get status from /status"""

    return jsonify(status="OK")
