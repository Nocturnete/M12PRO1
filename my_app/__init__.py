from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager =  Principal()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)

    with app.app_context():
        from . import routes_main, routes_auth
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)


    app.logger.info("Aplicación iniciada")
    return app