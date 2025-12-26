from flask import Blueprint, request, jsonify
from services.face_service import save_face_event
from database.task_db import save_face_to_db

camera_event_api = Blueprint("camera_event_api", __name__)


@camera_event_api.route("/API/AlarmEvent/EventPush", methods=["POST"])
def event_push():
    data = request.get_json(silent=True) or {}

    face_list = (
        data.get("data", {})
        .get("ai_snap_picture", {})
        .get("FaceInfo", [])
    )

    dev_net_info = data.get("data", {}).get("dev_net_info", [])
    nvr_info = dev_net_info[0] if dev_net_info else {}

    for face in face_list:
        save_face_event(face, nvr_info)

        save_face_to_db(face)

    return jsonify({"status": "OK"}), 200


@camera_event_api.route("/API/HttpListening/KeepLive", methods=["POST"])
def keep_live():
    return jsonify({"status": "alive"}), 200
