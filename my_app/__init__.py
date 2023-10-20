from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db_manager = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Valor aleatori molt llarg i super secret"

    # BASE DE DATOS
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + basedir + "/../database.db"
    app.config["SQLALCHEMY_ECHO"] = True
    
    # CARPETA UPLOADS
    app.config['UPLOAD_FOLDER'] = "my_app/uploads"

    # Inicialitza SQLAlchemy
    db_manager.init_app(app)

    with app.app_context():
        from . import routes_main
        app.register_blueprint(routes_main.main_bp)

    app.logger.info("Aplicación iniciada")
    return app