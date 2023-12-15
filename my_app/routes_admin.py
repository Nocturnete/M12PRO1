from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import current_user
from werkzeug.utils import secure_filename
from .forms import BanProductForm, UnbanProductForm
from .models import User, Product, Category, Status, Banned_Products, BlockedUser
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
    if form.validate_on_submit():
        new_product = Banned_Products()
        new_product.product_id = product_id
        form.populate_obj(new_product)
        db.session.add(new_product)
        db.session.commit()
        flash("Producte banejat", "success")
        return redirect(url_for('products_bp.product_list'))
    else:
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
    if form.validate_on_submit():
        if eliminar:
            db.session.delete(eliminar)
            db.session.commit()
        flash("Producte desbanejat", "success")
        return redirect(url_for('products_bp.product_list'))
    else:
        return render_template('admin/unban_product.html', form = form, product = product)
    
@admin_bp.route('/admin/users/<int:user_id>/block', methods=['GET', 'POST'])
@role_required(Role.admin)
def block_user(user_id):
    user_to_block = db.session.query(User).get_or_404(user_id)
    if request.method == 'POST':
        blocked_user = BlockedUser(user=user_to_block, reason=request.form.get('reason'))
        db.session.add(blocked_user)
        db.session.commit()
        user_to_block.blocked_user_id = blocked_user.id
        db.session.commit()
        flash(f'Usuario {user_to_block.name} bloqueado con éxito.', 'success')
        return redirect(url_for('admin_bp.admin_users'))
    return render_template('admin/block_user.html', user=user_to_block)

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['GET', 'POST'])
@role_required(Role.admin)
def unblock_user(user_id):
    result = db.session.query(User, BlockedUser).join(BlockedUser).filter(BlockedUser.id == user_id).one_or_none() 
    if result:
        (user, block) = result
        user_name = user.name
    if request.method == 'POST':
        blocked_user_to_delete = db.session.query(BlockedUser).get(user_id)
        db.session.delete(blocked_user_to_delete)
        db.session.commit()
        flash(f'Usuario {user_name} desbloqueado con éxito.', 'success')
        return redirect(url_for('admin_bp.admin_users'))
    return render_template('admin/unblock_user.html', user=user, block=block)
