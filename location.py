import requests  # pip install requests
import json

# generate a token with your client id and client secret
TOKEN = 'J5C_V0i7WaDtYRgMwfr4zYECD3LRIWvsuxIRdf9ODr3HBuPbNZnOlnmypjdwO2N4KMrZVK89-Efbvj8rpXKZvR0TvbuGmKj_SC665k0ZyF0UoI75fU90g2v0jqblTM0f2GIknQSH2DctSrwUprrELA..'
# url to geocode an address
GEOCODING_URL = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find'
# url to find closest shelter/pantry
CLOSEST_URL = 'http://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World/solveClosestFacility'


def getLatLngFromAddress(address):
    # given an address, returns lat/lng in the form {'x': latitude, 'y': longitude}

    try:
        data = requests.post(GEOCODING_URL, params={
            'f': 'json',
            # 'token': TOKEN.json()['access_token'],
            'text': address
        })

        data_json = data.json()
        location = data_json.get('locations')[0]  # possible locations, we just take first
        return location.get('feature').get('geometry')
    except Exception:
        return None


def get_nearest_facilities(x, y, features):
    incidents = {
        "features": [
            {
                "geometry": {
                    "x": x,
                    "y": y
                },
                "attributes": {
                    "Name": "user_location"
                }
            }
        ]
    }


    data = requests.post(CLOSEST_URL, params={
        'f': 'json',
        'token': TOKEN,
        'incidents': json.dumps(incidents),
        'facilities': json.dumps(features),
        'returnDirections': True,
        'defaultTargetFacilityCount': 5
    })
    #import ipdb; ipdb.set_trace()

    #import ipdb; ipdb.set_trace()

    return data.json()  # lat_lng = getLatLngFromAddress('2634 30th St Astoria, New York')
# print(get_nearest_facilities(lat_lng['x'], lat_lng['y']))
