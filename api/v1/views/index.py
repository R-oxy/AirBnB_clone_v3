#!/usr/bin/python3

from api.v1.views import (
    app_views, storage, Amenity, City, Place,
    Review, State, User
)
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each object by type"""
    objects = {User: "users",
               Amenity: "amenities",
               City: "cities",
               Place: "places",
               Review: "reviews",
               State: "states"}

    stats = {}
    for cls in objects.keys():
        stats[objects[cls]] = storage.count(cls)
    return jsonify(stats)
