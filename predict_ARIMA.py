from pmdarima.arima import auto_arima
from config import db
from datetime import datetime, timedelta
import pandas as pd

###############################################################################
# FUNCTIONS

def get_data_from_mongodb(days_back):
    '''returns data starting from days_back until now from mongoDB'''
    current_date = datetime.now()
    start_date = current_date - timedelta(days=days_back)
    data = list(db.pegeldata.find({"timestamp" : {"$gte": start_date} }))
    return data 

def preprocess_data(data):
    '''PREPROCESSING: Takes data from mongoDB and turns it into a dataframe 
    that ARIMA can read'''
    timestamps = []
    water_levels = []
    for i,_ in enumerate(data):
        timestamps.append(data[i]["timestamp"])
        water_levels.append(data[i]["value"])
    df = pd.DataFrame()
#    df["ds"] = timestamps
    df["y"] = water_levels
    return df

def train_ARIMA(df):
    '''Train model'''
    m = auto_arima(df, trace=True, error_action='ignore', suppress_warnings=True)
    m.fit(df)
    return m

def make_forecast_df(m, days, data):
    prediction_periods = days*24*4
    last_actual_timestamp = data[len(data)-1]["timestamp"]
    first_prediction_timestamp = last_actual_timestamp + timedelta(minutes=15)
    last_prediction_timestamp = first_prediction_timestamp + + timedelta(minutes=15*prediction_periods-1)
    timestamps = pd.date_range(first_prediction_timestamp, last_prediction_timestamp, freq = "15min")
    forecast = m.predict(n_periods=prediction_periods)
    forecast_df = pd.DataFrame()
    forecast_df["values"] = forecast
    forecast_df["timestamps"] = timestamps
    return forecast_df

def upload_predictions_to_mongodb(forecast_df):
    '''uploads data from df to mongoDB'''
    current_date = datetime.now() # prediction timestamp
    timestamps = list(forecast_df['timestamps'])
    values = list(forecast_df['values'])
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
    data = get_data_from_mongodb(90)
    df = preprocess_data(data)
    m = train_ARIMA(df)
    forecast_df = make_forecast_df(m, 7, data)
    delete_old_predictions() # to avoid data overflow / keeping db clean
    message = upload_predictions_to_mongodb(forecast_df)
    return message
