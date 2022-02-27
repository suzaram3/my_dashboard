from datetime import date, datetime, timedelta
from http import client
from flask import current_app
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeSerializer
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from . import login_manager

today = date.today()

# ---Models--------------------------------------#
class Book(db.Model):
    __tablename__ = "book"
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(64), nullable=False)
    book_author = db.Column(db.String(64), nullable=False)
    book_shelf = db.Column(db.String(64))
    book_read = db.Column(db.Integer)

    def __repr__(self):
        return f"<Book: {self.book_title} by {self.book_author.title()}>"


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(64), nullable=False)
    last = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(10))
    email = db.Column(db.String(64), index=True)
    frequency = db.Column(db.Integer, nullable=False)
    last_contact = db.Column(db.String(10), default=today.strftime("%Y-%m-%d"))
    next_contact = db.Column(db.String(10))
    notes = db.Column(db.String)

    def update_next_contact(self):
        if self.last_contact is not None:
            last_contact_iso = date.fromisoformat(self.last_contact)
            next_contact_date = last_contact_iso + timedelta(days=self.frequency * 30)
            next_contact_date = next_contact_date.strftime("%Y-%m-%d")
            db.session.query(Contact).filter(Contact.first == self.first).update(
                {Contact.next_contact: next_contact_date}
            )
            db.session.commit()

    def __repr__(self):
        return (
            f"{self.first.title()} {self.last.title()}\n{self.phone}, {self.email}\n\n"
        )


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return f"Role {self.name}"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = URLSafeSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'), max_age=3600)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Task({self.description}, {self.due_date}, {self.status})"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    def __repr__(self):
        return f"Role {self.username}"
