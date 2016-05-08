from flask import Flask, jsonify, request
import os
import json
from crossdomain import crossdomain
from flask_test import shelters_csv, facilities_csv, findClosestShelters
from random import randint
from location import get_nearest_facilities

shelters = shelters_csv()
facilities = facilities_csv()
places = facilities

features = []
shelters_serialized = []

for shelter in shelters:
    shelters_serialized.append(shelter.serialize())


def _place_to_feature(place):
    return {
        "geometry": {
            "x": place.long,
            "y": place.lat
        },
        "attributes": {
            "Name": place.name
        }
    }


app = Flask(__name__)


def _get_random_status():
    return randint(0,1)

@app.route('/')
@crossdomain(origin='*')
def hello_world():
    data_objs = places
    data_json = []

    for obj in data_objs:
        data_json.append(obj.serialize())

    for place in data_json:
        place['status'] = _get_random_status()
    
    
    return jsonify(data = data_json)


def _get_place_from_direction(dir):
    routeName = dir['routeName'].split('-')[1][1:]
    for place in places:
        if place.name == routeName:
            #import ipdb; ipdb.set_trace()
            return place.serialize()
    return None


@app.route('/locations')
@crossdomain(origin='*')
def hello_world2():
    lat = float(request.args.get('lat'))
    long = float(request.args.get('long'))
    findClosestShelters(lat, long, places)

    features = []
    for place in places:
        features.append(_place_to_feature(place))

    features = {'features': features[:20]}

    directions = get_nearest_facilities(long, lat, features)['directions']

    data_json = []
    for dir in directions:
        data_json.append(_get_place_from_direction(dir))

    data_json.extend(shelters_serialized)

    for data in data_json:
        data['status'] = _get_random_status()

    #import ipdb; ipdb.set_trace()

    return jsonify(data = data_json)

if __name__ == "__main__":
    app.run(debug=True,
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))

#if __name__ == "__main__":
 #   app.run(debug= True)