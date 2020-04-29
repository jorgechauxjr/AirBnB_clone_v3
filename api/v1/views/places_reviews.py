#!/usr/bin/python3

"""Places_Review module of view package"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.review import Review


@app_views.route("places/<place_id>/reviews", methods=["GET", "POST"])
def create_or_get_review(place_id=None):
    """Creates or get a review given a place id"""

    obj_place = storage.get("Place", place_id)

    if obj_place is None:
        abort(404)

    if request.method == "GET":
        objs = storage.all("Review")
        review_by_place = []
        for obj in objs.values():
            obj_dict = obj.to_dict()
            if obj_dict.get('place_id') == place_id:
                review_by_place.append(obj_dict)
        return jsonify(review_by_place)

    if request.method == "POST":
        if request.is_json is False:
            abort(400, "Not a JSON")
        review_dict = request.get_json()
        if "user_id" not in review_dict:
            abort(400, "Missing user_id")
        obj_user = storage.get("User", review_dict.get('user_id'))
        if obj_user is None:
            abort(404)
        if "text" not in review_dict:
            abort(400, "Missing text")
        review_dict.update(place_id=place_id)
        new_review = Review(**review_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def handle_review(review_id=None):
    """Get, Delete or Update a review by id"""

    obj_review = storage.get("Review", review_id)

    if obj_review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_review.to_dict())

    if request.method == "DELETE":
        obj_review.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        if request.is_json is False:
            abort(400, "Not a JSON")
        review_dict = request.get_json()
        obj_review.update(review_dict)
        return jsonify(obj_review.to_dict())
