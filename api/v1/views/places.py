#!/usr/bin/python3

"""Places module of view package"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place


@app_views.route("/places", methods=["GET"])
def get_places():
    """Get all places"""

    objs = storage.all("Place")
    all_places = [obj.to_dict() for obj in objs.values()]
    return jsonify(all_places)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id=None):
    """Cretes a place given a city id"""

    obj_city = storage.get("City", city_id)

    if obj_city is None:
        abort(404)

    if request.is_json is False:
        abort(400, "Not a JSON")
    place_dict = request.get_json()
    if "user_id" not in place_dict:
        abort(400, "Missing user_id")
    obj_user = storage.get("User", place_dict.get('user_id'))
    if obj_user is None:
        abort(404)
    if "name" not in place_dict:
        abort(400, "Missing name")
    place_dict.update(city_id=city_id)
    new_place = Place(**place_dict)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["GET", "DELETE", "PUT"])
def handle_place(place_id=None):
    """Get, Delete or Update a place by id"""

    obj_place = storage.get("Place", place_id)

    if obj_place is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_place.to_dict())

    if request.method == "DELETE":
        obj_place.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        if request.is_json is False:
            abort(400, "Not a JSON")
        place_dict = request.get_json()
        obj_place.update(place_dict)
        return jsonify(obj_place.to_dict())
