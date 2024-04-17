"""
    This module contains the models used in the API
"""
from datetime import date
from pydantic import BaseModel, Field, constr


class Todo(BaseModel):
    """
        Class representing a new Todo (task field is mandatory)

        - Attributes :
            - task (str) : the task to do
            - complete (bool) : the completion status of the task
            - due (date) : the due date of the task
    """
    task: constr() = Field(description="The task to do") # type: ignore
    complete: bool = Field(False, description="The completion status of the task")
    due: date = Field(None, description="The due date of the task")

class Todo_Patch(BaseModel):
    """
        Class representing todo attributes to patch

        - Attributes :
            - task (str) : the task to do
            - complete (bool) : the completion status of the task
            - due (date) : the due date of the task
    """
    task: constr() = Field(None, description="The task to do") # type: ignore
    complete: bool = Field(None, description="The completion status of the task")
    due: date = Field(None, description="The due date of the task")