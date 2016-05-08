import csv
import json
from location import getLatLngFromAddress

shelters_reader = csv.DictReader(open("dataset/shelters.csv"), skipinitialspace=True)
facilities_reader = csv.DictReader(open("dataset/FacilityDetails.csv"), skipinitialspace=True)


data_list = []

for csv_row in shelters_reader:
    try:
        address = csv_row['Address'] + "," + csv_row['City']
        # import ipdb ; ipdb.set_trace()
        lat_long = getLatLngFromAddress(address)

        data = {
            'address': address,
            'latitude': lat_long['y'],
            'longitude': lat_long['x']
        }

        data_list.append(data)
    except:
        pass

for csv_row in facilities_reader:
    try:
        address = csv_row['Street Address'] + "," + csv_row['City']
        lat_long = getLatLngFromAddress(address)

        data = {
            'address': address,
            'latitude': lat_long['y'],
            'longitude': lat_long['x']
        }

        data_list.append(data)
    except:
        pass

with open('latlngs2.json', 'w') as outfile:
    for data in data_list:
        json.dump(data, outfile)
        outfile.write('\n')