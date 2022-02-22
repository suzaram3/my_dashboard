from datetime import date, datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from . import login_manager

# ---Models--------------------------------------#
class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(64), nullable=False)
    last = db.Column(db.String(64))
    phone = db.Column(db.String(10))
    email = db.Column(db.String(64), index=True)
    frequency = db.Column(db.Integer, nullable=False)
    last_contact = db.Column(db.String(10))
    next_contact = db.Column(db.String(10))
    notes = db.Column(db.String)

    def update_next_contact(self):
        last_contact_iso = date.fromisoformat(self.last_contact)
        next_contact_date = last_contact_iso + timedelta(days=self.frequency * 30)
        next_contact_date = next_contact_date.strftime("%Y-%m-%d")
        db.session.query(Contact).filter(Contact.first == self.first).update(
            {Contact.next_contact: next_contact_date}
        )
        db.session.commit()

    def __repr__(self):
        return f"Contact {self.first, self.last}, frq: {self.frequency}, lc: {self.last_contact}, nc: {self.next_contact}"


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role")

    def __repr__(self):
        return f"Role {self.name}"


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    def __repr__(self):
        return f"Role {self.username}"
