from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db_manager = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db_manager.init_app(app)

    with app.app_context():
        from . import routes_main
        app.register_blueprint(routes_main.main_bp)

    app.logger.info("Aplicación iniciada")
    return app