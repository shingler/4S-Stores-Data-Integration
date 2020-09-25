#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import config


class Base:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/dms_interface?charset=utf8"
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = -1
    SQLALCHEMY_MAX_OVERFLOW = 2
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Development(Base):
    pass


class Test(Base):
    pass


class Production(Base):
    pass
