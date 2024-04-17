"""
    This module contains the services of the application

    - Services :
        - export_to_csv : export all the Todos to a CSV file
        - import_from_csv : import all the Todos from a CSV file
"""
import csv
import dataclasses
import io

from datetime import datetime

from toudou.models import create_todo, get_all_todos, Todo
from toudou import config


def export_to_csv() -> str :
    """
        Export all the Todos to a CSV file

        - Args :
            - None

        - Returns :
            - path (str) : the path to the CSV file
    """
    path = config['DATA_FOLDER'] + "/todos.csv"

    with open(path, "w") as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([f.name for f in dataclasses.fields(Todo)])

        for todo in get_all_todos():
            csv_writer.writerow(todo.__dict__.values())

    return path


def import_from_csv(csv_file: io.StringIO) -> None:
    """
        Import all the Todos from a CSV file

        - Args :
            - csv_file (io.StringIO) : the CSV file to import from

        - Returns :
            - None
    """
    csv_reader = csv.DictReader(
        csv_file,
        fieldnames=[f.name for f in dataclasses.fields(Todo)]
    )
    for row in csv_reader:
        if row["id"] != "id" and row["task"]:
            create_todo(
                task=row["task"],
                due=datetime.fromisoformat(row["due"]) if row["due"] else None,
                complete=row["complete"] == "True"
            )
