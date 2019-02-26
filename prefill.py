"""This script performs the inital prefilling of mongoDB atlas from a given data scource"""
""" https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json"""

import requests
import json
from config import db
import pandas as pd

###############################################################################
# FUNCTIONS

def delete_data():
    '''CAREFUL: deletes all entries in collection'''
    db.pegeldata.delete_many({})
    
def get_initial_data():
    '''gets initial data from API and stores it in df'''
    response = requests.get("https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json?start=2019-02-01T00:00%2B01:00&end=2019-02-25T16:00%2B01:00")
    json_data = json.loads(response.text)
    df = pd.DataFrame(json_data)
#    df.index = pd.to_datetime(df.index, unit='s')
    df['timestamp'] = df['timestamp'].astype('datetime64[s]') + pd.DateOffset(hours=1)
    df.index = pd.to_datetime(df['timestamp'], unit='s')
    # downsample data
    df = df.asfreq('15Min')
    return df
    
def initial_load(df):
    '''uploads data from df to mongoDB'''
    timestamps = list(df['timestamp'])
    values = df['value']
    for i,_ in enumerate(timestamps):
        db.pegeldata.insert_one({"station": "HAMBURG-ST.PAULI",
                             "timestamp" : timestamps[i],
                             "value" : values[i]
                             })
    print(f"{len(timestamps)} entries initially uploaded")

###############################################################################
# MAIN FUNCTION

def main():
    '''main function'''
    df = get_initial_data()
    initial_load(df)
    
