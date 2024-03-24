from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user")
}

roles = { "admin": list("admin"), "user": list("user") }

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        logging.info(f"User {username} has been authenticated")
        return username
    

@auth.get_user_roles
def get_user_roles(user):
    return roles.get(user)
