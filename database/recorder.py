import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

# =====================
# CONNECT DB
# =====================
load_dotenv()
MONGODB_URI = "mongodb://baoan_dev:5769boan20s12rui@103.159.51.61/baoan_dev"

client = MongoClient(MONGODB_URI)
db = client.get_default_database()

recorders = db["recorders"]

# =====================
# INIT INDEX
# =====================
recorders.create_index("mac", unique=True)


# =====================
# CREATE
# =====================
def create_recorder(
    mac: str,
    ip_public: str,
    ip_lan: str,
    address: str,
    account: str,
    password: str,
    port: int
):
    data = {
        "mac": mac,
        "ip_public": ip_public,
        "ip_lan": ip_lan,
        "address": address,
        "account": account,
        "password": password,
        "port": port,
        "created_at": datetime.utcnow()
    }

    return recorders.insert_one(data).inserted_id
# =====================
# READ
# =====================
def get_recorder_by_mac(mac: str):
    return recorders.find_one({"mac": mac})


def get_recorder_by_id(recorder_id: str):
    return recorders.find_one({"_id": ObjectId(recorder_id)})


def get_all_recorders():
    return list(recorders.find({}))


# =====================
# UPDATE
# =====================
def update_recorder_by_id(recorder_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()

    result = recorders.update_one(
        {"_id": ObjectId(recorder_id)},
        {"$set": update_data}
    )
    return result.modified_count


def update_recorder_by_mac(mac: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()

    result = recorders.update_one(
        {"mac": mac},
        {"$set": update_data}
    )
    return result.modified_count


# =====================
# DELETE
# =====================
def delete_recorder_by_id(recorder_id: str):
    result = recorders.delete_one(
        {"_id": ObjectId(recorder_id)}
    )
    return result.deleted_count


def delete_recorder_by_mac(mac: str):
    result = recorders.delete_one(
        {"mac": mac}
    )
    return result.deleted_count

# test
# update_recorder_by_mac(
#     "3824F10EB8DC",
#     {"ip_lan": "192.168.100.119"}
# )

# delete_recorder_by_mac("3824F10EB8DC")

# recorder_id = create_recorder(
#     mac="3824F10EB8DC",
#     ip_public="1.54.38.138",
#     ip_lan="192.168.100.10",
#     address="CS2,LNQ,TN",
#     account="admin",
#     password="Batek@abcd",
#     port=2123
# )
# print(get_all_recorders())