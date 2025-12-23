import jwt
import os
from flask import abort

JWT_SECRET = os.getenv("JWT_SECRET")

def verify_jwt_token(auth_header):
    if not auth_header or not auth_header.startswith("Bearer "):
        abort(401, "Missing token")

    token = auth_header.split(" ")[1]

    try:
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")
