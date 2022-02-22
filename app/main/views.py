from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User, Contact


@main.route("/")
def index():
    return render_template("index.html", title="Home")


@main.route("/contacts")
def contacts():
    contacts = Contact.query.all()
    for contact in contacts:
        contact.update_next_contact()
    return render_template("contacts.html", title="Contacts", contacts=contacts)


# @main.route("/form", methods=["GET", "POST"])
# def form():
#    form = NameForm()
#    if form.validate_on_submit():
#        user = User.query.filter_by(username=form.name.data).first()
#        if user is None:
#            user = User(username=form.name.data)
#            db.session.add(user)
#            session["known"] = False
#            if app.config["FLASKY_ADMIN"]:
#                send_email(
#                    app.config["FLASKY_ADMIN"],
#                    "New User",
#                    "mail/new_user",
#                    user=user,
#                )
#        else:
#            session["known"] = True
#        session["name"] = form.name.data
#        form.name.data = ""
#        old_name = session.get("name")
#        return redirect(url_for(".form"))
#    return render_template(
#        "form.html",
#        form=form,
#        name=session.get("name"),
#        known=session.get("known", False),
#    )
