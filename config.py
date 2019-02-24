import pymongo
from credentials import mongopass, mongouser
###############################################################################
# MONGODB SETTINGS LOCAL
client = pymongo.MongoClient()
db_local = client.apiproduct
###############################################################################
# MONGODB SETTINGS ATLAS
#mongopass = os.getenv("MONGOPASS")
connection = f"mongodb://{mongouser}:{mongopass}@projectdata-shard-00-00-fmvv2.mongodb.net:27017,projectdata-shard-00-01-fmvv2.mongodb.net:27017,projectdata-shard-00-02-fmvv2.mongodb.net:27017/test?ssl=true&replicaSet=ProjectData-shard-0&authSource=admin&retryWrites=true"
atlasclient = pymongo.MongoClient(connection)
db_atlas = atlasclient.apiproduct
###############################################################################
db = db_atlas