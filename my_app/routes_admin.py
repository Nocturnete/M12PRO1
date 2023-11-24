from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models import User
from .helper_role import require_admin_role, require_moderator_role
from . import db_manager as db
from flask_principal import Permission

# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates/admin", static_folder="static"
)

@admin_bp.route('/admin')
@login_required
@require_admin_role.require(http_exception=403)
def admin_index():
    return render_template('index.html')

@admin_bp.route('/admin/users')
@login_required
@require_admin_role.require(http_exception=403)
def admin_users():
    users = db.session.query(User).all()
    return render_template('users_list.html', users=users)