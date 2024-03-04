# import os
# import pickle
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
    id: uuid.UUID
    task: str
    complete: bool
    due: datetime | None


def init_db() -> None:
    # Avec Pickle
    # os.makedirs(TODO_FOLDER, exist_ok=True)

    # Avec SQLAlchemy
    metadata.create_all(engine)


def read_from_file(filename: str) -> Todo:
    # Avec Pickle
    # with open(os.path.join(TODO_FOLDER, filename), "rb") as f:
    #     return pickle.load(f)

    # Avec SQLAlchemy
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
    # Avec Pickle
    # with open(os.path.join(TODO_FOLDER, filename), "wb") as f:
    #     pickle.dump(todo, f)

    # Avec SQLAlchemy
    stmt = todos_table.insert().values(task=todo.task, complete=todo.complete, due=todo.due)
    with engine.begin() as conn:
        conn.execute(stmt)


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

    # Avec Pickle
    # for id in os.listdir(TODO_FOLDER):
    #     todo = get_todo(uuid.UUID(id))
    #     if todo:
    #         result.append(todo)

    # Avec SQLAlchemy
    with engine.connect() as conn:
        for row in conn.execute(select(todos_table)):
            result.append(Todo(
                row.id,
                row.task,
                row.complete,
                row.due
            ))

    result.sort(key=lambda todo: todo.due or datetime.max)

    return result


def update_todo(
    id: uuid.UUID,
    task: str,
    complete: bool,
    due: datetime | None
) -> None:
    if get_todo(id):
        todo = Todo(id, task=task, complete=complete, due=due)
        delete_todo(id)
        write_to_file(todo, todo.id.hex)


def delete_todo(id: uuid.UUID) -> None:
    # Avec Pickle
    # os.remove(os.path.join(TODO_FOLDER, id.hex))

    # Avec SQLAlchemy
    stmt = todos_table.delete().where(todos_table.c.id == id)
    with engine.begin() as conn:
        conn.execute(stmt)
