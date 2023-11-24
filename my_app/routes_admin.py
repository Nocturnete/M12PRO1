from flask import Blueprint, render_template
from flask_login import current_user, login_required
from .models import User
from .helper_role import require_admin_permission
from . import db_manager as db
from flask_principal import Permission

# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates", static_folder="static"
)

@admin_bp.route('/admin')
@login_required
@require_admin_permission.require(http_exception=403)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@login_required
@require_admin_permission.require(http_exception=403)
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin/index.html', users=users)