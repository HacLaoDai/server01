import base64
import json
import os
import re
import requests
from requests.auth import HTTPDigestAuth

path_log = "log_server1.txt"

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
    def get_images_feature(self, group_id, person_id=None):
        # take number of list person        
        url = f"http://{self.ip}/API/AI/AddedFaces/Search"
        payload = {"version":"1.0","data":{"MsgId":"null","FaceInfo":[{"GrpId":5}]}}
        
        # take id person_id  (empty error)
        url = f"http://{self.ip}/API/AI/AddedFaces/GetByIndex"
        payload = {"version":"1.0","data":{"MsgId":None,"GrpId": group_id,"StartIndex":0,"Count":4,"SimpleInfo":1,"WithImage":0,"WithFeature":0}}
        
        # take information of person ()
        # url = f"http://{self.ip}/API/AI/AddedFaces/GetById"	
        # payload ={"version":"1.0","data":{"MsgId":"null","FacesId":[2,3,14,16],"SimpleInfo":0,"WithImage":1,"WithFeature":1}}
        
        if person_id:
            payload["PersonID"] = person_id
        print(payload)
        headers = {
            "Content-Type": "application/json",
            "X-csrftoken": self.csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"http://{self.ip}/"
        }


        resp = self.session.post(url, headers=headers, json=payload)
        with open(path_log,'+w') as w:
            w.write(resp.text)
        print("\nGetImagesFeature:", resp.status_code)
        print(resp.text)

        if resp.status_code == 200:
            return resp.json()#.get("data", [])
        return []

        
    def remove_face(self, group_id, face_id=None, person_id=None):
        url = f"http://{self.ip}/API/AI/Face/Remove"

        payload = {
            "GrpId": group_id
        }

        if face_id:
            payload["FaceID"] = face_id

        if person_id:
            payload["PersonID"] = person_id

        headers = {
            "Content-Type": "application/json",
            "X-csrftoken": self.csrf
        }

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


# cam = CameraClient("192.168.100.119", "admin", "Batek@abcd")

# if cam.login():
    # info = input_and_validate()
    # cam.add_face(info)
    # cam.get_images_feature(group_id=5)
