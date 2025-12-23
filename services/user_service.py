from database.mongo import get_db

db = get_db()
users_col = db["users"]

def find_user(username):
    return users_col.find_one({"username": username})

def create_user(username, password_hash, role="user"):
    users_col.insert_one({
        "username": username,
        "password": password_hash,
        "role": role
    })
