from models.Camera_model import CameraClient
from utils.image import image_to_base64
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os
import base64

base_folder = "/home/lychien/Desktop/Cam_cty"

def set_face_service(req):
    # 1. Convert image
    image_b64 = image_to_base64(req.image)

    # 2. Chuẩn hóa info cho đầu ghi
    info = {
        "group_id": req.group_id,
        "name": req.name,
        "image": image_b64,
        "count": req.count,
        "sex": req.sex,
        "age": req.age,
        "nation": req.nation,
        "email": req.email,
        "phone": req.phone
    }

    # 3. Login đầu ghi
    cam = CameraClient(
        ip="192.168.100.119",
        user="admin",
        pwd="Batek@abcd"
    )

    if not cam.login():
        raise Exception("Login camera failed")

    # 4. Add face
    resp = cam.add_face(info)

    if resp.status_code != 200:
        raise Exception(resp.text)

    return resp.json()
def timestamp_to_vn(ts):
    try:
        dt = datetime.fromtimestamp(ts) - timedelta(hours=7)
        return dt
    except:
        return datetime.now()
def save_known_face_event(face,nvr_info):
    
    start_ts = face.get("StartTime", datetime.now().timestamp()) #- 3600*7
    end_ts   = face.get("EndTime", start_ts) #- 3600*7

    start_vn = timestamp_to_vn(start_ts)
    end_vn   = timestamp_to_vn(end_ts)

    date_folder = os.path.join(base_folder, start_vn.strftime("%Y-%m-%d"))
    os.makedirs(date_folder, exist_ok=True)

    name = face.get("Name", "unknown").strip()
    if not name:
        name = "unknown"
    Phone = face.get("Phone")
    Email = face.get("Email")
    channel = face.get("StrChn")
    MD5_img = face.get("MD5")
    nvr_info = nvr_info or {}

    nvr_ip  = nvr_info.get("ip", "")
    nvr_mac = nvr_info.get("mac", "")
    nvr_phy = nvr_info.get("phy", "")

    print("KNOWN:", name)

    name_folder = os.path.join(date_folder, name)
    os.makedirs(name_folder, exist_ok=True)

    log_path = os.path.join(name_folder, f"{name}.txt")
    first_time = not os.path.exists(log_path)

    if first_time:
        info_text = (
            f"Name: {name}\n"
            f"GrpId: {face.get('GrpId', '')}\n"
            f"StartTime: {start_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"EndTime: {end_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"SDT: {Phone}\n"
            f"Email: {Email}\n"
            f"Channel: {channel}\n"
            f"MD5: {MD5_img}\n"
            f"NVR_IP: {nvr_ip}\n"
            f"NVR_MAC: {nvr_mac}\n"
            f"NVR_PHY: {nvr_phy}\n"
        )
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(info_text)
    else:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("EndTime:"):
                lines[i] = f"EndTime: {end_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"

        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    # Ảnh đầu
    if first_time and "Image1" in face and len(face["Image1"]) > 50:
        try:
            img1_path = os.path.join(name_folder, f"{name}_Image1.jpg")
            with open(img1_path, "wb") as f:
                f.write(base64.b64decode(face["Image1"]))
        except Exception as e:
            print("Error saving Image1:", e)

    # Ảnh cuối
    if "Image4" in face and len(face["Image4"]) > 50:
        try:
            img4_path = os.path.join(
                name_folder,
                f"{name}_Image4_{end_vn.strftime('%H%M%S')}.jpg"
            )
            with open(img4_path, "wb") as f:
                f.write(base64.b64decode(face["Image4"]))
        except Exception as e:
            print("Error saving Image4:", e)

def save_stranger_face_event(face,nvr_info):
    start_ts = face.get("StartTime", datetime.now().timestamp()) #- 3600*7
    end_ts   = face.get("EndTime", start_ts) #- 3600*7

    start_vn = timestamp_to_vn(start_ts)
    end_vn   = timestamp_to_vn(end_ts)

    date_folder = os.path.join(base_folder, start_vn.strftime("%Y-%m-%d"))
    stranger_folder = os.path.join(date_folder, "Nguoi_la")
    os.makedirs(stranger_folder, exist_ok=True)

    snap_id = face.get("SnapId", "unknown")
    print("STRANGER SnapId:", snap_id)
    nvr_info = nvr_info or {}

    nvr_ip  = nvr_info.get("ip", "")
    nvr_mac = nvr_info.get("mac", "")
    nvr_phy = nvr_info.get("phy", "")

    log_path = os.path.join(
        stranger_folder,
        f"{start_vn.strftime('%H%M%S')}_Snap{snap_id}.txt"
    )

    info_text = (
        "Name: Nguoi_la\n"
        f"GrpId: {face.get('GrpId', '')}\n"
        f"SnapId: {snap_id}\n"
        f"StartTime: {start_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"EndTime: {end_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"NVR_IP: {nvr_ip}\n"
        f"NVR_MAC: {nvr_mac}\n"
        f"NVR_PHY: {nvr_phy}\n"
    )

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(info_text)

    # Ảnh đầu (Image1 hoặc Image2)
    image_first = face.get("Image1") or face.get("Image2")
    if image_first and len(image_first) > 50:
        try:
            img_path = os.path.join(
                stranger_folder,
                f"{start_vn.strftime('%H%M%S')}_Snap{snap_id}_first.jpg"
            )
            with open(img_path, "wb") as f:
                f.write(base64.b64decode(image_first))
        except Exception as e:
            print("Error saving stranger first image:", e)

    # Ảnh cuối
    if "Image4" in face and len(face["Image4"]) > 50:
        try:
            img_path = os.path.join(
                stranger_folder,
                f"{end_vn.strftime('%H%M%S')}_Snap{snap_id}_last.jpg"
            )
            with open(img_path, "wb") as f:
                f.write(base64.b64decode(face["Image4"]))
        except Exception as e:
            print("Error saving stranger last image:", e)
def save_face_event(face, nvr_info=None):
    name = face.get("Name", "").strip()
    face_id = face.get("Id")

    if not name or face_id == -1:
        save_stranger_face_event(face,nvr_info)
    else:
        save_known_face_event(face,nvr_info)
