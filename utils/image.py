import base64
import os

def image_to_base64(path):
    if not os.path.exists(path):
        raise Exception("Image not found")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
