from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    book_title = StringField("Title", validators=[DataRequired()])
    book_author = StringField("Author", validators=[DataRequired()])
    book_shelf = StringField("Shelf")
    book_read = StringField("Read")
    submit = SubmitField("Save")
