import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId

# CONNECT DB
MONGODB_URI = "mongodb://baoan_dev:5769boan20s12rui@103.159.51.61/baoan_dev"

client = MongoClient(MONGODB_URI)
db = client.get_default_database()

cameras = db["cameras"]

# INIT INDEX
cameras.create_index("serial", unique=True)
cameras.create_index("recorder_id")


# CREATE
def create_camera(
    serial: str,
    ip: str,
    channel: str,
    is_in: bool,
    status: bool,
    recorder_id
):
    data = {
        "serial": serial,
        "ip": ip,
        "channel": channel,
        "is_in": is_in,          # chuẩn snake_case
        "status": status,
        "recorder_id": ObjectId(recorder_id),
        "created_at": datetime.utcnow()
    }

    return cameras.insert_one(data).inserted_id



# data = get_cameras_with_recorder()
# for d in data:
#     print(d["serial"], d["recorder"]["ip_lan"])

# delete_camera_by_serial("CAM_01")

# update_camera_by_serial(
#     "CAM_01",
#     {"status": False}
# )
