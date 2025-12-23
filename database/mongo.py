from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "company_db"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_db():
    return db
