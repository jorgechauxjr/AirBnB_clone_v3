#!/usr/bin/python3
"""amenities view module.."""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'])
@swag_from('flasgger/amenities/amenities_get.yml', methods=['GET'])
def all_amenities():
    """Retrieves the list of all amenities objects """
    amenities_list = []
    amenities_objs = storage.all('Amenity').values()
    for element in amenities_objs:
        amenities_list.append(element.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
@swag_from('flasgger/amenities/amenity_id_delete.yml', methods=['DELETE'])
def amenities_remove(amenity_id):
    """Remove an amenity by Id"""
    amenity_to_delete = storage.get('Amenity', amenity_id)
    if amenity_to_delete is None:
        abort(404)
    amenity_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
@swag_from('flasgger/amenities/amenity_id_put.yml', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_dict = request.get_json()
    if amenity_dict is None:
        abort(400, "Not a JSON")
    amenity_obj.update(amenity_dict)
    return jsonify(amenity_obj.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["GET"])
@swag_from('flasgger/amenities/amenity_id_get.yml', methods=['GET'])
def amenities_by_id(amenity_id=None):
    """Get a amenity by id"""

    obj_amenity = storage.get("Amenity", amenity_id)

    if obj_amenity is None:
        abort(404)

    if request.method == "GET":
        return jsonify(obj_amenity.to_dict())


@app_views.route("/amenities", methods=["POST"])
@swag_from('flasgger/amenities/amenities_post.yml', methods=['POST'])
def create_amenity():
    """Create amenity"""
    if request.is_json is False:
        abort(400, "Not a JSON")
    amenity_dict = request.get_json()
    if "name" not in amenity_dict:
        abort(400, "Missing name")
    new_amenity = Amenity(**amenity_dict)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201
