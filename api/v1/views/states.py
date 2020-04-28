#!/usr/bin/python3

"""States module of view package"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route("/states")
@app_views.route("/states/<state_id>")
def get_states(state_id=None):
    """Get all states or specifc states"""

    if state_id:
        objs = storage.get("State", state_id)
        if objs:
            return jsonify(objs.to_dict())
        abort(404)
    objs = storage.all("State")
    list_objs = [obj.to_dict() for obj in objs.values()]
    return jsonify(list_objs)
