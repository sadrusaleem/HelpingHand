# -*- coding: utf-8 -*-
"""
Created on Sat May  7 14:31:59 2016

@author: kmarathe
"""
import os
#os.chdir("/Users/kmarathe/Desktop/code/helping_hand/HelpingHand")
from flask import Flask
import csv
import json
from flask import jsonify
from location import getLatLngFromAddress


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

def shelters_csv():
    shelters= []
    for line in open("dataset/shelters.csv", 'r'):
        try:
            csv_row = line.split(",") #returns a list ["1","50","60"]
            name=csv_row[1]
            address=csv_row[4]+","+csv_row[2]
            lat_long=getLatLngFromAddress(address)
            import ipdb ; ipdb.set_trace()
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
    
shelters_csv()

#if __name__ == "__main__":
#    app.run(debug=True)

    
 #jsonfile.write(out)
    