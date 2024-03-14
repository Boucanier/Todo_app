from flask_wtf import FlaskForm
from wtforms import StringField, DateField, HiddenField, BooleanField
from wtforms.validators import DataRequired, Optional

class AddForm(FlaskForm):
    task = StringField("task", validators=[DataRequired()])
    due = DateField("due", validators=[Optional()])
    action = HiddenField("action", validators=[DataRequired()])

class UpdateForm(FlaskForm):
    id = HiddenField("id", validators=[DataRequired()])
    task = StringField("task", validators=[DataRequired()])
    due = DateField("due", validators=[DataRequired()])
    complete = BooleanField("complete", validators=[DataRequired()])
    action = HiddenField("action", validators=[DataRequired()])

class DeleteForm(FlaskForm):
    id = HiddenField("id", validators=[DataRequired()])
    action = HiddenField("action", validators=[DataRequired()])