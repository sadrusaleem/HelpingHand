import requests # pip install requests
import json

# generate a token with your client id and client secret
TOKEN = requests.post('https://www.arcgis.com/sharing/rest/oauth2/token/', params={
  'f': 'json',
  'client_id': 'yrgHZpJ0ZJxstOse',
  'client_secret': 'b9e6c0b2942e47d8a6a9098fd17a6c1c',
  'grant_type': 'client_credentials',
  'expiration': '1440'
})
#url to geocode an address
GEOCODING_URL = 'http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find'
#url to find closest shelter/pantry
CLOSEST_URL = 'http://route.arcgis.com/arcgis/rest/services/World/ClosestFacility/NAServer/ClosestFacility_World/solveClosestFacility'

def getLatLngFromAddress(address):
    #given an address, returns lat/lng in the form {'x': latitude, 'y': longitude}

    try:
        data = requests.post(GEOCODING_URL, params={
            'f': 'json',
            'token': TOKEN.json()['access_token'],
            'text': address
        })

        data_json = data.json()
        location = data_json.get('locations')[0] #possible locations, we just take first
        return location.get('feature').get('geometry')
    except Exception:
        return None

def get_nearest_facilities(x, y):
    #our anchor location (the user's location)
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

    #the list of shelters
    facilities = {
        "features": [
            {
                "geometry": {
                    "x": -73.98135204156267,
                    "y": 40.745374368133696
                },
                "attributes": {
                    "Name": "Mainchance Drop-in Center"
                }
            },
            {
                "geometry": {
                    "x": -86.907479,
                    "y": 40.745374368133696
                },
                "attributes": {
                    "Name": "The Living Room Drop-in Center"
                }
            }
        ]
    }

    data = requests.post(CLOSEST_URL, data={
        'f': 'json',
        'token': TOKEN.json()['access_token'],
        'incidents': json.dumps(incidents),
        'facilities': json.dumps(facilities)
    })
    import ipdb; ipdb.set_trace()

    return data.json()


lat_lng = getLatLngFromAddress('324 East 82nd street, NYC')

print(get_nearest_facilities(-73.98135204156267, 40.745374368133696))


