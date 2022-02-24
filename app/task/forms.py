from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    week_out = date.today() + timedelta(days=7)
    description = StringField("Description", validators=[DataRequired()])
    due_date = StringField("Due Date", default=week_out, validators=[DataRequired()])
    status = StringField("Status", default="⛔️", validators=[DataRequired()])
    submit = SubmitField("Save")
