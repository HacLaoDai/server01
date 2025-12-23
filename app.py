# app.py
from flask import Flask, request, jsonify
from functools import wraps
import jwt
import os

from services.task_service import CameraClient
from services.face_service import save_face_event

# ======================
# CONFIG
# ======================
JWT_SECRET = "baoan_DSFfo832f@refw1!dfsof_3312ido0f"
JWT_ALGO = "HS256"

CAMERA_IP = "192.168.100.119"
CAMERA_USER = "admin"
CAMERA_PASS = "Batek@abcd"

app = Flask(__name__)

# ======================
# JWT MIDDLEWARE
# ======================
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        # 1. Authorization header
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]

        # 2. Cookie fallback (web)
        if not token:
            token = request.cookies.get("accessToken")

        if not token:
            return jsonify({"message": "Missing token"}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper


# ======================
# ROLE CHECK
# ======================
def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            roles = request.user.get("roles", [])
            if role not in roles:
                return jsonify({"message": "Forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator


# ======================
# SET FACE
# ======================
@app.route("/api/set-face", methods=["POST"])
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

    return jsonify({
        "success": True,
        "action_by": request.user.get("phone"),
        "camera_response": resp.json()
    })


# ======================
# REMOVE FACE
# ======================
@app.route("/api/remove-face", methods=["POST"])
@jwt_required
# @require_role("admin")
def remove_face():
    body = request.get_json(silent=True) or {}

    if not body.get("face_id") or not body.get("MD5_txt"):
        return jsonify({"message": "Missing face_id or MD5_txt"}), 400

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    if not cam.login():
        return jsonify({"message": "Camera login failed"}), 500

    resp = cam.remove_face(
        face_id=body["face_id"],
        MD5=body["MD5_txt"]
    )

    return jsonify({
        "success": True,
        "action_by": request.user.get("phone"),
        "camera_response": resp.json()
    })


# ======================
# TAKE LIST
# ======================
@app.route("/api/takelist", methods=["POST"])
@jwt_required
def takelist():
    body = request.get_json(silent=True) or {}
    face_ids = body.get("face_ids", [])

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    if not cam.login():
        return jsonify({"message": "Camera login failed"}), 500

    data = cam.get_faces(face_ids)

    return jsonify({"success": True, "data": data})


# ======================
# CAMERA EVENT PUSH (PUBLIC)
# ======================
@app.route("/API/AlarmEvent/EventPush", methods=["POST"])
def event_push():
    data = request.get_json(silent=True) or {}

    face_list = (
        data.get("data", {})
            .get("ai_snap_picture", {})
            .get("FaceInfo", [])
    )

    for face in face_list:
        save_face_event(face)

    return jsonify({"status": "OK"}), 200


# ======================
# KEEP ALIVE
# ======================
@app.route("/API/HttpListening/KeepLive", methods=["POST"])
def keep_live():
    return jsonify({"status": "alive"}), 200


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2123, debug=True)
