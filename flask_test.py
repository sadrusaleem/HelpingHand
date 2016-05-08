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
from datetime import datetime
import sys

datetime.now().strftime('%a')

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
           'daysofWeek': self.daysOfWeek,
           'long': self.long,
           'service_type': self.service_type,
           'phone': self.phone
        }
    
 
        
def make_shelter(name, address, lat, long, service_type,daysofweek,starttime,endtime,phone):
    shelter = Shelter(name, address, lat, long, service_type,daysofweek,starttime,endtime,phone)
    return shelter



latlong_cache = SimpleCache()
 #jsonfile.write(out)
with open("latlngs2.json",'r') as f:
    for line in f:
            try:
                jfile = json.loads(line)
                latlong_cache.set(jfile['address'],jfile)
            except ValueError:
                # Not yet a complete JSON value
                pass  


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
            #lat_long=getLatLngFromAddress(address)
            #import ipdb ; ipdb.set_trace()
            lat_long=latlong_cache.get(address)
            long = lat_long['longitude']
            lat = lat_long['latitude']
            
            service_type=1
            daysOfWeek=""
            #startTime=csv_row['StartTime']
        
            #endTime=csv_row['EndTime']
            phone=""
            shelter = make_shelter(name, address, lat, long, service_type,daysOfWeek,"","",phone)
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
            #lat_long=getLatLngFromAddress(address)
            #import ipdb ; ipdb.set_trace()
            lat_long=latlong_cache.get(address)
            long = lat_long['longitude']
            lat = lat_long['latitude']
            
            service_type=2
            daysOfWeek= ""
            
          
            phone=csv_row['Phone Number']
            shelter = make_shelter(name, address, lat, long, service_type,daysOfWeek,"","",phone)
            shelters.append(shelter)
        except:
            #import ipdb ; ipdb.set_trace()
            print("Exception")
            pass
    return shelters

import numpy as np
def findClosestShelters(lat,long,shelters):
    def inner_dist(shelter):
        return shelter_dist(lat, long, shelter)
    shelters.sort(key=lambda shelter2: inner_dist(shelter2))   
    return shelters
        
 
def shelter_dist(lat, long, shelter):
    try:
        lat_shelter = float(shelter.lat)
        long_shelter = float(shelter.long)
        return np.power(np.power(lat-(lat_shelter),2) + np.power(long - (long_shelter),2),0.5)
    except:
        return sys.float_info.max
    
def hospitals_csv():   
    shelters= []
    reader = csv.DictReader(open("dataset/Health_Facility_General_Information.csv"), skipinitialspace=True)
    for csv_row in reader:
        try:
            #line2 = line.replace("\"", "")
            #csv_row = row.split(",") #returns a list ["1","50","60"]
            #import ipdb ; ipdb.set_trace()
            #Address 1,Facility Address 2,Facility City
            if not csv_row['Facility City'] == "New York" or not csv_row['Short Description'] == "HOSP":
                pass
                        
            #import ipdb ; ipdb.set_trace()

            #address=""
            name=csv_row['Facility Name']
            address=csv_row['Facility Address 1']+","+csv_row['Facility Address 2'] + ","+ csv_row['Facility City']
            #import ipdb ; ipdb.set_trace()
            #lat_long=getLatLngFromAddress(address)
            #import ipdb ; ipdb.set_trace()
            #lat_long=latlong_cache.get(address)
            long = csv_row['Facility Longitude']
            lat = csv_row['Facility Latitude']
            
            service_type=3
            daysOfWeek= ""
            
          
            phone=csv_row['Facility Phone Number']
            shelter = make_shelter(name, address, lat, long, service_type,daysOfWeek,"","",phone)
            shelters.append(shelter)
        except:
            #import ipdb ; ipdb.set_trace()
            print("Exception")
            pass
    return shelters
    

x = shelters_csv()
y = facilities_csv()
z = hospitals_csv()
#if __name__ == "__main__":
#    app.run(debug=True)

    