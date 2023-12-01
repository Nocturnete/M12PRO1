from flask import Blueprint, render_template, redirect, url_for, flash, abort
from .models import Status
from .forms import StatusForm, DeleteForm
from .helper_role import Action, perm_required
from . import db_manager as db

status_bp = Blueprint("status_bp", __name__)

@status_bp.route('/statuses/list')
@perm_required(Action.statuses_list)
def status_list():
    statuses = db.session.query(Status).order_by(Status.id.asc()).all()
    
    return render_template('statuses/list.html', statuses = statuses)

@status_bp.route('/statuses/create', methods = ['POST', 'GET'])
@perm_required(Action.statuses_create)
def status_create(): 
    form = StatusForm()

    if form.validate_on_submit():
        new_status = Status()

        form.populate_obj(new_status)

        db.session.add(new_status)
        db.session.commit()

        flash("Nuevo estado creado", "success")

        return redirect(url_for('status_bp.status_list'))
    
    else:
        return render_template('statuses/create.html', form = form)

@status_bp.route('/statuses/read/<int:status_id>')
@perm_required(Action.statuses_read)
def status_read(status_id):
    status = db.session.query(Status).filter(Status.id == status_id).one_or_none()

    if not status:
        abort(404)

    return render_template('statuses/read.html', status = status)

@status_bp.route('/statuses/update/<int:status_id>',methods = ['POST', 'GET'])
@perm_required(Action.statuses_update)
def status_update(status_id):
    status = db.session.query(Status).filter(Status.id == status_id).one_or_none()
    
    if not status:
        abort(404)

    form = StatusForm(obj = status)

    if form.validate_on_submit():
        form.populate_obj(status)

        db.session.add(status)
        db.session.commit()

        flash("Estat actualitzat", "success")

        return redirect(url_for('status_bp.status_read', status_id = status_id))

    else:
        return render_template('statuses/update.html', status_id = status_id, form = form)

@status_bp.route('/statuses/delete/<int:status_id>',methods = ['GET', 'POST'])
@perm_required(Action.statuses_delete)
def status_delete(status_id):
    status = db.session.query(Status).filter(Status.id == status_id).one_or_none()

    if not status:
        abort(404)

    form = DeleteForm()
    if form.validate_on_submit(): 
        db.session.delete(status)
        db.session.commit()

        flash("Estado borrado", "success")

        return redirect(url_for('status_bp.status_list'))

    else:
        return render_template('statuses/delete.html', form = form, status = status)