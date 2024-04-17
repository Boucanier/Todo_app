"""
    This module contains the forms used in the web views
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Optional

class AddForm(FlaskForm):
    """
        Form to add a new Todo

        - Attributes :
            - task (str) : the task to do
            - due (date) : the due date of the task
            - action (str) : the action to perform
    """
    task = StringField("task", validators=[DataRequired()])
    due = DateField("due", validators=[Optional()])
    action = HiddenField("action", validators=[DataRequired()])

class UpdateForm(FlaskForm):
    """
        Form to update a Todo

        - Attributes :
            - id (str) : the id of the Todo
            - task (str) : the task to do
            - due (date) : the due date of the task
            - complete (bool) : the completion status of the task
            - action (str) : the action to perform
    """
    id = HiddenField("id", validators=[DataRequired()])
    task = StringField("task", validators=[DataRequired()])
    due = DateField("due", validators=[Optional()])
    complete = BooleanField("complete", validators=[Optional()])
    action = HiddenField("action", validators=[DataRequired()])

class DeleteForm(FlaskForm):
    """
        Form to delete a Todo

        - Attributes :
            - id (str) : the id of the Todo
            - action (str) : the action to perform
    """
    id = HiddenField("id", validators=[DataRequired()])
    action = HiddenField("action", validators=[DataRequired()])