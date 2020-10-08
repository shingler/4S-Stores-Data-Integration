#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

app = Flask(__name__)
app.config.from_object("settings.Development")
db = SQLAlchemy()
db.init_app(app)
context = app.app_context()
context.push()
