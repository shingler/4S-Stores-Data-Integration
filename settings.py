#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import config


class Base:
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_TIMEOUT = 30
    SQLALCHEMY_POOL_RECYCLE = -1
    SQLALCHEMY_MAX_OVERFLOW = 2
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


class Development(Base):
    ENV = "Development"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/dms_interface?charset=utf8"


class Test(Base):
    ENV = "Test"
    # SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:msSqlServer2020@127.0.0.1:1401/dms_interface"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:msSqlServer2020@127.0.0.1:1401/dms_interface?driver=ODBC+Driver+17+for+SQL+Server"

class Production(Base):
    ENV = "production"
