from flask import Blueprint, render_template, flash, redirect, url_for, flash, abort, request
from .models import User, BlockedUser
from flask_login import current_user
from .helper_role import Role, role_required
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
    blocked_users = db.session.query(BlockedUser).all()
    return render_template('admin/users_list.html', users=users, blocked_users=blocked_users)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['POST'])
@role_required(Role.admin)
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    blocked_user = BlockedUser(user=user, reason=request.form.get('reason'))
    db.session.add(blocked_user)
    db.session.commit()
    flash(f'Usuario {user.username} bloqueado con éxito.', 'success')
    return redirect(url_for('admin.block_user'))

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['POST'])
@role_required(Role.admin)
def unblock_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)
    blocked_user = BlockedUser.query.filter_by(user_id=user.id).first()
    
    if blocked_user:
        db.session.delete(blocked_user)
        db.session.commit()
        flash(f'Usuario {user.username} desbloqueado con éxito.', 'success')
    else:
        flash(f'El usuario {user.username} no está bloqueado.', 'warning')

    return redirect(url_for('admin.unblock_user'))