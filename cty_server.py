from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os
import base64

app = Flask(__name__)
base_folder = "/home/lychien/Desktop/Cam_cty"

def timestamp_to_vn(ts):
    """Đơn giản: trừ 7h để về giờ Việt Nam"""
    try:
        dt = datetime.fromtimestamp(ts) - timedelta(hours=7)
        return dt
    except:
        return datetime.now()

def save_face_event(face):
    start_ts = face.get("StartTime", datetime.now().timestamp())
    end_ts = face.get("EndTime", start_ts)
    start_time_vn = timestamp_to_vn(start_ts)
    end_time_vn = timestamp_to_vn(end_ts)

    # Folder theo ngày
    date_folder = os.path.join(base_folder, start_time_vn.strftime("%Y-%m-%d"))
    os.makedirs(date_folder, exist_ok=True)

    # Folder theo tên người
    name = face.get("Name", "unknown")
    name_folder = os.path.join(date_folder, name)
    os.makedirs(name_folder, exist_ok=True)

    # Log file tên mặc định là Name.txt
    log_file_path = os.path.join(name_folder, f"{name}.txt")

    # Nếu log chưa tồn tại → tạo mới
    if not os.path.exists(log_file_path):
        info_text = (
            f"Name: {name}\n"
            f"GrpId: {face.get('GrpId', '')}\n"
            f"StartTime: {start_time_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"EndTime: {end_time_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write(info_text)
    else:
        # Nếu log đã tồn tại → chỉ cập nhật EndTime
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("EndTime:"):
                lines[i] = f"EndTime: {end_time_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    # Lưu ảnh
    # Image1: lưu 1 lần duy nhất
    img1_path = os.path.join(name_folder, f"{name}_Image1.jpg")
    if "Image1" in face and not os.path.exists(img1_path):
        try:
            img_bytes = base64.b64decode(face["Image1"])
            with open(img1_path, "wb") as f:
                f.write(img_bytes)
        except Exception as e:
            print(f"Failed Image1 for {name}: {e}")

    # Image4: lần đầu lưu time in, sau đó lưu time out
   # Image4: lần đầu lưu time in, sau đó lưu time out
    if "Image4" in face:
        # Tìm tất cả file Image4 trong folder
        all_img4_files = [f for f in os.listdir(name_folder) if f.startswith(f"{name}_Image4")]
        
        # Kiểm tra có file "in" chưa
        has_in = any("_in_" in f for f in all_img4_files)
        
        if not has_in:
            # Lần đầu: lưu time in
            img4_path = os.path.join(name_folder, f"{name}_Image4_in_{start_time_vn.strftime('%H%M%S')}.jpg")
        else:
            # Lần sau: lưu time out
            # Xóa file Image4_out cũ nếu có
            for f in all_img4_files:
                if "_out_" in f:
                    try:
                        os.remove(os.path.join(name_folder, f))
                    except Exception as e:
                        print(f"Failed to remove old Image4_out: {e}")
            img4_path = os.path.join(name_folder, f"{name}_Image4_out_{end_time_vn.strftime('%H%M%S')}.jpg")
        
        # Lưu ảnh mới
        try:
            img_bytes = base64.b64decode(face["Image4"])
            with open(img4_path, "wb") as f:
                f.write(img_bytes)
        except Exception as e:
            print(f"Failed Image4 for {name}: {e}")


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
    app.run(host="0.0.0.0", port=5050)
