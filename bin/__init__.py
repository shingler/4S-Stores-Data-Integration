#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("settings.Development")
db = SQLAlchemy()
db.init_app(app)
context = app.app_context()
context.push()
