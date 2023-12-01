from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required, logout_user
from .forms import ProfileForm, LoginForm, RegisterForm, ResendForm, ProductForm, CategoryForm, StatusForm, DeleteForm
from . import db_manager as db, mail_manager as mail, logger
import secrets
from .models import BlockedUser



main_bp = Blueprint("main_bp", __name__)


@main_bp.route('/')
def init():
    if current_user.is_authenticated:
        return redirect(url_for('products_bp.product_list'))
    else:
        return redirect(url_for("auth_bp.login"))
    
@main_bp.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    blocked_user = BlockedUser.query.filter_by(user_id=current_user.id).first()
    form = ProfileForm()
    if form.validate_on_submit():
        something_change = False
        new_email = form.email.data
        new_name = form.name.data
        new_password = form.password.data

        if new_email != current_user.email:
            something_change = True
            current_user.email = new_email
            current_user.verified = False
            current_user.email_token = secrets.token_urlsafe(20)

        if new_name != current_user.name:
            something_change = True
            current_user.name = new_name

        if new_password: 
            something_change = True
            current_user.password = new_password

        if not something_change:
            flash("Cap canvi", "success")
        else:
            db.session.commit()
            if not current_user.verified:
                mail.send_register_email(current_user.name, current_user.email, current_user.email_token)
                logout_user()
                flash("Revisa el teu correu per verificar-lo", "success")
                return redirect(url_for("auth_bp.login"))

            flash("Perfil actualizado correctamente", "success")
            
        return redirect(url_for('main_bp.profile'))
    
    else:
        form.name.data = current_user.name
        form.email.data = current_user.email    

        return render_template('profile.html', form = form, blocked_user=blocked_user)

@main_bp.app_errorhandler(403)
def forbidden_access(e):
  return render_template('403.html',message=e), 403

@main_bp.app_errorhandler(404)
def not_allowed(e):
  return render_template('404.html',message=e), 404