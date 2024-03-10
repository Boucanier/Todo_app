"""
    This module contains the model for the Todo application : the Todo class and the functions to interact with the database OR with the pickle files
    Pickle related actions are commented, as they are not used in the final version of the application
"""

# import pickle
import os
import select
import uuid

from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Table, MetaData, Uuid, select


TODO_FOLDER = "db"


engine = create_engine("sqlite:///" + TODO_FOLDER + "/todos.db", echo=True)
metadata = MetaData()
todos_table = Table(
        "todos",
        metadata,
        Column("id", Uuid, primary_key=True, default=uuid.uuid4),
        Column("task", String, nullable=False),
        Column("complete", Boolean, nullable=False),
        Column("due", DateTime, nullable=True)
    )

@dataclass
class Todo:
    """
        The Todo class, representing a task to do with its completion status and its due date
    """
    id: uuid.UUID
    task: str
    complete: bool
    due: datetime | None


def init_db() -> None:
    """
        Database initialization
        Create the database and the table if they don't exist

        - Args :
            - None

        - Returns :
            - None
    """
    os.makedirs(TODO_FOLDER, exist_ok=True)

    # With SQLAlchemy
    metadata.create_all(engine)


def read_from_file(filename: str) -> Todo:
    """
        Read a Todo from a file

        - Args :
            - filename (str) : the name of the file to read from -> Only for Pickle

        - Returns :
            - (Todo) : the Todo read from the file
    """
    # With Pickle
    # with open(os.path.join(TODO_FOLDER, filename), "rb") as f:
    #     return pickle.load(f)

    # With SQLAlchemy
    stmt = select(todos_table).where(todos_table.c.id == uuid.UUID(filename))
    with engine.begin() as conn:
        result = conn.execute(stmt)

    retId = None
    
    for row in result:
        retId = row.id
        retTask = row.task
        retComplete = row.complete
        retDue = row.due

    if retId:
        return Todo(retId, retTask, retComplete, retDue)
    else:
        return None # type: ignore


def write_to_file(todo: Todo, filename: str) -> None:
    """
        Write a Todo to a file
        
        - Args :
            - todo (Todo) : the Todo to write to the file
            - filename (str) : the name of the file to write to -> Only for Pickle
            
        - Returns :
            - None
    """
    # With Pickle
    # with open(os.path.join(TODO_FOLDER, filename), "wb") as f:
    #     pickle.dump(todo, f)

    # With SQLAlchemy
    stmt = todos_table.insert().values(task=todo.task, complete=todo.complete, due=todo.due)
    with engine.begin() as conn:
        conn.execute(stmt)


def create_todo(
    task: str,
    complete: bool = False,
    due: datetime | None = None
) -> None:
    """
        Create a new Todo and write it to a file

        - Args :
            - task (str) : the task of the Todo
            - complete (bool) : the completion status of the Todo
            - due (datetime | None) : the due date of the Todo

        - Returns :
            - None
    """
    todo = Todo(uuid.uuid4(), task=task, complete=complete, due=due)
    write_to_file(todo, todo.id.hex)


def get_todo(id: uuid.UUID) -> Todo:
    """
        Get a Todo from a file

        - Args :
            - id (uuid.UUID) : the id of the Todo to get

        - Returns :
            - (Todo) : the Todo with the given id
    """
    return read_from_file(id.hex)


def get_all_todos() -> list[Todo]:
    """
        Get all the Todos from the files

        - Args :
            - None

        - Returns :
            - result (list[Todo]) : a list of all the Todos
    """
    result = []

    # With Pickle
    # for id in os.listdir(TODO_FOLDER):
    #     todo = get_todo(uuid.UUID(id))
    #     if todo:
    #         result.append(todo)

    # With SQLAlchemy
    with engine.connect() as conn:
        for row in conn.execute(select(todos_table)):
            result.append(Todo(
                row.id,
                row.task,
                row.complete,
                row.due
            ))

    result.sort(key=lambda todo: todo.due or datetime.max)
    result.sort(key=lambda todo: todo.complete)

    return result


def update_todo(
    id: uuid.UUID,
    task: str,
    complete: bool,
    due: datetime | None
) -> None:
    """
        Update a Todo with new values

        - Args :
            - id (uuid.UUID) : the id of the Todo to update
            - task (str) : the new task of the Todo
            - complete (bool) : the new completion status of the Todo
            - due (datetime | None) : the new due date of the Todo

        - Returns :
            - None
    """
    if get_todo(id):
        todo = Todo(id, task=task, complete=complete, due=due)
        delete_todo(id)
        write_to_file(todo, todo.id.hex)


def delete_todo(id: uuid.UUID) -> None:
    """
        Delete a Todo from the files

        - Args :
            - id (uuid.UUID) : the id of the Todo to delete

        - Returns :
            - None
    """
    # With Pickle
    # os.remove(os.path.join(TODO_FOLDER, id.hex))

    # With SQLAlchemy
    stmt = todos_table.delete().where(todos_table.c.id == id)
    with engine.begin() as conn:
        conn.execute(stmt)
