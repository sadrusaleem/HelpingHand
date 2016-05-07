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
    except Exception, e:
        return None

def get_nearest_facilities(lat, lng):
    #our anchor location
    incidents = {
        "features": [
            {
                "geometry": {
                    "x": -122.4079,
                    "y": 37.78356
                },
                "attributes": {
                    "Name": "Fire Incident 1",
                    "Attr_TravelTime": 4
                }
            }

        ]
    }

    #the list of places that we wanna compare distances for
    facilities = {
        "features": [
            {
                "geometry": {
                    "x": -24,
                    "y": 42
                },
                "attributes": {
                    "Name": "Fire Station 34",
                    "Attr_TravelTime": 4
                }
            },
            {
                "geometry": {
                    "x": 55,
                    "y": 86
                },
                "attributes": {
                    "Name": "Fire Station 29",
                    "Attr_TravelTime": 5
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


#print(getLatLngFromAddress('1430 Tremont St Boston MA 02120'))
print(get_nearest_facilities(143, 23))


