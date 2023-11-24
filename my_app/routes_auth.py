from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import current_user, login_required, login_user, logout_user
from . import login_manager 
from .models import User
from .forms import LoginForm, RegisterForm
from . import db_manager as db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ja està autenticat, sortim d'aquí
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        plain_text_password = form.password.data

        user = load_user(email)

        print(f"Hash is {user.password} and password is {plain_text_password}")

        if user and check_password_hash(user.password, plain_text_password):
            login_user(user)
            flash('Logged in successfully.', "success")
            return redirect(url_for("main_bp.init"))

        flash("Credenciales incorrectas. Por favor, inténtelo de nuevo.", "error")
        return redirect(url_for("auth_bp.login"))

    return render_template('login.html', form = form)


@login_manager.user_loader
def load_user(email):
    if email is not None:
        try:
            user_or_none = db.session.query(User).filter(User.email == email).one()
            return user_or_none
        except (NoResultFound, MultipleResultsFound):
            return None
    return None



@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))




@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # Si ya está autenticado, redirigimos
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        plain_text_password = form.password.data

        # Verifica si el usuario ya existe
        existing_user = db.session.query(User).filter(User.email == email).first()
        if existing_user:
            flash('El correo electrónico ya está registrado. Inicia sesión en lugar de registrarte.', 'warning')
            return redirect(url_for("auth_bp.login"))

        # Crea un nuevo usuario y almacena el nombre, correo y la contraseña hasheada
        hashed_password = generate_password_hash(plain_text_password, method='scrypt:32768:8:1')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro exitoso. Inicia sesión ahora.', 'success')
        return redirect(url_for("auth_bp.login"))

    return render_template('register.html', form=form)

