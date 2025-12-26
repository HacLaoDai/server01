from flask import Flask
from controllers.face_controller import face_api
from controllers.camera_controller import camera_event_api

app = Flask(__name__)

# register routes
app.register_blueprint(face_api)
app.register_blueprint(camera_event_api)

if __name__ == "__main__":
    app.run(host="192.168.100.94", port=2123, debug=False)
