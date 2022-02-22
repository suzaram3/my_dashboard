from flask import render_template, session, redirect, url_for
from flask_login import login_required
from . import cont
from .. import db
from ..models import User, Contact


@cont.route("/")
@login_required
def contacts():
    contacts = Contact.query.all()
    for contact in contacts:
        contact.update_next_contact()
    return render_template("contacts.html", title="Contacts", contacts=contacts)
