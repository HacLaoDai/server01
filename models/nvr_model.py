import requests, uuid
from config import NVR

def add_face(group_id, name, image_path, **extra):
    url = f"http://{NVR['ip']}:{NVR['port']}/API/AI/AddedFaces"

    person_id = str(uuid.uuid4())

    face = {
        "GrpId": group_id,
        "PersonId": person_id,
        "Name": name
    }

    if extra.get("sex") is not None:
        face["Gender"] = extra["sex"]
    if extra.get("age") is not None:
        face["Age"] = extra["age"]

    payload = {
        "version": "1.0",
        "data": {"FaceInfo": [face]}
    }

    with open(image_path, "rb") as img:
        files = {"image": img}
        r = requests.post(
            url,
            data={"json": str(payload)},
            files=files,
            auth=(NVR["user"], NVR["password"]),
            timeout=10
        )

    return {
        "person_id": person_id,
        "status": r.status_code,
        "response": r.text
    }
