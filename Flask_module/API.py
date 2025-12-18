from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from Client.img.SaveFace import save_face_event

app = Flask(__name__)
@app.route("/API/AlarmEvent/EventPush", methods=["POST"])
def event_push():
    data = request.json
    print("=== EVENT RECEIVED ===")
    print(data)

    face_list = data.get("data", {}).get("ai_snap_picture", {}).get("FaceInfo", [])
    for face in face_list:
        save_face_event(face)

    return jsonify({"status": "OK"}), 200


@app.route("/API/HttpListening/KeepLive", methods=["POST"])
def keep_live():
    print("=== KEEPALIVE RECEIVED ===")
    print(request.get_data(as_text=True))
    return jsonify({"status": "alive"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2123)
