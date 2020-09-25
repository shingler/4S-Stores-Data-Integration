#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import db
from src import create_app

app = create_app()
with app.app_context():
    db.create_all()
