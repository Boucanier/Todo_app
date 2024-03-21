from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import logging

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "noob": generate_password_hash("noob")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        logging.info(f"User {username} has been authenticated")
        return username