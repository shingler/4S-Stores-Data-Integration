#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from src import set_Env

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
logging.basicConfig(filename="%s.log" % __name__, level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

app = Flask(__name__)
# app.config.from_object("settings.Development")
app.config.from_object("settings.Test")
set_Env(app.config["ENV"])
db = SQLAlchemy()
db.init_app(app)
context = app.app_context()
context.push()
