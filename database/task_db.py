import os
from pymongo import MongoClient

from datetime import datetime
from bson import ObjectId
import base64
from io import BytesIO
from PIL import ImageDraw, ImageFont,Image
import matplotlib.pyplot as plt
import math
# ======================================================
# CONNECT MONGODB
# ======================================================
URI= "mongodb://baoan_dev:5769boan20s12rui@103.159.51.61/baoan_dev"
client = MongoClient(URI)
db = client.get_default_database()
# ======================================================
# COLLECTIONS
# ======================================================
users = db["users"]
face_events = db["face_events"]
recorders = db["recorders"]
cameras = db["cameras"]

# ======================================================
# INDEXES
# ======================================================
recorders.create_index("mac", unique=True)
cameras.create_index("serial", unique=True)
cameras.create_index("recorder_id")
face_events.create_index("time_in")
face_events.create_index("person_id")

# ======================================================
# USERS
# ======================================================
def get_all_users():
    return list(users.find({}))


# ======================================================
# FACE EVENTS
# ======================================================
def save_face_to_db(face: dict):
    person_id = face.get("Id", -1)
    is_unknown = person_id == -1 or not face.get("Name")

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

        "time_in": datetime.fromtimestamp(face.get("StartTime") - 3600 * 7),
        "time_out": datetime.fromtimestamp(face.get("EndTime") - 3600 * 7),

        "image1": face.get("Image1") if not is_unknown else None,
        "image2": face.get("Image2"),
        "image4": face.get("Image4"),

        "created_at": datetime.utcnow()
    }

    return face_events.insert_one(doc).inserted_id


def get_face_event_by_id(event_id: str):
    return face_events.find_one({"_id": ObjectId(event_id)})


def get_face_events(limit=100):
    return list(
        face_events.find({})
        .sort("time_in", -1)
        .limit(limit)
    )
def get_all_face_events_simple(limit=100):
    events = face_events.find(
        {},
        {
            "_id": 0,
            "person_id": 1,
            "name": 1,
            "time_in": 1,
            "time_out": 1
        }
    ).sort("time_in", -1).limit(limit)

    result = []
    for e in events:
        name = e.get("name") if e.get("person_id") != -1 else "Người lạ"

        result.append({
            "name": name,
            "time_in": e.get("time_in"),
            "time_out": e.get("time_out")
        })

    return result
def get_face_events_simple(limit=50):
    return list(
        face_events.find(
            {},
            {
                "_id": 0,
                "name": 1,
                "time_in": 1,
                "time_out": 1,
                "image2": 1
            }
        )
        .sort("time_in", -1)
        .limit(limit)
    )


def get_face_events_by_person(person_id, limit=50):
    return list(
        face_events.find({"person_id": person_id})
        .sort("time_in", -1)
        .limit(limit)
    )


def get_unknown_faces(limit=50):
    return list(
        face_events.find({"person_id": -1})
        .sort("time_in", -1)
        .limit(limit)
    )


def update_face_event(event_id: str, data: dict):
    return face_events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": data}
    )


def delete_face_event(event_id: str):
    return face_events.delete_one(
        {"_id": ObjectId(event_id)}
    )


def delete_face_events_by_person(person_id):
    return face_events.delete_many(
        {"person_id": person_id}
    )


# ======================================================
# RECORDERS
# ======================================================
# recorder_id = create_recorder(
#     mac="3824F10EB8DC",
#     ip_public="1.54.38.138",
#     ip_lan="192.168.100.10",
#     address="CS2,LNQ,TN",
#     account="admin",
#     password="Batek@abcd",
#     port=2123
# )

def get_recorder_by_id(recorder_id):
    return recorders.find_one({"_id": ObjectId(recorder_id)})


def get_recorder_by_mac(mac: str):
    return recorders.find_one({"mac": mac})


def get_all_recorders():
    return list(recorders.find({}))


def update_recorder(recorder_id, data: dict):
    return recorders.update_one(
        {"_id": ObjectId(recorder_id)},
        {"$set": data}
    )


def delete_recorder(recorder_id):
    cameras.delete_many({"recorder_id": ObjectId(recorder_id)})
    return recorders.delete_one(
        {"_id": ObjectId(recorder_id)}
    )


# ======================================================
# CAMERAS
# ======================================================
# create_camera(
#     serial="CAM_01",
#     ip="192.168.100.89",
#     channel="CH1",
#     is_in=True,
#     status=True,
#     recorder_id=recorder_id
# )


def get_camera_by_id(camera_id):
    return cameras.find_one({"_id": ObjectId(camera_id)})


def get_camera_by_serial(serial: str):
    return cameras.find_one({"serial": serial})


def get_cameras_by_recorder(recorder_id):
    return list(
        cameras.find({"recorder_id": ObjectId(recorder_id)})
    )


def get_all_cameras():
    return list(cameras.find({}))


def update_camera(camera_id, data: dict):
    return cameras.update_one(
        {"_id": ObjectId(camera_id)},
        {"$set": data}
    )


def delete_camera(camera_id):
    return cameras.delete_one(
        {"_id": ObjectId(camera_id)}
    )


def get_cameras_with_recorder():
    pipeline = [
        {
            "$lookup": {
                "from": "recorders",
                "localField": "recorder_id",
                "foreignField": "_id",
                "as": "recorder"
            }
        },
        {"$unwind": "$recorder"}
    ]

    return list(cameras.aggregate(pipeline))

def deletl_all(db):
    db.cameras.delete_many({})
    db.recorders.delete_many({})
# show

def base64_to_pil(base64_str):
    img_bytes = base64.b64decode(base64_str)
    return Image.open(BytesIO(img_bytes)).convert("RGB")


def draw_info_on_image(img, name, time_in):
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        font = ImageFont.load_default()

    text = f"{name} | {time_in.strftime('%Y-%m-%d %H:%M:%S')}"
    
    draw.rectangle((0, 0, img.width, 40), fill=(0, 0, 0))
    draw.text((10, 8), text, fill=(255, 255, 255), font=font)

    return img



def show_face_images(events, cols=4):
    rows = math.ceil(len(events) / cols)
    plt.figure(figsize=(cols * 4, rows * 4))

    for i, ev in enumerate(events):
        img = base64_to_pil(ev["image2"])
        img = draw_info_on_image(
            img,
            ev.get("name", "Unknown"),
            ev["time_in"]
        )

        plt.subplot(rows, cols, i + 1)
        plt.imshow(img)
        plt.axis("off")

    plt.tight_layout()
    plt.show()
    
# events = get_face_events_simple(limit=20)
# # print(events)
# show_face_images(events)


    # print("✅ Đã xóa toàn bộ dữ liệu trong cameras & recorders")
    
# events = get_all_face_events_simple()

# print(f"=== ALL {len(events)}===")
# for e in events:
#     print(e["name"], e["time_in"])
