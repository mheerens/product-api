"""This script performs the inital prefilling of mongoDB atlas from a given data scource"""
""" https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json"""

import requests
import json
from config import db

def delete_data():
    db.pegeldata.delete_many({})

def initial_load():
    ### still per minute! ###
    response = requests.get("https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json?start=2019-01-01T09:00%2B01:00&end=2019-02-18T16:00%2B01:00")
    json_data = json.loads(response.text)
    for i,_ in enumerate(json_data):
        db.pegeldata.insert_one({"station": "HAMBURG-ST.PAULI",
                             "timestamp" : json_data[i]["timestamp"],
                             "value" : json_data[i]["value"]
                             })
    
def delta_load(datefrom):
    fromdate = get_latest_entry_mongo()
    todate = get_latest_entry_source()
    delta_load = get_delta(fromdate, todate)
    upload_data(delta_load)
    

