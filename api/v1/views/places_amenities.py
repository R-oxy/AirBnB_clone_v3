#!/usr/bin/python3
"""
Module for Place-Amenity API
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import (app_views, storage, Place,
                          Amenity)
from os import getenv


app = Flask(__name__)


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object from a Place
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"],
                 strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """
    Links an Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return "Bad amenity", 404
    if amenity_id in place.amenities_id:
        return jsonify(amenity.to_json()), 200
    place.amenities_id.append(amenity_id)
    place.save()
    return jsonify(amenity.to_json()), 201
