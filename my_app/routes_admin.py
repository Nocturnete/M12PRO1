from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from .forms import BanProductForm, UnbanProductForm
from .models import User, Product, Category, Status, Banned_Products
from .helper_role import Role, role_required, Action, perm_required
import uuid
import os

from . import db_manager as db


admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)

@admin_bp.route('/admin/products/<int:product_id>/ban', methods = ['POST', 'GET'])
@perm_required(Action.products_read)
@role_required(Role.moderator)
def ban_products(product_id):

    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_moderate, product):
        abort(403)

    form = BanProductForm()
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        new_product = Banned_Products()
        new_product.product_id = product_id

        # dades del formulari a l'objecte product
        form.populate_obj(new_product)

        # insert!
        db.session.add(new_product)
        db.session.commit()

        flash("Producte banejat", "success")
        return redirect(url_for('products_bp.product_list'))
    else: # GET
        return render_template('admin/ban_product.html', form = form, product = product)
    
@admin_bp.route('/admin/products/<int:product_id>/unban', methods = ['POST', 'GET'])
@perm_required(Action.products_read)
@role_required(Role.moderator)
def unban_products(product_id):

    product = db.session.query(Product).filter(Product.id == product_id).one_or_none()

    if not product:
        abort(404)

    if not current_user.is_action_allowed_to_product(Action.products_moderate, product):
        abort(403)

    eliminar = db.session.query(Banned_Products).filter(Banned_Products.product_id == product_id).one_or_none()


    form = UnbanProductForm()
    if form.validate_on_submit(): # si s'ha fet submit al formulari
        if eliminar:
            db.session.delete(eliminar)
            db.session.commit()

        flash("Producte desbanejat", "success")
        return redirect(url_for('products_bp.product_list'))
    else: # GET
        return render_template('admin/unban_product.html', form = form, product = product)
