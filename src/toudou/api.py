from datetime import date, datetime
from flask import Blueprint, Request, jsonify, request
from flask_httpauth import HTTPTokenAuth
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic import BaseModel, Field, constr
import uuid, logging

import toudou.models as models

api_auth = HTTPTokenAuth(scheme='Bearer')
api_check = FlaskPydanticSpec('flask')
api = Blueprint('api', __name__, url_prefix="/api")

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
    task: constr() = Field(description="The task to do") # type: ignore
    complete: bool = Field(False, description="The completion status of the task")
    due: date = Field(None, description="The due date of the task") # type: ignore

class Todo_Patch(BaseModel):
    task: constr() = Field(None, description="The task to do") # type: ignore
    complete: bool = Field(None, description="The completion status of the task")
    due: date = Field(None, description="The due date of the task") # type: ignore


# Routes

@api.route("/todos", methods=["GET"])
@api_auth.login_required
def get_todos():
    """
        Get all the Todos

        - Args :
            - None

        - Returns :
            - (list) : the list of all the Todos
    """
    todos = models.get_all_todos()

    # Complete filter
    if request.args.get('complete')  == "true":
        todos = [todo for todo in todos if todo.complete]
    elif request.args.get('complete')  == "false":
        todos = [todo for todo in todos if not todo.complete]

    # Due filter
    if request.args.get('due') == "null":
        todos = [todo for todo in todos if todo.due == None]
    elif request.args.get('due'):
        todos = [todo for todo in todos if todo.due == datetime.strptime(request.args.get('due'), "%Y-%m-%d")]

    return jsonify(todos)


@api.route("/todos/<id>", methods=["GET"])
@api_auth.login_required
def get_todo_by_id(id):
    """
        Get a Todo by its ID

        - Args :
            - id (str) : the ID of the Todo

        - Returns :
            - (dict) : the Todo
    """
    return jsonify(models.get_todo(uuid.UUID(id)))


@api.route("/todos", methods=["POST"])
@api_auth.login_required
@api_check.validate(body=Request(Todo))
def create_todo():
    """
        Create a new Todo

        - Args :
            - None

        - Returns :
            - (str) : the HTML for the index page
    """
    data = request.json
    logging.info(f"Adding a new Todo: {data}")
    models.create_todo(data['task'], \
                       due=(datetime.strptime(data['due'], "%Y-%m-%d") if 'due' in data.keys() else None), \
                       complete=(data['complete'] if 'complete' in data.keys() else False))

    return {"message": "Todo created"}, 201


@api.route("/todos/<id>", methods=["PUT"])
@api_auth.login_required
@api_check.validate(body=Request(Todo))
def update_todo_by_id(id):
    """
        Update a Todo by its ID

        - Args :
            - id (str) : the ID of the Todo

        - Returns :
            - (dict) : the Todo
    """
    data = request.json

    if not models.get_todo(uuid.UUID(id)) :
        logging.warning(f"[PUT] - Todo {id} requested but not existing")
        return {"message": "Todo not replaced"}
    
    logging.info(f"Replacing Todo {id}: {data}")
    models.update_todo(uuid.UUID(id), data['task'], \
                       due=(datetime.strptime(data['due'], "%Y-%m-%d") if 'due' in data.keys() else None), \
                       complete=(data['complete'] if 'complete' in data.keys() else False))

    return {"message": "Todo replaced"}, 200


@api.route("/todos/<id>", methods=["DELETE"])
@api_auth.login_required
def delete_todo_by_id(id):
    """
        Delete a Todo by its ID

        - Args :
            - id (str) : the ID of the Todo

        - Returns :
            - (dict) : the Todo
    """
    if not models.get_todo(uuid.UUID(id)) :
        logging.warning(f"[DELETE] - Todo {id} requested but not existing")
        return {"message": "Todo not updated"}
    
    logging.info(f"Deleting Todo {id}")
    models.delete_todo(uuid.UUID(id))

    return {"message": "Todo deleted"}, 200


@api.route("/todos/<id>", methods=["PATCH"])
@api_auth.login_required
@api_check.validate(body=Request(Todo_Patch))
def patch_todo(id):
    """
        Patch a Todo by its ID

        - Args :
            - id (str) : the ID of the Todo

        - Returns :
            - (dict) : the Todo
    """
    data = request.json
    old_todo = models.get_todo(uuid.UUID(id))
    if not old_todo :
        logging.warning(f"[PATCH] - Todo {id} requested but not existing")
        return {"message": "Todo not updated"}
    
    logging.info(f"Updating Todo {id}: {data}")
    models.update_todo(uuid.UUID(id), data['task'] if 'task' in data.keys() else old_todo.task, \
                       due=(datetime.strptime(data['due'], "%Y-%m-%d") if 'due' in data.keys() else old_todo.due), \
                       complete=(data['complete'] if 'complete' in data.keys() else old_todo.complete))
    
    return {"message": "Todo updated"}, 200
