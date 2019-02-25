"""This script performs the inital prefilling of mongoDB atlas from a given data scource"""
""" https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json"""

import requests
import json
from config import db
import pandas as pd

def delete_data():
    db.pegeldata.delete_many({})
    
def get_initial_data():
    response = requests.get("https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json?start=2019-02-01T00:00%2B01:00&end=2019-02-25T16:00%2B01:00")
    json_data = json.loads(response.text)
    df = pd.DataFrame(json_data)
    df.index = pd.to_datetime(df.index, unit='s')
    df['timestamp'] = df['timestamp'].astype('datetime64[s]')
    df.index = pd.to_datetime(df['timestamp'], unit='s')
    # downsample data
    df = df.asfreq('15Min')
    return df
    
def initial_load():
    df = get_initial_data()
    timestamps = list(df['timestamp'].astype('str'))
    values = df['value']
    for i,_ in enumerate(timestamps):
        db.pegeldata.insert_one({"station": "HAMBURG-ST.PAULI",
                             "timestamp" : timestamps[i],
                             "value" : values[i]
                             })
    
"""    
def delta_load(datefrom):
    fromdate = get_latest_entry_mongo()
    todate = get_latest_entry_source()
    delta_load = get_delta(fromdate, todate)
    upload_data(delta_load)
"""    

