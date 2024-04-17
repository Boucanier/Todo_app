"""
    This module contains the routes of the API
"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from spectree import SpecTree, SecurityScheme
import uuid, logging

import toudou.models as models
from toudou.api.auth import api_auth
from toudou.api.models import Todo, Todo_Patch

spec = SpecTree("flask", annotations=True, title="Toudou API",
    security_schemes=[SecurityScheme(name="bearer_token", data={"type": "http", "scheme": "bearer"})],
    security=[{"bearer_token": []}]) # Access swagger doc at [server adress]/apidoc/swagger/

api = Blueprint('api', __name__, url_prefix="/api")


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
@spec.validate(tags=["api"], json=Todo)
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
@spec.validate(tags=["api"], json=Todo)
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
@spec.validate(tags=["api"], json=Todo_Patch)
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
