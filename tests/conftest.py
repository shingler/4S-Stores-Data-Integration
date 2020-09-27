#!/usr/bin/python
# -*- coding:utf-8 -*-
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
@pytest.fixture(scope="session")
def init_app():
    app = Flask(__name__)
    app.config.from_object("settings.Development")
    db = SQLAlchemy()
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()

    return app, db
