#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import db


class UserList(db.Model):
    __tablename__ = "User_List"
    # 登陆用户ID
    UserID = db.Column(db.String(50), nullable=False, primary_key=True, comment="登陆用户ID")
    # 登陆密码
    Password = db.Column(db.String(50), nullable=False, comment="登陆密码")
    # 禁用
    Blocked = db.Column(db.Boolean, nullable=False, default=False, comment="禁用")
    # 是否接收提醒邮件
    Receive_Notification = db.Column(db.Boolean, nullable=False, default=False, comment="是否接收提醒邮件")
    # 邮件地址
    Email_Address = db.Column(db.String(100), nullable=False, comment="邮件地址")
    # 固定电话号码
    Telephone = db.Column(db.String(20), nullable=False, comment="固定电话号码")
    # 手机号码
    Cell_Phone = db.Column(db.String(20), nullable=False, comment="手机号码")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")


class SystemSetup(db.Model):
    __tablename__ = "System_Setup"
    ID = db.Column(db.Integer, nullable=False, primary_key=True)
    # SMTP主机地址(提醒邮件使用)
    Email_SMTP = db.Column(db.String(50), nullable=False, comment="SMTP主机地址(提醒邮件使用)")
    # SMTP端口
    SMTP_Port = db.Column(db.String(50), nullable=False, comment="SMTP端口")
    # 邮箱登陆ID
    Email_UserID = db.Column(db.String(50), nullable=False, comment="邮箱登陆ID")
    # 邮箱登陆密码
    Email_Password = db.Column(db.String(50), nullable=False, comment="邮箱登陆密码")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")
    # 系统URL
    System_URL = db.Column(db.String(500))
    # 使用SSL(1-是,0-否)
    Use_SSL = db.Column(db.Integer, default=1)
    # 每页显示行数
    Page_Cnt = db.Column(db.Integer, default=1)
    # 发件人名称
    Email_SenderName = db.Column(db.String(50))
    # 临时文件存储路径
    Temp_Path = db.Column(db.String(50))
    # 手动调用接口地址
    Manual_Call_URL = db.Column(db.String(500))
    # 内容超长处理方式(1-报错,2-截断)
    Value_Overlenth_Handle = db.Column(db.Integer, default=1)


class NAVTableFieldSetup(db.Model):
    __tablename__ = "NAV_Table_Field_Setup"
    # 表名称
    Table_Name = db.Column(db.String(50), nullable=False, primary_key=True, comment="表名称")
    # 字段名称
    Field_Name = db.Column(db.String(50), nullable=False, primary_key=True, comment="字段名称")
    # 字段类型(1 - String, 2 - Int, 3 - Decimal, 4 - Date, 5 - Datetime)
    Type = db.Column(db.Integer, nullable=False, default=1, comment="字段类型(1 - String, 2 - Int, 3 - Decimal, 4 - Date, 5 - Datetime)")
    # 是否主键(0 - 否, 1 - 是)
    Primary_Key = db.Column(db.Integer, nullable=False, default=0, comment="是否主键(0 - 否, 1 - 是)")
    # 主键生成方法(0 - 什么也不做, 1 - 最后号码 + 1)
    PK_Generate_Method = db.Column(db.Integer, nullable=False, default=0, comment="主键生成方法(0 - 什么也不做, 1 - 最后号码 + 1)")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")
