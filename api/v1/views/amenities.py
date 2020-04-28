#!/usr/bin/python3
"""States view module.."""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'])
def all_amenities():
    """Retrieves the list of all amenities objects """
    amenities_list = []
    amenities_objs = storage.all('Amenity').values()
    for element in amenities_objs:
        amenities_list.append(element.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenities_list_id(amenities_id):
    """Retrieves an Amenity object by Id"""
    amenities_objs = storage.all('Amenity').values()
    for element in amenities_objs:
        if element.id == amenities_id:
            return jsonify(element.to_dict())
    abort(404)
