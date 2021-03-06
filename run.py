from flask import Flask, jsonify, request
import os
import json
from crossdomain import crossdomain
from flask_test import shelters_csv, facilities_csv, hospitals_csv, findClosestShelters
from random import randint
from location import get_nearest_facilities
import twilio.twiml
from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
shelters = shelters_csv()
facilities = facilities_csv()
hospitals = hospitals_csv()
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


def _get_random_status(name):
    if cache.get(name):
        return cache.get(name)
    return randint(0,1)

@app.route('/')
@crossdomain(origin='*')
def hello_world():
    data_objs = places
    data_json = []

    for obj in data_objs:
        data_json.append(obj.serialize())

    for place in data_json:
        place['status'] = _get_random_status(place['name'])
    
    
    return jsonify(data = data_json)


def _get_place_from_direction(dir):
    routeName = dir['routeName'].split('-')[1][1:]
    for place in places + hospitals:
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
    findClosestShelters(lat, long, hospitals)

    features = []
    for place in places:
        features.append(_place_to_feature(place))

    features = {'features': features[:20]}

    directions = get_nearest_facilities(long, lat, features)['directions']

    data_json = []
    for dir in directions:
        data_json.append(_get_place_from_direction(dir))


    features_hospitals = []
    for hospital in hospitals:
        features_hospitals.append(_place_to_feature(hospital))

    features_hospitals = {'features': features_hospitals[:20]}
    directions_hospitals = get_nearest_facilities(long, lat, features_hospitals)['directions']
    for dir in directions_hospitals:
        to_add = _get_place_from_direction(dir)
        if to_add:
            data_json.append(to_add)

    data_json.extend(shelters_serialized)

    for data in data_json:
        if data:
            data['status'] = _get_random_status(data['name'])

    return jsonify(data = data_json)

@app.route("/sms", methods=['GET', 'POST'])
def respond():
    body = request.values.get('Body', None)
    print body
    parts = body.split("*")
    if update_status(parts[0], parts[1]):
        print 'yay'
    else:
        print 'nah'
    resp = twilio.twiml.Response()
    resp.sms('We have updated the ' + parts[0] + " shelter to have a status of " + parts[1])
    return str(resp)

def update_status(name, new_status):
    if new_status in ('closed', 'open'):
        if new_status == 'closed':
            cache.set(name, 0)
        else:
            cache.set(name, 1)
        
        return True
    return False

if __name__ == "__main__":
    app.run(debug=True,
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))

#if __name__ == "__main__":
 #   app.run(debug= True)