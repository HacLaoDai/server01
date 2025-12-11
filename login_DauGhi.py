import base64
import json
import requests
from requests.auth import HTTPDigestAuth

class CameraClient:
    def __init__(self, ip, user, pwd):
        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.session = requests.Session()
        self.csrf = None

    def login(self):
        url = f"http://{self.ip}/API/Web/Login"
        r = self.session.post(url, auth=HTTPDigestAuth(self.user, self.pwd))

        print("Login:", r.status_code, r.text)

        # Cookie
        print("Cookies:", self.session.cookies.get_dict())

        # CSRF
        self.csrf = r.headers.get("X-csrftoken")
        print("CSRF:", self.csrf)
        

    def add_face(self, img_path, name="user", group_id=5):
        url = f"http://{self.ip}/API/AI/Faces/Add"

        # Đọc ảnh → base64
        with open(img_path, "rb") as f:
            b64_image = base64.b64encode(f.read()).decode()

        payload = {
                "version": "1.0",
                "data": {
                    "MsgId": 0,
                    "Count": 1,
                    "FaceInfo": [
                        {
                            "Id": 0,
                            "GrpId": group_id,
                            "Name": name,
                            "Image1": b64_image,
                            "Image2": "",
                            "Image3": "",
                            "Sex": 0,
                            "Age": 0,
                            "Chn": 0,
                            "ModifyCnt": 0,
                            "Similarity": 0,
                            "Time": 0,
                            "Nation": "",
                            "NativePlace": "",
                            "Job": "",
                            "Remark": "",
                            "Phone": "",
                            "Email": "",
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

        print("Add Face Status:", resp.status_code)
        print("Response:", resp.text)

        return resp


# =========== TEST =============

cam = CameraClient("192.168.100.119", "admin", "Batek@abcd")
cam.login()

cam.add_face("khiem.jpg", name="khiem", group_id=5)
