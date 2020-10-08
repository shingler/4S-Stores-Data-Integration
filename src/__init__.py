from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models.dms import *
from .models.system import *
from .models.log import *
from .models.nav import *


def create_app():
    app = Flask(__name__)
    # app.config.from_object("settings.Development")
    app.config.from_object("settings.Test")
    db.init_app(app)

    # app.register_blueprint()

    return app
