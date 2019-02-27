"""Checks and fetches deltas between most recent data on atlas and newest data 
available in original data source
chronjob should be done every 15 minutes, 5 minutes after quarter"""

import requests
import pandas as pd
import json
from config import db
import datetime


###############################################################################
# FUNCTIONS

def get_first_timestamp_from_mongo():
    '''determines first entry in mongoDB as datetime.datetime format'''
    first = list(db.pegeldata.find().sort([("timestamp", 1)]).limit(1))
    first_timestamp  = first[0]["timestamp"]
    return first_timestamp

def get_last_timestamp_from_mongo():
    '''determines latest entry in mongoDB as datetime.datetime format'''
    latest = list(db.pegeldata.find().sort([("timestamp", -1)]).limit(1))
    last_timestamp  = latest[0]["timestamp"]
    return last_timestamp
    
def add_15_minutes(timestamp):
    '''adds 15 minutes to timestamp'''
    timestamp += datetime.timedelta(minutes=15)
    return timestamp

def create_API_format(timestamp):
    '''converts datetime.datetime to format that can be read by API'''
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day
    hour = timestamp.hour
    minute = timestamp.minute
    startstring = f"{year}-{month}-{day}T{hour}:{minute}%2B01:00"
    return startstring

def delete_old_data(days_back):
    ''' to keep db lean'''
    current_date = datetime.datetime.now()
    last_relevant_date = current_date - datetime.timedelta(days=days_back)    
    db.pegeldata.delete_many({"timestamp" : {"$lt": last_relevant_date} })
    
    
def fetch_delta(startstring):
    '''fetches data from given start string until now from API'''
    start = startstring#f"2019-02-24T03:00%2B01:00"
    fetchstring = f"https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/HAMBURG-ST.PAULI/W/measurements.json?start={start}"
    response = requests.get(fetchstring)
    json_data = json.loads(response.text)
    df = pd.DataFrame(json_data)
    df.index = pd.to_datetime(df.index, unit='s')
    df['timestamp'] = df['timestamp'].astype('datetime64[s]') + pd.DateOffset(hours=1)
    df.index = pd.to_datetime(df['timestamp'], unit='s')
    # downsample data
    df = df.asfreq('15Min')
    return df

def upload_delta(df_delta):
    '''uploads data from df to mongoDB'''
    timestamps = list(df_delta['timestamp'])
    values = df_delta['value']
    for i,_ in enumerate(timestamps):
        db.pegeldata.insert_one({"station": "HAMBURG-ST.PAULI",
                             "timestamp" : timestamps[i],
                             "value" : values[i]
                             })
    message = f"{len(timestamps)} entries uploaded"
    return message
    
###############################################################################
# MAIN FUNCTION

def main():
    '''main function'''
    last_timestamp = get_last_timestamp_from_mongo()
    last_timestamp_plus = add_15_minutes(last_timestamp)
    startstring = create_API_format(last_timestamp_plus)
    df_delta = fetch_delta(startstring)
    delete_old_data(90)
    message = upload_delta(df_delta)
    return message
    