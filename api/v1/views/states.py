#!/usr/bin/python3

"""States module of view package"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def get_states():
    """Get all states"""

    if request.method == "GET":
        objs = storage.all("State")
        all_states = [obj.to_dict() for obj in objs.values()]
        return jsonify(all_states)

    if request.method == "POST":
        if request.is_json is False:
            abort(400, "Not a JSON")
        state_dict = request.get_json()
        if "name" not in state_dict:
            abort(400, "Missing name")
        new_state = State(**state_dict)
        new_state.save()
        return jsonify(new_state.to_dict())


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def handle_state(state_id=None):
    """Get, Delete or Update a state by id"""

    obj_state = storage.get("State", state_id)

    if obj_state is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_state.to_dict())

    if request.method == "DELETE":
        obj_state.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        if request.is_json is False:
            abort(400, "Not a JSON")
        state_dict = request.get_json()
        obj_state.update(state_dict)
        return jsonify(obj_state.to_dict())
