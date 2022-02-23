from datetime import date, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    first = StringField("First", validators=[DataRequired()])
    last = StringField("Last")
    phone = StringField("Phone")
    email = StringField("Email")
    frequency = StringField("Frequency", validators=[DataRequired()])
    last_contact = StringField("Last Contact")
    next_contact = StringField("Next Contact")
    notes = TextAreaField("Notes")
    submit = SubmitField("Save")
