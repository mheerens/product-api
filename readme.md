# TO DO / NEXT STEPS
- make lean application that gets data from api and displays actual vs. predictions
- update documentation, simple chart with draw.io
# Overview
![alt text](overview.png)
# Data Science Product API
This project is to demonstrate a working data science product using methods such as
modularization, data gathering through apis, continuous inprovement of ML model, publishing
and visualisation via minimal website/minimal api and continuous testing - all hosted
on AWS
## prefill.py
This script performs the inital prefilling of mongoDB atlas from a given data scource
## fetch.py
Checks and fetches deltas between most recent data on atlas and newest data 
available in original data source
## train.py
Uses available data on atlas to train a machine learning model that can predict
future values (facebook prophet)
## predict.py
Uses most recent version of ML model to predict future values and saves them
into atlas
## show.py
Creates a nice visualization of the training data as well as predicted values
as html document (plot.ly)
## server.py
Flask server file
## test.py
Test scripts for database, API connection
## config.py
Main settings for the project, such as server connections, prediction horizon etc.
## fabric.py
fabric script that setups the AWS