#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime

from sqlalchemy import and_
from sqlalchemy.orm import foreign, remote

from src import db
from . import dms, system


class NotificationLog(db.Model):
    __tablename__ = "Notification_Log"
    ID = db.Column(db.Integer, nullable=False, primary_key=True)
    # 公司代码(Link to table: DMS_API_Setup)
    Company_Code = db.Column(db.String(20), nullable=False, comment="公司代码(Link to table: DMS_API_Setup)")
    # 接口代码(Link to table: DMS_API_Setup)
    API_Code = db.Column(db.String(100), nullable=False, comment="接口代码(Link to table: DMS_API_Setup)")
    # 收件人
    Recipients = db.Column(db.String(500), nullable=False, comment="收件人")
    # 邮件标题
    Email_Title = db.Column(db.String(100), nullable=True, comment="邮件标题")
    # 邮件内容(HTML的内容)
    Email_Content = db.Column(db.Text, nullable=True, comment="邮件内容(HTML的内容)")
    # 发送时间
    Sent_DT = db.Column(db.DateTime, nullable=False, comment="发送时间",
                        default=datetime.datetime.now().isoformat(timespec="milliseconds"))

    company = db.relationship("dms.ApiSetup",
                              primaryjoin=foreign(Company_Code) == remote(dms.ApiSetup.Company_Code))


class APILog(db.Model):
    __tablename__ = "API_Log"
    ID = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    # 公司代码(Link to table: DMS_API_Setup)
    Company_Code = db.Column(db.String(20), nullable=False, comment="公司代码(Link to table: DMS_API_Setup)")
    # 接口代码(Link to table: DMS_API_Setup)
    API_Code = db.Column(db.String(100), nullable=False, comment="接口代码(Link to table: DMS_API_Setup)")
    # API输入参数(http包)
    API_P_In = db.Column(db.Text, nullable=True, comment="API输入参数(http包)")
    # API返回的内容(整个http包或者XML文件内容)
    API_Content = db.Column(db.Text, nullable=True, comment="API返回的内容(整个http包或者XML文件内容)")
    # 内容类型(1 - http包，2 - XML文件)
    Content_Type = db.Column(db.Integer, nullable=False, default=1, comment="内容类型(1 - http包，2 - XML文件)")
    # 执行时间
    Executed_DT = db.Column(db.DateTime, nullable=False, comment="执行时间")
    # 完成时间
    Finished_DT = db.Column(db.DateTime, nullable=True, comment="完成时间")
    # 1 - 系统自动, 2 - 人工手动
    Executed_By = db.Column(db.Integer, nullable=False, default=1, comment="1 - 系统自动, 2 - 人工手动")
    # 用户ID(Link to table: User_List), 如果为系统自动执行，值为System
    UserID = db.Column(db.String(50), nullable=False, comment="用户ID")

    company = db.relationship("dms.ApiSetup", primaryjoin=and_(
        (foreign(Company_Code) == remote(dms.ApiSetup.Company_Code)),
        (foreign(API_Code) == remote(dms.ApiSetup.API_Code))))

    user = db.relationship("system.UserList", primaryjoin=foreign(UserID) == remote(system.UserList.UserID))
