from flask_httpauth import HTTPTokenAuth
import logging

api_auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "tk1": "jules",
    "tk2": "matis"
}


@api_auth.verify_token
def verify_token(token):
    if token in tokens:
        logging.info(f"Token {token} is valid -> user = {tokens[token]}")
        return tokens[token]

    else:
        logging.error(f"Token {token} is invalid")
        return None