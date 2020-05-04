#!/usr/bin/python3

"""Users module of view package"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from flasgger.utils import swag_from


@app_views.route("/users", methods=["GET", "POST"])
@swag_from('flasgger/users/users_get.yml', methods=['GET'])
@swag_from('flasgger/users/users_post.yml', methods=['POST'])
def get_users():
    """Get all users"""

    if request.method == "GET":
        objs = storage.all("User")
        all_users = [obj.to_dict() for obj in objs.values()]
        return jsonify(all_users)

    if request.method == "POST":
        if request.is_json is False:
            abort(400, "Not a JSON")
        user_dict = request.get_json()
        if "email" not in user_dict:
            abort(400, "Missing email")
        if "password" not in user_dict:
            abort(400, "Missing password")
        new_user = User(**user_dict)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["GET", "DELETE", "PUT"])
@swag_from('flasgger/users/users_user_id_get.yml', methods=['GET'])
@swag_from('flasgger/users/users_user_id_delete.yml', methods=['DELETE'])
@swag_from('flasgger/users/users_user_id_put.yml', methods=['PUT'])
def handle_user(user_id=None):
    """Get, Delete or Update a user by id"""

    obj_user = storage.get("User", user_id)

    if obj_user is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_user.to_dict())

    if request.method == "DELETE":
        obj_user.delete()
        storage.save()
        return jsonify({})

    if request.method == "PUT":
        if request.is_json is False:
            abort(400, "Not a JSON")
        user_dict = request.get_json()
        obj_user.update(user_dict)
        return jsonify(obj_user.to_dict())
