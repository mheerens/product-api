"""Exemplary application that gets data from API for further use, in this case
a visualization of the available data
--> Like a STAND-ALONE APPLICATION"""

# chron:
# 8,23,38,53 * * * * python3 /home/ec2-user/product-api/show.py


import plotly as py
import plotly.graph_objs as go
import pandas as pd
import requests
import json
import datetime

#API_ADDRESS = "http://0.0.0.0:8080"
API_ADDRESS = "http://ec2-18-197-132-108.eu-central-1.compute.amazonaws.com:8080"

###############################################################################
# FUNCTIONS

def get_dates(days_back=14, days_future=7):
    fromdate = datetime.datetime.now() - datetime.timedelta(days=days_back)
    todate = datetime.datetime.now() + datetime.timedelta(days=days_future)
    return fromdate, todate

def convert_BSON_date(BSON_date):
    '''BSON date is defined in milliseconds from the unix date 01.01.1970'''
    unix_date = datetime.datetime(1970,1,1)
    timestamp = datetime.timedelta(milliseconds=BSON_date) + unix_date
    return timestamp

def get_data_from_API(source, fromdate, todate):
    #create correct timestamps that can be read by API
    fromstring = f"{fromdate.year}{'%02d' % fromdate.month}{'%02d' % fromdate.day}{'%02d' % fromdate.hour}{'%02d' % fromdate.minute}"
    tostring = f"{todate.year}{'%02d' % todate.month}{'%02d' % todate.day}{'%02d' % todate.hour}{'%02d' % todate.minute}"
   
    #get data from API
    if source == "pegeldata":
        response = requests.get(f"{API_ADDRESS}/api/getdata/actual/{fromstring}/{tostring}")
    elif source == "pegelpredictions":
        response = requests.get(f"{API_ADDRESS}/api/getdata/predicted/{fromstring}/{tostring}")
    dump = json.loads(response.text)
    
    #create lists
    timestamps = []
    values = []
    for i,j in enumerate(dump):
        timestamp = convert_BSON_date(dump[i]["timestamp"]["$date"])
        timestamps.append(timestamp)
        values.append(dump[i]["value"])
        
    df = pd.DataFrame()
    df["timestamps"] = timestamps
    df["values"] = values
    return df


def make_chart(df_actuals, df_predictions, fromdate, todate):
    
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
                    line = dict(color = '#F58A18'),
                    opacity = 0.8)
    
    data = [trace_high,trace_low]
    
    
    fromstring = f"{fromdate.year}-{'%02d' % fromdate.month}-{'%02d' % fromdate.day}"
    tostring = f"{todate.year}-{'%02d' % todate.month}-{'%02d' % todate.day}"
    layout = dict(
        title = "WATER LEVELS ELBE @ HAMBURG ST.PAULI",
        xaxis = dict(
            range = [fromstring, tostring])
    )
    
    fig = dict(data=data, layout=layout)
    
    py.offline.plot(fig, filename='/home/ec2-user/product-api/templates/show.html', auto_open=False)
    
###############################################################################
# MAIN FUNCTION
    
def main():
    fromdate, todate = get_dates(days_back=14, days_future=7)
    df_actuals = get_data_from_API("pegeldata", fromdate, todate)
    df_predictions = get_data_from_API("pegelpredictions", fromdate, todate) 
    
    fromdate_chart, todate_chart = get_dates(days_back=14, days_future=7)
    make_chart(df_actuals, df_predictions, fromdate_chart, todate_chart)
    
############################################################################### 

if __name__ == "__main__":
    main()