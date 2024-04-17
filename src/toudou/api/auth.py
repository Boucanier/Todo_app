"""
    This module contains the authentication system for the API
"""
from flask_httpauth import HTTPTokenAuth
import logging

api_auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "tk1": "user1",
    "tk2": "user2"
}


@api_auth.verify_token
def verify_token(token: str) -> str | None :
    """
        Check if a token is valid

        - Args :
            - token (str) : the token to check

        - Returns :
            - (str) : the user associated with the token
    """
    if token in tokens:
        logging.info(f"Token {token} is valid -> user = {tokens[token]}")
        return tokens[token]

    else:
        logging.error(f"Token {token} is invalid")
        return None