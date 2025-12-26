from flask import Blueprint, request, jsonify
from services.auth_service import jwt_required, require_role
from models.Camera_model import CameraClient

face_api = Blueprint("face_api", __name__)

CAMERA_IP = "192.168.100.119"
CAMERA_USER = "admin"
CAMERA_PASS = "Batek@abcd"


@face_api.route("/api/set-face", methods=["POST"])
@jwt_required
@require_role("admin")
def set_face():
    body = request.get_json(silent=True) or {}
    image_b64 = body.get("image_b64")

    if not image_b64:
        return jsonify({"message": "Missing image_b64"}), 400

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    if not cam.login():
        return jsonify({"message": "Camera login failed"}), 500

    resp = cam.add_face(body)
    return jsonify({"success": True, "camera_response": resp.json()})


@face_api.route("/api/remove-face", methods=["POST"])
@jwt_required
def remove_face():
    body = request.get_json(silent=True) or {}

    if not body.get("face_id") or not body.get("MD5_txt"):
        return jsonify({"message": "Missing params"}), 400

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    cam.login()

    resp = cam.remove_face(body["face_id"], body["MD5_txt"])
    return jsonify({"success": True, "camera_response": resp.json()})
