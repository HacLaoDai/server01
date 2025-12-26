import base64
import json
import os
import re
import requests
from requests.auth import HTTPDigestAuth

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

class CameraClient:
    def __init__(self, ip, user, pwd):
        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.session = requests.Session()
        self.csrf = None
        
    def login(self):
        url = f"http://{self.ip}/API/Web/Login"
        resp = self.session.post(url, auth=HTTPDigestAuth(self.user, self.pwd))

        print(f"\nLogin: {resp.status_code} {resp.text}")
        print("Cookies:", self.session.cookies.get_dict())

        self.csrf = resp.headers.get("X-csrftoken")
        print("CSRF:", self.csrf)

        return resp.status_code == 200
    def get_images_feature(self,face_ids):
        # take information of person ()
        url = f"http://{self.ip}/API/AI/AddedFaces/GetById"
        payload = {
            "version": "1.0",
            "data": {
                "MsgId": "null",
                "FacesId": face_ids,
                "SimpleInfo": 0,
                "WithImage": 1,
                "WithFeature": 1
            }
        }
            
        print(payload)
        headers = {
            "Content-Type": "application/json",
            "X-CSRFToken": self.csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.ip}/",
            "Cookie": f"session={self.session.cookies.get('session')}; csrftoken={self.csrf}"
        }

        resp = self.session.post(url, headers=headers, json=payload)
        print("\nGetImagesFeature:", resp.status_code)
        print(resp.text)

        if resp.status_code == 200:
            return resp.json()#.get("data", [])
        return []

        
    def remove_face(self, face_id,MD5 ):
        url = f"http://{self.ip}/API/AI/Faces/Remove"

        payload = {
            "data": {
                "MsgId": "null",
                "Count": 1,
                "FaceInfo": [
                    {
                        "Id": face_id, 
                        "MD5": MD5
                    }
                    ]
                }
            }


        headers = {
            "Content-Type": "application/json",
            "X-csrftoken": self.csrf
        }
        # print("99")
        resp = self.session.post(url, headers=headers, json=payload)

        print("\nRemove Face:", resp.status_code)
        print(resp.text)

        return resp

    def add_face(self, info):
        """
        info = {
            "group_id": int,
            "name": str,
            "image": base64,
            "count": int,
            "sex": int,
            "age": int,
            "nation": str,
            "email": str,
            "phone": str
        }
        """

        url = f"http://{self.ip}/API/AI/Faces/Add"

        payload = {
            "version": "1.0",
            "data": {
                "MsgId": 0,
                "Count": info["count"],
                "FaceInfo": [
                    {
                        "Id": 0,
                        "GrpId": info["group_id"],
                        "Name": info["name"],
                        "Image1": info["image"],
                        "Image2": "",
                        "Image3": "",
                        "Sex": info["sex"],
                        "Age": info["age"],
                        "Chn": 0,
                        "ModifyCnt": 0,
                        "Similarity": 0,
                        "Time": 0,
                        "Nation": info["nation"],
                        "NativePlace": "",
                        "Job": "",
                        "Remark": "",
                        "Phone": info["phone"],
                        "Email": info["email"],
                        "IdCode": "",
                        "Country": "",
                        "EnableChnAlarm": []
                    }
                ]
            }
        }

        headers = {
            "Content-Type": "application/json",
            "X-csrftoken": self.csrf,
            "Accept": "application/json; charset=utf-8"
        }

        resp = self.session.post(url, headers=headers, data=json.dumps(payload))

        print("\nAdd Face Status:", resp.status_code)
        print("Response:", resp.text)

        return resp


# def input_and_validate():
#     while True:
#         cnt = input("Số lượng: ").strip()
#         if cnt.isdigit() and int(cnt) >= 1:
#             count = int(cnt)
#             break
#         print("Số lượng phải >= 1.")
#     while True:
#         g = input("Group ID: ").strip()
#         if g.isdigit():
#             group_id = int(g)
#             break
#         print("Group ID phải là số nguyên.")

#     while True:
#         name = input("Tên: ").strip()
#         if name:
#             break
#         print("Tên không được để trống.")
        
#     while True:
#         img_path = input("Đường dẫn ảnh: ").strip()
#         if not os.path.isfile(img_path):
#             print("File không tồn tại.")
#             continue

#         if not img_path.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".webp")):
#             print("Ảnh phải có định dạng JPG/PNG/BMP/WEBP.")
#             continue

#         try:
#             image_b64 = image_to_base64(img_path)
#             break
#         except:
#             print("Không đọc được ảnh.")

#     while True:
#         sex_in = input("Giới tính (nam/nữ): ").strip().lower()
#         if sex_in in ["nam", "n", "male"]:
#             sex = 0
#             break
#         if sex_in in ["nữ", "nu", "female"]:
#             sex = 1
#             break
#         print("Chỉ nhập nam/nữ.")
        
#     while True:
#         a = input("Tuổi: ").strip()
#         if a.isdigit():
#             age = int(a)
#             break
#         print("Tuổi phải là số.")

#     while True:
#         nation = input("Quốc tịch: ").strip()
#         if nation.replace(" ", "").isalpha():
#             break
#         print("Quốc tịch chỉ chứa chữ cái.")

#     email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
#     while True:
#         email = input("Email: ").strip()
#         if re.match(email_pattern, email):
#             break
#         print("Email không hợp lệ.")

#     phone_pattern = r"^\+?\d{9,15}$"
#     while True:
#         phone = input("Số điện thoại: ").strip()
#         if re.match(phone_pattern, phone):
#             break
#         print("Số điện thoại không hợp lệ.")

#     return {
#         "group_id": group_id,
#         "name": name,
#         "image": image_b64,
#         "count": count,
#         "sex": sex,
#         "age": age,
#         "nation": nation,
#         "email": email,
#         "phone": phone
#     }
# 
# cam = CameraClient("192.168.100.119", "admin", "Batek@abcd")

# if cam.login():
#     info = input_and_validate()
#     cam.add_face(info)
    
    
    # face_ids = list(range(0, 101))  # FaceID từ 1 → 100
    # cam.get_images_feature(group_id=5,face_ids=face_ids)
    # 
    # cam.remove_face(face_id=23,MD5="4A61DE90CEAC88CA0528BE369B9F897B")
