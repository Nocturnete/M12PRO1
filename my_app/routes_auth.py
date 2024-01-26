from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user
from . import login_manager, mail_manager
from .forms import LoginForm, RegisterForm, ResendForm
from .helper_role import notify_identity_changed, Role
from .models import User
import secrets


auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = load_user(email)
        if user and user.check_password(password):
            if not user.verified:
                flash("Revisa el teu email i verifica el teu compte", "error")
                return redirect(url_for("auth_bp.login"))
            
            login_user(user)
            notify_identity_changed()

            return redirect(url_for("main_bp.init"))

        flash("Error del usuario o contraseña", "error")

        return redirect(url_for("auth_bp.login"))
    
    return render_template('login.html', form = form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User()
        form.populate_obj(new_user)
        new_user.role = Role.wanner
        new_user.verified = False
        new_user.email_token = secrets.token_urlsafe(20)
        User.save(new_user)
        mail_manager.send_register_email(new_user.name, new_user.email, new_user.email_token)
        flash("Verifica el correo", "success")
        return redirect(url_for("auth_bp.login"))
    return render_template('register.html', form = form)

@auth_bp.route("/verify/<name>/<token>")
def verify(name, token):
    user = User.get_one_filtered_name(name = name)
    if user and user.email_token == token:
        user.verified = True
        user.email_token = None 
        flash("Se ha verificado el correo", "success")
    else:
        flash("Error de verificación", "error")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/resend", methods=["GET", "POST"])
def resend():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = ResendForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.get_one_filtered_email(email = email)
        if user:
            if user.verified:
                flash("Esta cuenta ya esta verificada", "error")

            else:
                mail_manager.send_register_email(user.name, user.email, user.email_token)
                flash("Verifica el correo", "success")
        else:
            flash("Esta cuenta no existe", "error")

        return redirect(url_for("auth_bp.login"))
    
    else:
        return render_template('resend.html', form = form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()

    flash("Te has desconectado", "success")

    return redirect(url_for("auth_bp.login"))

@login_manager.user_loader
def load_user(email):
    if email is not None:
        return User.get_one_filtered_email(email = email)
    return None

@login_manager.unauthorized_handler
def unauthorized():

    flash("Inicia sesión o registrate para acceder a esta pagina", "error")
    
    return redirect(url_for("auth_bp.login"))
