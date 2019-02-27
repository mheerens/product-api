"""this script contains all the chronjobs that call certain URLS on the API that
trigger actions"""
# export VISUAL=nano; crontab -e
# 6,21,36,51 * * * * python3 /home/ec2-user/api-product/chrons.py -do fetch
# check errors in var/mail/ec2-user

import requests
import argparse

###############################################################################
# MAIN FUNCTION

def main(action):
    if action == "fetch":
        response = requests.get("http://0.0.0.0:8080/api/control/fetch")
        print(response)
    elif action == "predict":
        response = requests.get("http://0.0.0.0:8080/api/control/predict")
        print(response)        
    else:
        return print("type -do, and then 'fetch', or 'predict', 'XX' as parameter")
                          
###############################################################################
# ARGPARSE FOR CHRONJOBS

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='chronjobs')
    PARSER.add_argument('-do', '--action', type=str)
    ARGS = PARSER.parse_args()
    main(ARGS.action)