from config import db
import datetime

###############################################################################
# TEST FUNCTIONS

def test_number_of_entries():
    '''checks whether the no of documents in mongoDB matches the no of
    15 minute steps between first and last timestamp --> no duplicates, no gaps'''
    
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
    
    last_timestamp = get_last_timestamp_from_mongo()
    first_timestamp = get_first_timestamp_from_mongo()
    timedelta = last_timestamp - first_timestamp
    entries_theoretical = timedelta / datetime.timedelta(minutes=15) + 1
    entries_in_mongo = db.pegeldata.count()
    assert entries_theoretical == entries_in_mongo