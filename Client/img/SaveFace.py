from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import os
import base64

base_folder = "/home/lychien/Desktop/Cam_cty"

def timestamp_to_vn(ts):
    return datetime.utcfromtimestamp(ts) + timedelta(hours=7)

def save_face_event(face):

    start_ts = face.get("StartTime", datetime.now().timestamp())-3600*7
    end_ts   = face.get("EndTime", start_ts)-3600*7

    start_vn = timestamp_to_vn(start_ts)
    end_vn   = timestamp_to_vn(end_ts)

    date_folder = os.path.join(base_folder, start_vn.strftime("%Y-%m-%d"))
    os.makedirs(date_folder, exist_ok=True)

    name = face.get("Name", "unknown")
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
        )
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(info_text)

    else:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Update EndTime
        for i, line in enumerate(lines):
            if line.startswith("EndTime:"):
                lines[i] = f"EndTime: {end_vn.strftime('%Y-%m-%d %H:%M:%S')}\n"

        with open(log_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    if first_time:
        if "Image1" in face and len(face["Image1"]) > 50:
            try:
                img1_path = os.path.join(name_folder, f"{name}_Image1.jpg")
                with open(img1_path, "wb") as f:
                    f.write(base64.b64decode(face["Image1"]))
            except Exception as e:
                print("Error saving Image1:", e)

    if "Image4" in face and len(face["Image4"]) > 50:

        img4_path = os.path.join(
            name_folder, 
            f"{name}_Image4_{end_vn.strftime('%H%M%S')}.jpg"
        )

        try:
            with open(img4_path, "wb") as f:
                f.write(base64.b64decode(face["Image4"]))
        except Exception as e:
            print("Error saving Image4:", e)
