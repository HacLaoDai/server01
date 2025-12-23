import requests
import base64
import os

API_URL = "http://192.168.100.80:2123/api/internal/set-face"

image_path = "/home/lychien/Downloads/khiem.jpg"  # đổi path nếu chạy Windows

# --- check ảnh ---
if not os.path.isfile(image_path):
    raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")

# --- convert ảnh → base64 ---
with open(image_path, "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode("utf-8")


payload = {
    "group_id": 5,
    "name": "Nguyen Anh",
    "image": image_b64,   # nếu API của bạn tự đọc path
    # hoặc nếu API nhận base64 thì đổi thành:
    # "image": image_b64,
    "count": 1,
    "sex": 0,
    "age": 25,
    "nation": "VN",
    "email": "nguyenanh123@gmail.com",
    "phone": "0388123456"
}

headers = {
    "Content-Type": "application/json"
}

resp = requests.post(API_URL, json=payload, headers=headers, timeout=10)

print("Status:", resp.status_code)
print("Response:", resp.text)
