import os
import re
from .utils import image_to_base64
def input_and_validate1():
    while True:
        cnt = input("Số lượng: ").strip()
        if cnt.isdigit() and int(cnt) >= 1:
            count = int(cnt)
            break
        print("Số lượng phải >= 1.")
    while True:
        g = input("Group ID: ").strip()
        if g.isdigit():
            group_id = int(g)
            break
        print("Group ID phải là số nguyên.")

    while True:
        name = input("Tên: ").strip()
        if name:
            break
        print("Tên không được để trống.")
        
    while True:
        img_path = input("Đường dẫn ảnh: ").strip()
        if not os.path.isfile(img_path):
            print("File không tồn tại.")
            continue

        if not img_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp")):
            print("Ảnh phải có định dạng JPG/PNG/BMP/WEBP.")
            continue

        try:
            image_b64 = image_to_base64(img_path)
            break
        except:
            print("Không đọc được ảnh.")

    while True:
        sex_in = input("Giới tính (nam/nữ): ").strip().lower()
        if sex_in in ["nam", "n", "male"]:
            sex = 0
            break
        if sex_in in ["nữ", "nu", "female"]:
            sex = 1
            break
        print("Chỉ nhập nam/nữ.")
        
    while True:
        a = input("Tuổi: ").strip()
        if a.isdigit():
            age = int(a)
            break
        print("Tuổi phải là số.")

    while True:
        nation = input("Quốc tịch: ").strip()
        if nation.replace(" ", "").isalpha():
            break
        print("Quốc tịch chỉ chứa chữ cái.")

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    while True:
        email = input("Email: ").strip()
        if re.match(email_pattern, email):
            break
        print("Email không hợp lệ.")

    phone_pattern = r"^\+?\d{9,15}$"
    while True:
        phone = input("Số điện thoại: ").strip()
        if re.match(phone_pattern, phone):
            break
        print("Số điện thoại không hợp lệ.")

    return {
        "group_id": group_id,
        "name": name,
        "image": image_b64,
        "count": count,
        "sex": sex,
        "age": age,
        "nation": nation,
        "email": email,
        "phone": phone
    }
