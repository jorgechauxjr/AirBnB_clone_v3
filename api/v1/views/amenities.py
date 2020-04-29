#!/usr/bin/python3
"""amenities view module.."""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Retrieves the list of all amenities objects """
    amenities_list = []
    amenities_objs = storage.all('Amenity').values()
    for element in amenities_objs:
        amenities_list.append(element.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenities_remove(amenity_id):
    """Remove an amenity by Id"""
    amenity_to_delete = storage.get('Amenity', amenity_id)
    if amenity_to_delete is None:
        abort(404)
    amenity_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity object
    """
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404)
    amenity_dict = request.get_json()
    if amenity_dict is None:
        abort(400, "Not a JSON")
    amenity_obj.update(amenity_dict)
    return jsonify(amenity_obj.to_dict())
