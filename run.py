from flask import Flask, jsonify
import os
import json
from crossdomain import crossdomain
from flask_test import shelters_csv, facilities_csv
from random import randint


shelters = shelters_csv()
facilities = facilities_csv()


app = Flask(__name__)


def _get_random_status():
    return randint(0,1)

@app.route('/')
@crossdomain(origin='*')
def hello_world():
    data_objs = shelters + facilities
    data_json = []

    for obj in data_objs:
        data_json.append(obj.serialize())

    for place in data_json:
        place['status'] = _get_random_status()
    
    
    return json.dumps(data_json)

@app.route('/locations')
def hello_world2(input):
    shelters = []

    for shelter in cache.get('facilities'):
        shelters.append(shelter.serialize())

    return jsonify(data=shelters)

if __name__ == "__main__":
    app.run(debug=True, 
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))