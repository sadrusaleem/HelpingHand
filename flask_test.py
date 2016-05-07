# -*- coding: utf-8 -*-
"""
Created on Sat May  7 14:31:59 2016

@author: kmarathe
"""

from flask import Flask
import csv
import json


from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
cache.set('counter',100)


app = Flask(__name__)



counter=0
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
    

@app.route("/shelters")
def shelters():
    return csv2json("dataset/shelters.csv",("Name","City","Borough","Address","Latitude","Longitude","StartTime","EndTime","ServiceType"))

@app.route("/food/<username>")
def food(username):
    counter=cache.get('counter')
    print(counter)
    x= cache.set('counter', counter+1)
    return username+":"+str(counter)+":"+csv2json("dataset/FacilityDetails.csv",("Name","Brief Description","Proximity","Street Address","City","State","Zip Code","Phone Number","Web Site","Hours of Operation"))

@app.route("/food/<username>")
def results(latitude, longitude, time):
    return

if __name__ == "__main__":
    app.run(debug=True)

    
 #jsonfile.write(out)
    