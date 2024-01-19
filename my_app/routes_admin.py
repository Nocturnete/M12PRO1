from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask_login import current_user
<<<<<<< HEAD
from .forms import BanProductForm, UnbanProductForm
from .models import User, Product, Banned_Products, BlockedUser
=======
from werkzeug.utils import secure_filename
from .forms import BanProductForm, UnbanProductForm, BlockUserForm, UnblockUserForm
from .models import User, Product, Category, Status, Banned_Products, BlockedUser
>>>>>>> ded4e54 (Fix Block and Unblock users)
from .helper_role import Role, role_required, Action, perm_required
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
    blockedUsers = db.session.query(BlockedUser).order_by(BlockedUser.user_id).all()
    return render_template('admin/users/users_list.html', users=users, blockedUsers=blockedUsers)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['GET', 'POST'])
@role_required(Role.admin)
def block_user(user_id):
    user = db.session.query(User).get(user_id)
    form = BlockUserForm()
    if form.validate_on_submit():
        userToBlock = BlockedUser()
        userToBlock.user_id = user_id
        form.populate_obj(userToBlock)
        db.session.add(userToBlock)
        db.session.commit()
        flash(f'Usuario {user.name} bloqueado con éxito.', 'success')
        return redirect(url_for('admin_bp.admin_users'))
    return render_template('admin/users/block_user.html', user=user, form=form)

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['GET', 'POST'])
@role_required(Role.admin)
def unblock_user(user_id):
    user = db.session.query(User).get(user_id)
    blocked_user = db.session.query(BlockedUser).filter(BlockedUser.user_id == user_id).one_or_none()
    reason = blocked_user.reason if blocked_user else None
    form = UnblockUserForm()
    if form.validate_on_submit():
        blocked_user_to_delete = db.session.query(BlockedUser).filter(BlockedUser.user_id == user_id).one_or_none()
        if blocked_user_to_delete:
            db.session.delete(blocked_user_to_delete)
            db.session.commit()
            flash(f'Usuario {user.name} desbloqueado con éxito.', 'success')
            return redirect(url_for('admin_bp.admin_users'))
    return render_template('admin/users/unblock_user.html', user=user, form=form, reason=reason)


# @admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['GET', 'POST'])
# @role_required(Role.admin)
# def unblock_user(user_id):
#     user = db.session.query(User).get(user_id)
#     blocked_user = db.session.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
#     reason = blocked_user.reason if blocked_user else None 
#     form = UnblockUserForm()
#     if form.validate_on_submit():
#         blocked_user_to_delete = db.session.query(BlockedUser).filter(BlockedUser.user_id == user_id).first()
#         if blocked_user_to_delete:
#             db.session.delete(blocked_user_to_delete)
#             db.session.commit()
#             flash(f'Usuario {user.name} desbloqueado con éxito.', 'success')
#             return redirect(url_for('admin_bp.admin_users'))
#     return render_template('admin/users/unblock_user.html', user=user, form=form, reason=reason)


@admin_bp.route('/admin/products/<int:product_id>/ban', methods = ['POST', 'GET'])
@perm_required(Action.products_read)
@role_required(Role.moderator)
def ban_products(product_id):
    product = Product.get_filtered_by(id=product_id)
    if not product:
        abort(404)
    if not current_user.is_action_allowed_to_product(Action.products_moderate, product):
        abort(403)
    form = BanProductForm()
    if form.validate_on_submit():
        ban_product = Banned_Products()
        ban_product.product_id = product_id
        form.populate_obj(ban_product)
        Banned_Products.save(ban_product)
        flash("Producte banejat", "success")
        return redirect(url_for('products_bp.product_list'))
    else:
        return render_template('admin/ban_product.html', form = form, product = product)
    
@admin_bp.route('/admin/products/<int:product_id>/unban', methods = ['POST', 'GET'])
@perm_required(Action.products_read)
@role_required(Role.moderator)
def unban_products(product_id):
    product = Product.get_filtered_by(id=product_id)
    if not product:
        abort(404)
    if not current_user.is_action_allowed_to_product(Action.products_moderate, product):
        abort(403)
    eliminar = Banned_Products.get_filtered_by(product_id = product_id)
    form = UnbanProductForm()
    if form.validate_on_submit():
        if eliminar:
            Banned_Products.delete(eliminar)
        flash("Producte desbanejat", "success")
        return redirect(url_for('products_bp.product_list'))
    else:
        return render_template('admin/unban_product.html', form = form, product = product)
<<<<<<< HEAD
    
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
=======
>>>>>>> ded4e54 (Fix Block and Unblock users)
