import os
from os import environ
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:

    # Flask-Config
    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Base de datos
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + basedir + "/" + environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Assets
    STATIC_FOLDER = environ.get("STATIC_FOLDER")
    TEMPLATES_FOLDER = environ.get("TEMPLATES_FOLDER")
    UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")
    ALLOWED_EXTENSIONS = environ.get("ALLOWED_EXTENSIONS")




