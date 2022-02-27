from datetime import date, datetime, timedelta
from http import client
from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous.url_safe import URLSafeSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

today = date.today()

# ---Models--------------------------------------#
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


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
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return f"Role {self.name}"

    def add_permissions(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permissions(self, perm):
        if not self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles = {
            "User": [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            "Admin": [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = "User"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permissions(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config["FLASKY_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def generate_confirmation_token(self):
        s = URLSafeSerializer(current_app.config["SECRET_KEY"])
        return s.dumps({"confirm": self.id})

    def confirm(self, token):
        s = URLSafeSerializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"), max_age=3600)
        except:
            return False
        if data.get("confirm") != self.id:
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

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(40), nullable=False)
    due_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"Task({self.description}, {self.due_date}, {self.status})"


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    def __repr__(self):
        return f"Role {self.username}"
