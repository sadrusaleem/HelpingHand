# -*- coding: utf-8 -*-
"""
Created on Sat May  7 14:31:59 2016

@author: kmarathe
"""
import os
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
    reader = csv.DictReader(open("dataset/shelters.csv"), skipinitialspace=True)
    for csv_row in reader:
        try:
            #line2 = line.replace("\"", "")
            #csv_row = row.split(",") #returns a list ["1","50","60"]
            
            name=csv_row['Name']
            address=csv_row['Address']+","+csv_row['City']
            #import ipdb ; ipdb.set_trace()
            lat_long=getLatLngFromAddress(address)
            #import ipdb ; ipdb.set_trace()
            long = lat_long['x']
            lat = lat_long['y']
            
            service_type=1
            daysOfWeek=""
            startTime=csv_row['StartTime']
        
            endTime=csv_row['EndTime']
            phone=""
            shelter = make_shelter(name, address, lat, long, service_type,daysOfWeek,startTime,endTime,phone)
            shelters.append(shelter)
        except:
            pass
    return shelters
    
def facilities_csv():
    shelters= []
    reader = csv.DictReader(open("dataset/FacilityDetails.csv"), skipinitialspace=True)
    for csv_row in reader:
        try:
            #line2 = line.replace("\"", "")
            #csv_row = row.split(",") #returns a list ["1","50","60"]
            #import ipdb ; ipdb.set_trace()
            name=csv_row['Name']
            address=csv_row['Street Address']+","+csv_row['City']
            #import ipdb ; ipdb.set_trace()
            lat_long=getLatLngFromAddress(address)
            #import ipdb ; ipdb.set_trace()
            long = lat_long['x']
            lat = lat_long['y']
            
            service_type=2
            daysOfWeek=""
          
            phone=csv_row['Phone Number']
            shelter = make_shelter(name, address, lat, long, service_type,daysOfWeek,"","",phone)
            shelters.append(shelter)
        except:
            #import ipdb ; ipdb.set_trace()
            print("Exception")
            pass
    return shelters
    


shelters = shelters_csv()
facilities = facilities_csv()
#if __name__ == "__main__":
#    app.run(debug=True)

    
 #jsonfile.write(out)
    