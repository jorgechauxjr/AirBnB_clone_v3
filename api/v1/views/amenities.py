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

