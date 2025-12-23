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
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME")
JWT_ALGO = "HS256"

CAMERA_IP = "192.168.100.119"
CAMERA_USER = "admin"
CAMERA_PASS = "Batek@abcd"

app = Flask(__name__)
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        token = None

        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]
        else:
            token = request.cookies.get("accessToken")

        if not token:
            return jsonify({"message": "Missing token"}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper

token = request.cookies.get("accessToken")

# ======================
# ROLE CHECK (OPTIONAL BUT NÊN CÓ)
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

    info = {
        "group_id": body.get("group_id"),
        "name": body.get("name"),
        "image": image_b64,
        "count": body.get("count", 1),
        "sex": body.get("sex", 0),
        "age": body.get("age", 0),
        "nation": body.get("nation", "VN"),
        "email": body.get("email", ""),
        "phone": body.get("phone", "")
    }

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    if not cam.login():
        return jsonify({"message": "Camera login failed"}), 500

    resp = cam.add_face(info)

    return jsonify({
        "success": True,
        "action_by": request.user.get("email"),
        "camera_response": resp.json()
    })


# ======================
# REMOVE FACE
# ======================
@app.route("/api/remove-face", methods=["POST"])
@jwt_required
@require_role("admin")
def remove_face():
    body = request.get_json(silent=True) or {}

    md5_txt = body.get("MD5_txt")
    face_id = body.get("face_id")

    if not md5_txt or not face_id:
        return jsonify({"message": "Missing MD5_txt or face_id"}), 400

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    if not cam.login():
        return jsonify({"message": "Camera login failed"}), 500

    resp = cam.remove_face(face_id=face_id, MD5=md5_txt)

    return jsonify({
        "success": True,
        "action_by": request.user.get("email"),
        "camera_response": resp.json()
    })


# ======================
# TAKE LIST (GET FACE INFO)
# ======================
@app.route("/api/takelist", methods=["POST"])
@jwt_required
def takelist():
    body = request.get_json(silent=True) or {}

    face_ids = body.get("face_ids")
    if not isinstance(face_ids, list):
        return jsonify({"message": "face_ids must be a list"}), 400

    cam = CameraClient(CAMERA_IP, CAMERA_USER, CAMERA_PASS)
    if not cam.login():
        return jsonify({"message": "Camera login failed"}), 500

    data = cam.get_faces(face_ids)

    return jsonify({
        "success": True,
        "data": data
    })


# ======================
# CAMERA EVENT PUSH (NO AUTH)
# ======================
@app.route("/API/AlarmEvent/EventPush", methods=["POST"])
def event_push():
    data = request.get_json(silent=True) or {}
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


# ======================
# CAMERA KEEP ALIVE
# ======================
@app.route("/API/HttpListening/KeepLive", methods=["POST"])
def keep_live():
    print("=== KEEPALIVE RECEIVED ===")
    print(request.get_data(as_text=True))
    return jsonify({"status": "alive"}), 200


# ======================
# RUN
# ======================
if __name__ == "__main__":
    app.run(
        host="192.168.100.80",
        port=2123,
        debug=True
    )
