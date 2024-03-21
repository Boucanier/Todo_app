from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import logging

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "noob": generate_password_hash("noob")
}

roles = { "admin": "admin", "noob": "noob" }

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        logging.info(f"User {username} has been authenticated")
        auth.current_user = dict()
        auth.current_user['role'] = roles[username]
        auth.current_user['username'] = username
        return username