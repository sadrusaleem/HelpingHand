from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return {'name': 'Test Shelter',
            'address': '120 East 32nd St, New York',
            'lat': 40.745374368133696,
            'long': -73.98135204156267
            'service_type': 1,
            'phone': '9545361686'
    }

@app.route('/locations/input')
def hello_world(input):
    print input
    return input

if __name__ == "__main__":
    app.run(debug=True, 
            host=os.getenv('IP', '0.0.0.0'),
            port = int(os.getenv('PORT', '8080')))