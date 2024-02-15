import os
import pickle
import uuid

from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Table, MetaData, Uuid


TODO_FOLDER = "db"


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    complete: bool
    due: datetime | None


def init_db() -> None:
    # Avec Pickle
    # os.makedirs(TODO_FOLDER, exist_ok=True)

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

    metadata.create_all(engine)


def read_from_file(filename: str) -> Todo:
    with open(os.path.join(TODO_FOLDER, filename), "rb") as f:
        return pickle.load(f)


def write_to_file(todo: Todo, filename: str) -> None:
    with open(os.path.join(TODO_FOLDER, filename), "wb") as f:
        pickle.dump(todo, f)


def create_todo(
    task: str,
    complete: bool = False,
    due: datetime | None = None
) -> None:
    todo = Todo(uuid.uuid4(), task=task, complete=complete, due=due)
    write_to_file(todo, todo.id.hex)


def get_todo(id: uuid.UUID) -> Todo:
    return read_from_file(id.hex)


def get_all_todos() -> list[Todo]:
    result = []
    for id in os.listdir(TODO_FOLDER):
        todo = get_todo(uuid.UUID(id))
        if todo:
            result.append(todo)
    return result


def update_todo(
    id: uuid.UUID,
    task: str,
    complete: bool,
    due: datetime | None
) -> None:
    if get_todo(id):
        todo = Todo(id, task=task, complete=complete, due=due)
        write_to_file(todo, todo.id.hex)


def delete_todo(id: uuid.UUID) -> None:
    os.remove(os.path.join(TODO_FOLDER, id.hex))
