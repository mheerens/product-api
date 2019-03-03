# API-centric Data Science Product
This project is to demonstrate a working data science product using methods such as
modularization, data gathering through apis, continuous inprovement of ML model, publishing
and visualisation via minimal website/minimal api and continuous testing - all hosted
on AWS. The main idea is to build everything around an API, and use that API for
(A) controlling/triggering main fuctions such as unpdating the database, re-training the 
machine learning model and (B) making data and results available through jsons.
As a result, any theoretical application can make use of this data science product,
as long it is connected to the web!
# Overview
![alt text](overview.png)
## prefill.py
This script performs the inital prefilling of mongoDB atlas from a given data scource
## fetch.py
Checks and fetches deltas between most recent data on atlas and newest data 
available in original data source
## predict_ARIMA.py
Uses available data on atlas to train a machine learning model (ARIMA) that can predict
future values, then saves them into MongoDB Atlas
## show.py
Creates a nice visualization of the training data as well as predicted values
as html document (plot.ly)
## api.py
Flask server file
## test.py
Test scripts for database, API connection
## config.py
Main settings for the project, such as server connections, prediction horizon etc.
## fabfile.py
fabric script that setups the AWS