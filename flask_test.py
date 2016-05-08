# -*- coding: utf-8 -*-
"""
Created on Sat May  7 14:31:59 2016

@author: kmarathe
"""

from flask import Flask
import csv
import json
from flask import jsonify


from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
cache.set('counter',100)


app = Flask(__name__)

import requests # pip install requests
import json

class Shelter(object):
    name=""
    address=""
    lat=""
    long=""
    service_type=1
    daysOfWeek=""
    startTime=""
    endTime=""
    phone=""
        
    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, address, lat, long, service_type,daysofweek,starttime,endtime,phone):
        self.name = name
        self.address = address
        self.lat = lat
        self.long = long
        self.service_type = service_type
        self.daysOfWeek = daysofweek
        self.startTime = starttime
        self.endTime = endtime
        self.phone = phone
        
    def serialize(self):
        return {
           'name' : self.name,
           'address': self.address,
           'lat': self.lat,
           'long': self.long,
           'service_type': self.service_type,
           'phone': self.phone
        }
        
def make_shelter(name, address, lat, long, service_type,daysofweek,starttime,endtime,phone):
    shelter = Shelter(name, address, lat, long, service_type,daysofweek,starttime,endtime,phone)
    return shelter


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




@app.route("/")
def hello():
    global counter
    
    return "Hello World! "+1


#from uber_rides.session import Session
    
def csv2json(filename,fieldnames):
    csvfile = open(filename, 'r')
    #jsonfile = open('file.json', 'w')

    #fieldnames = ("Name","City","Borough","Address","Latitude","Longitude","StartTime","EndTime","ServiceType")  
    reader = csv.DictReader( csvfile, fieldnames)
    out = json.dumps( [ row for row in reader ] )
    return out

fields=["name","address","lat","long","service_type","daysofweek","starttime","endtime","phone"]
def shelters_csv(filename):
    shelters= []
    for line in open(filename, 'r'):
        csv_row = line.split(sep=",") #returns a list ["1","50","60"]
        name=csv_row[1]
        address=csv_row[4]+","+csv_row[2]
        lat_long=getLatLngFromAddress(address)
        long = lat_long['x']
        lat = lat_long['y']
        lat=""
        long=""
        service_type=1
        daysOfWeek=""
        startTime=csv_row[7]
        endTime=csv_row[8]
        phone=""
        shelter = make_shelter(name, address, lat, long, service_type,daysOfWeek,startTime,endTime,phone)
        shelters.append(shelter)
    return shelters
    


@app.route("/shelters")
def shelters():
    return csv2json("dataset/shelters.csv",("Name","City","Borough","Address","Latitude","Longitude","StartTime","EndTime","ServiceType"))

@app.route("/food/<username>")
def food(username):
    counter=cache.get('counter')
    print(counter)
    x= cache.set('counter', counter+1)
    return username+":"+str(counter)+":"+csv2json("dataset/FacilityDetails.csv",("Name","Brief Description","Proximity","Street Address","City","State","Zip Code","Phone Number","Web Site","Hours of Operation"))

@app.route("/food/input")
def results(input):
    return

#if __name__ == "__main__":
#    app.run(debug=True)

    
 #jsonfile.write(out)
    