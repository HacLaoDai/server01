from datetime import datetime
from bson import ObjectId
from database.task_db import TaskDB

# =========================
# COLLECTION
# =========================

face_events = TaskDB.face_events

# =========================
# CREATE
# =========================
def create_face_event(data: dict):
    data["created_at"] = datetime.utcnow()
    return face_events.insert_one(data).inserted_id


# =========================
# READ
# =========================
def get_all_face_events(limit=100):
    return list(
        face_events.find({})
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


def get_face_events_by_time(start: datetime, end: datetime):
    return list(
        face_events.find({
            "time_in": {
                "$gte": start,
                "$lte": end
            }
        }).sort("time_in", -1)
    )


def get_face_events_by_channel(channel: str, limit=50):
    return list(
        face_events.find({"channel": channel})
        .sort("time_in", -1)
        .limit(limit)
    )


def get_face_event_by_id(event_id: str):
    return face_events.find_one(
        {"_id": ObjectId(event_id)}
    )


# =========================
# UPDATE
# =========================
def update_face_event(event_id: str, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()

    result = face_events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": update_data}
    )
    return result.modified_count


def update_face_events_by_person(person_id: int, update_data: dict):
    update_data["updated_at"] = datetime.utcnow()

    result = face_events.update_many(
        {"person_id": person_id},
        {"$set": update_data}
    )
    return result.modified_count


# =========================
# DELETE
# =========================
def delete_face_event(event_id: str):
    result = face_events.delete_one(
        {"_id": ObjectId(event_id)}
    )
    return result.deleted_count


def delete_unknown_faces():
    result = face_events.delete_many(
        {"person_id": -1}
    )
    return result.deleted_count


def delete_face_events_by_time(start: datetime, end: datetime):
    result = face_events.delete_many({
        "time_in": {
            "$gte": start,
            "$lte": end
        }
    })
    return result.deleted_count


def delete_face_events_by_channel(channel: str):
    result = face_events.delete_many(
        {"channel": channel}
    )
    return result.deleted_count


# from services.face_data import *

# events = get_unknown_faces(10)
# print(events)

# update_face_event(
#     event_id="65a1c9f3...",
#     update_data={"name": "Nguyễn Văn A", "person_id": 12}
# )

# delete_unknown_faces()
# from services.face_data import (
#     get_all_face_events,
#     get_unknown_faces
# )

# events = get_all_face_events(100)
# print("=== ALL ===")
# for e in events:
#     print(e["name"], e["time_in"])

# unknowns = get_unknown_faces()
# print("\n=== UNKNOWN ===")
# for u in unknowns:
#     print(u["time_in"])
