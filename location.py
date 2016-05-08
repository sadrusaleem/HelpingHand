import requests  # pip install requests
import json

# generate a token with your client id and client secret
TOKEN = 'Qtm1OymG8oVOFIeUKTq6RfsYwwZylOpXJOgNpt-OBVXnn0PDQl_eWZ2ktOH-A-SbyF3MFWSsBQ1m-mTkrbVtYPcu0NL9nbsr3-hzHB8j_Vz6jBZ9XZPZKDJ9EA8I-JBI_XNSAjkFaCSPHdDcfz6WxQ..'
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


def get_nearest_facilities(x, y):
    # our anchor location (the user's location)

    # incidents = '-73.9851, 40.7589;'
    # incidents = '-122.4496,37.7467'

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
                    "x": -75.907479,
                    "y": 40.745374368133696
                },
                "attributes": {
                    "Name": "The Living Room Drop-in Center"
                }
            }
        ]
    }

    data = requests.post(CLOSEST_URL, params={
        'f': 'json',
        'token': TOKEN,
        'incidents': json.dumps(incidents),
        'facilities': json.dumps(facilities),
        'returnDirections': True,
        'defaultTargetFacilityCount': 10
    })
    import ipdb; ipdb.set_trace()

    return data.json()

#lat_lng = getLatLngFromAddress('2634 30th St Astoria, New York')
#print(get_nearest_facilities(lat_lng['x'], lat_lng['y']))
