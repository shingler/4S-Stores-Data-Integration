#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import db


class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"
    # 非自增字段（[Entry No_]）
    Entry_No_ = db.Column("[Entry No_]", db.Integer, nullable=False, primary_key=True, comment="非自增字段")
    DMSCode = db.Column(db.String(20), nullable=False)
    DMSTitle = db.Column(db.String(50), nullable=False)
    CompanyCode = db.Column(db.String(20), nullable=False)
    CompanyTitle = db.Column(db.String(50), nullable=False)
    CreateDateTime = db.Column(db.DateTime, nullable=False)
    Creator = db.Column(db.String(30), nullable=False)
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False, comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, comment="处理时间")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, comment="处理人")
    # 状态(INIT, PROCESSING, ERROR, COMPLETED), 初始插入数据INIT
    Status = db.Column(db.String(10), nullable=False, comment="状态(INIT, PROCESSING, ERROR, COMPLETED), 初始插入数据INIT")
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, comment="错误消息, 初始插入数据时插入空字符('')")
    # XML文件名，如使用的是WEB API则插入空字符('')
    XMLFileName = db.Column(db.String(250), nullable=False, comment="XML文件名")
    # 客户供应商记录数，对应CustVendorInfo文件或接口
    Customer_Vendor_Total_Count = db.Column("[Customer_Vendor Total Count]", db.Integer, nullable=False, comment="客户供应商记录数，对应CustVendorInfo文件或接口")
    # 发票记录数, 对应Invoice文件或接口
    # 类型(0 - CustVendInfo, 1 - FA, 2 - Invoice, 3 - Other)
    Type = db.Column(db.Integer, nullable=False, comment="类型(0 - CustVendInfo, 1 - FA, 2 - Invoice, 3 - Other)")
    # Other记录数, 对应Other文件或接口
    Other_Transaction_Total_Count = db.Column("[Other Transaction Total Count]", db.Integer, nullable=False, comment="Other记录数, 对应Other文件或接口")
    # FA记录数, 对应FA文件或接口
    FA_Total_Count = db.Column("[FA Total Count]", db.Integer, nullable=False, comment="FA记录数, 对应FA文件或接口")
    

class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"


class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"


class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"


class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"


class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"


class InterfaceInfo(db.Model):
    __tablename__ = "DMSInterfaceInfo"