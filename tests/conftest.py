#!/usr/bin/python
# -*- coding:utf-8 -*-
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.models.nav import set_Env


@pytest.fixture(scope="session")
def init_app():
    app = Flask(__name__)
    app.config.from_object("settings.Development")
    # app.config.from_object("settings.Test")
    set_Env(app.config["ENV"])
    db = SQLAlchemy()
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()

    return app, db


@pytest.fixture(scope="session")
def load_app():
    from bin import app, db
    return app, db
