from datetime import date, datetime
from flask import flash, render_template, session, redirect, request, url_for
from flask_login import current_user, login_required
from . import cont
from .forms import ContactForm
from .. import db
from ..models import User, Contact


@cont.route("/contacts/<int:contact_id>/delete", methods=["GET", "POST"])
@login_required
def delete_contact(contact_id):
    if current_user != task.user_id and not current_user.can(Permission.ADMIN):
        abort(403)
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact {} has been deleted".format(contact.first), "success")
    return redirect(url_for("cont.contacts"))


@cont.route("/contacts", methods=["GET"])
@login_required
def contacts():
    if current_user.is_authenticated:
        contacts = Contact.query.filter_by(user_id=current_user.id).all()
        #.order_by(Contact.first).all()
        return render_template("cont/contacts.html", title="Contacts", contacts=contacts)


@cont.route("/contacts/<int:contact_id>", methods=["GET"])
@login_required
def contact_view(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template("cont/contact.html", contact=contact)


@cont.route("/new", methods=["GET", "POST"])
@login_required
def new_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            first=form.first.data,
            last=form.last.data,
            phone=form.phone.data,
            email=form.email.data,
            frequency=form.frequency.data,
            last_contact=form.last_contact.data,
            next_contact=form.next_contact.data,
            notes=form.notes.data,
            user_id=current_user._get_current_object(),
        )
        db.session.add(contact)
        db.session.commit()
        contact.update_next_contact()
        flash("{} has been created!".format(contact.first), "success")
        return redirect(url_for("cont.contacts"))
    return render_template("cont/contact_edit.html", title="New Contact", form=form)


@cont.route("/contacts/<int:contact_id>/update", methods=["GET", "POST"])
@login_required
def update_contact(contact_id):
    if current_user != task.user_id and not current_user.can(Permission.ADMIN):
        abort(403)
    contact = Contact.query.get_or_404(contact_id)
    form = ContactForm(contact=contact)
    if form.validate_on_submit():
        contact.first = form.first.data
        contact.last = form.last.data
        contact.phone = form.phone.data
        contact.frequency = form.frequency.data
        contact.last_contact = form.last_contact.data
        contact.next_contact = form.next_contact.data
        contact.notes = form.notes.data
        db.session.add(contact)
        db.session.commit()
        contact.update_next_contact()
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
    return render_template("cont/contact_edit.html", title="Edit Contact", form=form)


@cont.route("contacts/today_contacts", methods=["GET"])
@login_required
def check_next_contact_date():
    t = date.today()
    today = t.strftime("%Y-%m-%d")
    contact_query = Contact.query.filter(Contact.next_contact == today)
    contacts = [contact for contact in contact_query]
    return render_template(
        "cont/contacts.html", title="Contacts For Today", contacts=contacts
    )
