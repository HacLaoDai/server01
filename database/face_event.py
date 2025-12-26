from pymongo import MongoClient
from datetime import datetime
import os

MONGODB_URI = "mongodb://baoan_dev:5769boan20s12rui@103.159.51.61/baoan_dev"

client = MongoClient(MONGODB_URI)
db = client.get_default_database()

face_events = db["face_events"]


def save_face_to_db(face: dict):
    """
    Lưu 1 FaceInfo vào MongoDB
    - Người lạ: Id = -1, Name = 'Người lạ'
    - Nhân viên: lấy đầy đủ thông tin
    """

    person_id = face.get("Id", -1)

    is_unknown = (
        person_id == -1
        or not face.get("Name")
    )

    doc = {
        "person_id": person_id if not is_unknown else -1,
        "grp_id": face.get("GrpId"),
        "name": face.get("Name") if not is_unknown else "Người lạ",
        "md5": face.get("MD5", ""),
        "channel": face.get("StrChn"),

        "sex": face.get("Sex"),
        "age": face.get("Age"),
        "gender": face.get("Gender"),

        "country": face.get("Country", ""),
        "nation": face.get("Nation", ""),
        "native_place": face.get("NativePlace", ""),
        "job": face.get("Job", ""),
        "phone": face.get("Phone", ""),
        "email": face.get("Email", ""),

        "time_in": datetime.fromtimestamp(face.get("StartTime")-3600*7),
        "time_out": datetime.fromtimestamp(face.get("EndTime")-3600*7),

        # Ảnh
        "image1": face.get("Image1") if not is_unknown else None,
        "image2": face.get("Image2"),
        "image4": face.get("Image4"),

        "created_at": datetime.utcnow()
    }

    return face_events.insert_one(doc).inserted_id
