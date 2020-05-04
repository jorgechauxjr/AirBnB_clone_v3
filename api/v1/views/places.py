#!/usr/bin/python3

"""Places module of view package"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from os import getenv
from flasgger.utils import swag_from

storage_t = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/cities/<city_id>/places", methods=["GET", "POST"])
@swag_from('flasgger/places/city_id_places_get.yml', methods=['GET'])
@swag_from('flasgger/places/city_id_places_post.yml', methods=['POST'])
def create_or_get_place(city_id=None):
    """Creates or get a place given a city id"""

    obj_city = storage.get("City", city_id)

    if obj_city is None:
        abort(404)

    if request.method == "GET":
        objs = storage.all("Place")
        place_by_city = []
        for obj in objs.values():
            obj_dict = obj.to_dict()
            if obj_dict.get('city_id') == city_id:
                place_by_city.append(obj_dict)
        return jsonify(place_by_city)

    if request.method == "POST":
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
@swag_from('flasgger/places/place_id_places_get.yml', methods=['GET'])
@swag_from('flasgger/places/place_id_places_delete.yml', methods=['DELETE'])
@swag_from('flasgger/places/place_id_places_put.yml', methods=['PUT'])
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


@app_views.route("/places_search", methods=["POST"])
@swag_from('flasgger/places/places_search_post.yml', methods=['POST'])
def places_search():

    if request.is_json is False:
        abort(400, "Not a JSON")

    objs_place = storage.all("Place")
    all_places = [place for place in objs_place.values()]
    dict_req = request.get_json()
    state_ids = set(dict_req.get("states", []))
    cities_ids = set(dict_req.get("cities", []))
    amenities_ids = set(dict_req.get("amenities", []))
    sum_lens = len(state_ids) + len(cities_ids) + len(amenities_ids)
    if not dict_req or sum_lens == 0:
        ans = [place.to_dict() for place in all_places]
        return jsonify(ans)

    all_cities = storage.all("City")
    # Get all cities ids that are in state_ids
    states_cities = []
    for city in all_cities.values():
        if city.state_id in state_ids:
            states_cities.append(city.id)
    # Verify if cities_ids exists in storage
    cities_ids_real = []
    for city_id in cities_ids:
        if storage.get("City", city_id):
            cities_ids_real.append(city_id)
    # All cities from each states_ids join with all cities_ids
    states_cities = set(states_cities + cities_ids_real)
    # Filter all places by ids of cities
    if len(states_cities) > 0:
        all_places = [
            place for place in all_places if place.city_id in states_cities]
    # Verify if amenities_ids exists in storage
    amenities_ids_real = []
    for amenity_id in amenities_ids:
        if storage.get("Amenity", amenity_id):
            amenities_ids_real.append(amenity_id)
    # Get place that have all amenities
    filter_place_amenity = []
    for place in all_places:
        place__amenities = []
        if place.amenities:
            place__amenities = [amenity.id for amenity in place.amenities]

        if place__amenities and amenities_ids_real and all([
                amenity_id in place__amenities for
                amenity_id in amenities_ids_real]):
            filter_place_amenity.append(place)

    # If filter of amenity exists choose that instead
    if len(filter_place_amenity) > 0:
        ans = [place.to_dict() for place in filter_place_amenity]
    else:
        ans = [place.to_dict() for place in all_places]
    for dict_place in ans:
        if "amenities" in dict_place:
            del dict_place["amenities"]
    return jsonify(ans)
