from flask import flash, render_template, session, redirect, request, url_for
from flask_login import login_required
from . import cont
from .forms import ContactForm
from .. import db
from ..models import User, Contact

@cont.route("/contacts/<int:contact_id>/delete", methods=["GET", "POST"])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact {} has been deleted".format(contact.first), "success")
    return redirect(url_for("cont.contacts"))

@cont.route("/contacts", methods=["GET"])
@login_required
def contacts():
    contacts = Contact.query.all()
    #for contact in contacts:
    #    contact.update_next_contact()
    return render_template("cont/contacts.html", title="Contacts", contacts=contacts)

@cont.route("/contacts/<int:contact_id>", methods=["GET"])
@login_required
def contact_view(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template("cont/contact.html", contact=contact)


@cont.route("/contacts/<int:contact_id>/update", methods=["GET", "POST"])
@login_required
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    form = ContactForm()
    if form.validate_on_submit():
        contact.first = form.first.data
        contact.frequency = form.frequency.data
        db.session.commit()
        flash("Contact {} has been updated".format(contact.first), "success")
        return redirect(url_for("cont.contacts"))
    elif request.method == "GET":
        form.first.data = contact.first
        form.last.data = contact.last
        form.phone.data = contact.phone
        form.email.data = contact.email
        form.frequency.data = contact.frequency
        form.last_contact.data = contact.last_contact
        form.next_contact.data = contact.next_contact
        form.notes.data = contact.notes
    return render_template(
        "cont/contact_edit.html", title="Edit Contact", form=form
    )
