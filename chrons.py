"""this script contains all the chronjobs that call certain URLS on the API that
trigger actions"""

# fetch - every 15 minutes
# test - once per day
# train - once per day
# predict - once per day
# make new chart - every 15 minutes
# show chart
import requests
import argparse

###############################################################################
# MAIN FUNCTION

def main(action):
    if action == "fetch":
        response = requests.get("http://127.0.0.1:5000/api/control/fetch")
        print(response)             
    else:
        return print("type -do, and then 'fetch', 'XX' as parameter")
                          
###############################################################################
# ARGPARSE FOR CHRONJOBS

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='chronjobs')
    PARSER.add_argument('-do', '--action', type=str)
    ARGS = PARSER.parse_args()
    main(ARGS.action)