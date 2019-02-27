"""this script loads data from mongoDB, takes it as input to train Prophet,
then makes predictions and uploads them back into mongoDB"""

"""TEMPORARILY DISABLED DUE TO MEMORY RESTRICTIONS ON AWS
import pandas as pd
from fbprophet import Prophet 
from config import db
from datetime import datetime, timedelta

###############################################################################
# FUNCTIONS

def get_data_from_mongodb(days_back):
    '''returns data starting from days_back until now from mongoDB'''
    current_date = datetime.now()
    start_date = current_date - timedelta(days=days_back)
    data = list(db.pegeldata.find({"timestamp" : {"$gte": start_date} }))
    return data

def make_prophet_dataframe(data):
    '''PREPROCESSING: Takes data from mongoDB and turns it into a dataframe 
    that prophet can read'''
    timestamps = []
    water_levels = []
    for i,_ in enumerate(data):
        timestamps.append(data[i]["timestamp"])
        water_levels.append(data[i]["value"])
    df = pd.DataFrame()
    df["ds"] = timestamps
    df["y"] = water_levels
    return df

def train_prophet(df):
    '''Train model'''
    m = Prophet()
    m.fit(df)
    return m

def make_future_df(m, days_into_future):
    '''makes a future dataframe where predictions go in'''
    future_df = m.make_future_dataframe(periods=days_into_future*24*4, freq="15min", include_history=False)
    #future.tail()
    return future_df

def make_predictions(m, future_df):
    '''predict'''
    predictions = m.predict(future_df)
    return predictions

def upload_predictions_to_mongodb(predictions):
    '''uploads data from df to mongoDB'''
    current_date = datetime.now() # prediction timestamp
    timestamps = list(predictions['ds'])
    values = list(predictions['yhat'])
    for i,_ in enumerate(timestamps):
        db.pegelpredictions.insert_one({"station": "HAMBURG-ST.PAULI",
                             "prediction_timestamp" : current_date,
                             "timestamp" : timestamps[i],
                             "value" : values[i]
                             })
    message = f"{len(timestamps)} predictions uploaded"
    return message

def delete_old_predictions():
    '''CAREFUL: deletes all entries in collection'''
    db.pegelpredictions.delete_many({})
    
###############################################################################
# MAIN FUNCTION

def main():
    '''combining functions'''
    data = get_data_from_mongodb(365)
    df = make_prophet_dataframe(data)
    m = train_prophet(df)
    future_df = make_future_df(m, 7)
    predictions = make_predictions(m, future_df)
    delete_old_predictions() # to avoid data overflow / keeping db clean
    message = upload_predictions_to_mongodb(predictions)
    return message
    
"""