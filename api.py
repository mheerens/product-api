"""
This file contains the main API server using flask.
# start via: FLASK_APP=api.py flask run
"""
from flask import Flask, request#, send_from_directory
from fetch import main as fetch_main
from config import db
from bson.json_util import dumps
from datetime import datetime
from test import test_number_of_entries
from credentials import shutdownpw


# flask api used as control interface for program
# fetch /api/fetch
# train /api/train
# predict /api/predict/10   (days, variable)
# erase predictions /api/droppredictions
# make chart /api/draw
# show chart /chart
# GET DATA

###############################################################################
# INITIALIZING FLASK

app = Flask(__name__)

###############################################################################
# SHUTDOWN FUNCTION - NO NEED TO KILL PROCESSES ON AWS WHEN USING THIS

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.route('/api/control/shutdown/<PASSWORD>')
def shutdown(PASSWORD):
    if PASSWORD == shutdownpw:
        shutdown_server()
        return 'Server shutting down...'
    else:
        return 'Wrong password...'

###############################################################################
# API FUNCTIONS

@app.route("/api/control/fetch")
def trigger_fetching():
    '''triggers the fetching of latest data and uploading it into mongodb'''
    message = fetch_main()
    return message

@app.route("/api/control/test")
def trigger_testing():
    '''triggers testing functions'''
    message = test_number_of_entries()
    return message

@app.route("/api/getdata/<FROMDATE>/<TODATE>")
def return_data(FROMDATE, TODATE):
    '''returns data from mongoDB in the given timeframe for use in other applications.
    format for query has to be 201902212015 (21. Feb 2019, 8:15pm, YYYYMMDDHHMM)'''
    # parse startdate
    sy = int(FROMDATE[0:4])
    sm = int(FROMDATE[4:6])
    sd = int(FROMDATE[6:8])
    shr = int(FROMDATE[8:10])
    smin = int(FROMDATE[10:12])
    start = datetime(sy, sm, sd, shr, smin) 
    # parse enddate
    ey = int(TODATE[0:4])
    em = int(TODATE[4:6])
    ed = int(TODATE[6:8])
    ehr = int(TODATE[8:10])
    emin = int(TODATE[10:12])
    end = datetime(ey, em, ed, ehr, emin) 
    dump = dumps(db.pegeldata.find({"timestamp" : {"$gte": start, "$lt": end} }))
    return dump


