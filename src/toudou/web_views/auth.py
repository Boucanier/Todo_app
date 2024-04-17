"""
    This module contains the authentication elements for the web views
"""
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
    "user": generate_password_hash("user")
}

roles = { "admin": ["admin", "user"], "user": ["user"] }

@auth.verify_password
def verify_password(username, password):
    """
        Check if a username and password are valid

        - Args :
            - username (str) : the username
            - password (str) : the password

        - Returns :
            - (str) : the user associated with the username
    
    """
    if username in users and check_password_hash(users.get(username), password):
        logging.info(f"User {username} has been authenticated")
        return username


@auth.get_user_roles
def get_user_roles(user):
    """
        Get the roles of a user

        - Args :
            - user (str) : the username

        - Returns :
            - (list) : the roles of the user
    """
    return roles.get(user)
