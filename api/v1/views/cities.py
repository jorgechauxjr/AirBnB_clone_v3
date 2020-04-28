#!/usr/bin/python3
"""States view module.."""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def all_cities():
    """Retrieves the list of all cities objects """
    cities_list = []
    cities_objs = storage.all('City').values()
    for element in cities_objs:
        cities_list.append(element.to_dict())
    return jsonify(cities_list)


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_list(state_id):
    """Retrieves the list of all cities objects of a State"""
    cities_list = []
    cities_objs = storage.get('State', state_id)
    if cities_objs is None:
        abort(404)
    for city in cities_objs.cities:
        cities_list.append(city.to_dict())

    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_list_id(city_id):
    """Retrieves a City object by Id"""
    cities_objs = storage.all('City').values()
    for element in cities_objs:
        if element.id == city_id:
            return jsonify(element.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def cities_remove(city_id):
    """Remove a city by Id"""
    city_to_delete = storage.get('City', city_id)
    if city_to_delete is None:
        abort(404)
    city_to_delete.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Creates a new city
    """
    if request.is_json is False:
        abort(400, "Not a JSON")
    city_dict = request.get_json()
    if 'name' not in city_dict:
        abort(400, 'Missing name')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    city_dict.update(state_id=state_id)
    new_city = City(**city_dict)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a City object
    """
    city_obj = storage.get('City', city_id)
    if city_obj is None:
        abort(404)
    city_dict = request.get_json()
    if city_dict is None:
        abort(400, "Not a JSON")
    city_obj.update(city_dict)
    return jsonify(city_obj.to_dict())
