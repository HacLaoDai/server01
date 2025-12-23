from flask import Blueprint, request, jsonify
from services.face_service import save_face_event

api_bp = Blueprint("api", __name__)

@api_bp.route("/API/AlarmEvent/EventPush", methods=["POST"])
def event_push():
    data = request.get_json(force=True, silent=True) or {}

    print("=== EVENT RECEIVED ===")
    print(data)

    face_list = (
        data.get("data", {})
            .get("ai_snap_picture", {})
            .get("FaceInfo", [])
    )

    for face in face_list:
        save_face_event(face)

    return jsonify({"status": "OK"}), 200


@api_bp.route("/API/HttpListening/KeepLive", methods=["POST"])
def keep_live():
    print("=== KEEPALIVE RECEIVED ===")
    print(request.get_data(as_text=True))
    return jsonify({"status": "alive"}), 200
