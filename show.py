"""Exemplary application that gets data from API for further use, in this case
a visualization of the available data"""


import plotly as py
import plotly.graph_objs as go
import pandas as pd
from config import db, HTTP_AWS

def get_data_from_API(collection):
    # use HTTP_AWS adress!
    timestamps = []
    values = []
    dump = list(db[collection].find({}))
    for i,j in enumerate(dump):
        timestamps.append(dump[i]["timestamp"])
        values.append(dump[i]["value"])
    df = pd.DataFrame()
    df["timestamps"] = timestamps
    df["values"] = values
    return df

def make_chart():
    df_actuals = get_data("pegeldata")
    df_predictions = get_data("pegelpredictions")
    
    trace_high = go.Scatter(
                    x=df_actuals['timestamps'],
                    y=df_actuals['values'],
                    name = "actuals",
                    line = dict(color = '#17BECF'),
                    opacity = 0.8)
    
    trace_low = go.Scatter(
                    x=df_predictions['timestamps'],
                    y=df_predictions['values'],
                    name = "predictions",
                    line = dict(color = '#7F7F7F'),
                    opacity = 0.8)
    
    data = [trace_high,trace_low]
    
    layout = dict(
        title = "WATER LEVELS ELBE @ HAMBURG ST.PAULI",
        xaxis = dict(
            range = ['2019-02-01','2019-03-31'])
    )
    
    fig = dict(data=data, layout=layout)
    
    py.offline.plot(fig, filename='show.html')