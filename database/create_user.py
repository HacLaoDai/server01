# create_user.py
import bcrypt
from db import users_col

password = bcrypt.hashpw(b"123456a@", bcrypt.gensalt())

users_col.insert_one({
    "email": "nguyenanh123@gmail.com",
    "phone": "0388123456",
    "password": password,
    "roles": ["admin"]
})

print("User created")
