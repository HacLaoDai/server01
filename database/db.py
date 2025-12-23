# db.py
from pymongo import MongoClient

MONGODB_URI = "mongodb://baoan_dev:5769boan20s12rui@103.159.51.61/baoan_dev"

client = MongoClient(MONGODB_URI)
db = client.get_default_database()
users_col = db["users"]
# print(users_col)
# print("done")