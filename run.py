from flask import Flask, jsonify
import os
import json
from crossdomain import crossdomain
from flask_test import shelters_csv, facilities_csv
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

shelters = shelters_csv()
import ipdb; ipdb.set_trace()
facilities = facilities_csv()
import ipdb; ipdb.set_trace()

cache.set('shelters', shelters)
cache.set('facilities', facilities)

app = Flask(__name__)

@app.route('/')
@crossdomain(origin='*')
def hello_world():
    data = [{'name': 'Test Shelter',
            'address': '120 East 32nd St, New York',
            'lat': 40.745374368133696,
            'long': -73.98135204156267,
            'service_type': 1,
            'phone': '9545361686'
    }]
    
    return json.dumps(data)

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