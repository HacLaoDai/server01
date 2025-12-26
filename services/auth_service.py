from functools import wraps
from flask import request, jsonify
import jwt

JWT_SECRET = "baoan_DSFfo832f@refw1!dfsof_3312ido0f"
JWT_ALGO = "HS256"


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None

        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            token = auth.split(" ", 1)[1]

        if not token:
            token = request.cookies.get("accessToken")

        if not token:
            return jsonify({"message": "Missing token"}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper


def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            roles = request.user.get("roles", [])
            if role not in roles:
                return jsonify({"message": "Forbidden"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
