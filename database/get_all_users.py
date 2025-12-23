import os
from pymongo import MongoClient
from dotenv import load_dotenv

# =====================
# LOAD ENV
# =====================
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
print("paramenter of database! ")
print(MONGODB_URI)
# =====================
# CONNECT MONGODB
# =====================
client = MongoClient(MONGODB_URI)

# Lấy database từ URI (baoan_dev)
db = client.get_default_database()

users = db["users"]

print("MongoDB connected:", db.name)


# =====================
# GET ALL USERS
# =====================
def get_all_users():
    return list(
        users.find({})
    )


# =====================
# TEST
# =====================
if __name__ == "__main__":
    all_users = get_all_users()
    print("number of users in system: ",len(all_users))
    for u, v in enumerate(all_users):
        print(u)  # index
        print(v)  # user (dict)
