from datetime import date
from flask_httpauth import HTTPTokenAuth
from pydantic import BaseModel, Field, constr
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

class Todo(BaseModel):
    task: constr() = Field(..., description="The task to do") # type: ignore
    complete: bool = Field(False, description="The completion status of the task")
    due: date = Field(None, description="The due date of the task") # type: ignore