from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models.dms import *


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.Development")
    db.init_app(app)

    # app.register_blueprint()

    return app
