from flask import abort, flash, render_template, session, redirect, request, url_for
from flask_login import current_user, login_required
from . import task
from .. import db
from .forms import TaskForm
from ..models import User, Contact, Task, Permission


@task.route("/tasks/<int:task_id>/delete", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user != task.user_id and not current_user.can(Permission.ADMIN):
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash("Task {} has been deleted".format(task.id), "success")
    return redirect(url_for("task.tasks"))


@task.route("/tasks")
@login_required
def tasks():
    tasks_list = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("task/tasks.html", title="Tasks", tasks=tasks_list)


@task.route("/new", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data,
            user_id=current_user.id,
        )
        db.session.add(task)
        db.session.commit()
        flash("Task has been created!".format(task.description), "success")
        return redirect(url_for("task.tasks"))
    return render_template("task/task_edit.html", title="New Task", form=form)


@task.route("/task/<int:task_id>")
def task_view(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("task/task.html", task=task, legend=task.id)


@task.route("/tasks/<int:task_id>/update", methods=["GET", "POST"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user != task.user_id and not current_user.can(Permission.ADMIN):
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.status = form.status.data
        db.session.commit()
        flash("Task {} has been updated".format(task.description), "success")
        return redirect(url_for("task.tasks"))
    elif request.method == "GET":
        form.description.data = task.description
        form.due_date.data = task.due_date
        form.status.data = task.status
    return render_template(
        "task/task_edit.html", title="Edit Task", form=form, legend="Edit Task"
    )
