from flask import flash, render_template, session, redirect, request, url_for
from flask_login import login_required
from . import book
from .. import db
from .forms import BookForm
from ..models import Book


@book.route("/books/<int:book_id>/delete", methods=["GET", "POST"])
@login_required
def delete_book(book_id):
    book = book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("book {} has been deleted".format(book.book_title), "success")
    return redirect(url_for("book.books"))


@book.route("/books")
@login_required
def books():
    books = Book.query.all()
    return render_template("book/books.html", title="books", books=books)


@book.route("/new", methods=["GET", "POST"])
@login_required
def new_book():
    form = BookForm()
    if form.validate_on_submit():
        book = book(
            book_title=form.book_title.data,
            book_author=form.book_author.data,
            book_shelf=form.book_shelf.data,
            book_read=form.book_read.data,
        )
        db.session.add(book)
        db.session.commit()
        flash("book has been created!".format(book.book_title), "success")
        return redirect(url_for("book.books"))
    return render_template("book/book_edit.html", title="New book", form=form)


@book.route("/book/<int:book_id>")
def book_view(book_id):
    book = book.query.get_or_404(book_id)
    return render_template("book/book.html", book=book, legend=book.id)


@book.route("/books/<int:book_id>/update", methods=["GET", "POST"])
@login_required
def update_book(book_id):
    book = book.query.get_or_404(book_id)
    form = TaskForm()
    if form.validate_on_submit():
        book.book_title = form.book_title.data
        book.book_author = form.book_author.data
        book.book_shelf = form.book_shelf.data
        book_read = form.book_read.data
        db.session.commit()
        flash("book {} has been updated".format(book.book_title), "success")
        return redirect(url_for("book.books"))
    elif request.method == "GET":
        form.book_title.data = book.book_title
        form.book_author.data = book.book_author
        form.book_shelf.data = book.book_shelf
        book_read = form.book_read.data
    return render_template(
        "book/task_edit.html", title="Edit book", form=form, legend="Edit book"
    )
