#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime

from sqlalchemy import func
from sqlalchemy.orm import foreign, remote

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
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000", comment="处理时间")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    # 状态(INIT, PROCESSING, ERROR, COMPLETED), 初始插入数据INIT
    Status = db.Column(db.String(10), nullable=False, default="INIT", comment="状态(INIT, PROCESSING, ERROR, COMPLETED), 初始插入数据INIT")
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default='', comment="错误消息, 初始插入数据时插入空字符('')")
    # XML文件名，如使用的是WEB API则插入空字符('')
    XMLFileName = db.Column(db.String(250), nullable=False, comment="XML文件名")
    # 客户供应商记录数，对应CustVendorInfo文件或接口
    Customer_Vendor_Total_Count = db.Column("[Customer_Vendor Total Count]", db.Integer, nullable=False, comment="客户供应商记录数，对应CustVendorInfo文件或接口")
    # 发票记录数, 对应Invoice文件或接口
    Invoice_Total_Count = db.Column("[Invoice Total Count]", db.Integer, nullable=False, comment="发票记录数, 对应Invoice文件或接口")
    # 类型(0 - CustVendInfo, 1 - FA, 2 - Invoice, 3 - Other)
    Type = db.Column(db.Integer, nullable=False, comment="类型(0 - CustVendInfo, 1 - FA, 2 - Invoice, 3 - Other)")
    # Other记录数, 对应Other文件或接口
    Other_Transaction_Total_Count = db.Column("[Other Transaction Total Count]", db.Integer, nullable=False, comment="Other记录数, 对应Other文件或接口")
    # FA记录数, 对应FA文件或接口
    FA_Total_Count = db.Column("[FA Total Count]", db.Integer, nullable=False, comment="FA记录数, 对应FA文件或接口")

    def __repr__(self):
        return "EntryNo = %s: <DMSCode: %s, CompanyCode: %s>" %\
               (self.Entry_No_, self.DMSCode, self.CompanyCode)

    # 获取最大id然后+1
    def getLatestEntryNo(self):
        max_entry_id = db.session.query(func.max(self.__class__.Entry_No_)).scalar()
        # max_entry_id = 0
        return max_entry_id + 1 if max_entry_id is not None else 1


class CustVendBuffer(db.Model):
    __tablename__ = "CustVendBuffer"
    # 非自增字段
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, comment="非自增字段")
    No_ = db.Column(db.String(20), default='', nullable=False)
    Name = db.Column(db.String(50), default='', nullable=False)
    Address = db.Column(db.String(50), default='', nullable=False)
    City = db.Column(db.String(30), default='', nullable=False)
    Post_Code = db.Column("[Post Code]", db.String(20), default='', nullable=False)
    # 默认值为'CN-0086'
    Country = db.Column(db.String(10), nullable=False, default="CN-0086")
    # 如果值为'RMB', 则插入空字符('')
    Currency = db.Column(db.String(10), nullable=False, default='', comment="FA记录数, 对应FA文件或接口")
    # 插入空字符('')
    Gen_Bus_Posting_Group = db.Column("[Gen_ Bus_ Posting Group]", db.String(10), nullable=False, default='')
    # 插入空字符('')
    VAT_Bus_Posting_Group = db.Column("[VAT Bus_ Posting Group]", db.String(10), nullable=False, default='')
    # 插入空字符('')
    Cust_VendPostingGroup = db.Column(db.String(10), nullable=False, default="")
    Application_Method = db.Column("[Application Method]", db.String(20), nullable=False, default='')
    PaymentTermsCode = db.Column(db.String(10), nullable=False, default='')
    Template = db.Column(db.String(20), nullable=False, default='')
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, nullable=False)
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default="")
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False, default=str(datetime.datetime.now()), comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000", comment="处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')")
    # 类型(0 - Customer, 1 - Vendor, 3 - Unknow)
    Type = db.Column(db.Integer, nullable=False, default=1, comment="类型(0 - Customer, 1 - Vendor, 3 - Unknow)")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, comment="处理人", default='')
    Address_2 = db.Column("[Address 2]", db.String(50), nullable=False, default='')
    PhoneNo = db.Column(db.String(30), nullable=False, default='')
    FaxNo = db.Column(db.String(30), nullable=False, default='')
    Blocked = db.Column(db.String(10), nullable=False, default='')
    Email = db.Column(db.String(50), nullable=False, default='')
    ARAPAccountNo = db.Column(db.String(50), nullable=False, default='')
    PricesIncludingVAT = db.Column(db.Integer, nullable=False, default='')
    PaymentMethodCode = db.Column(db.String(20), nullable=False, default='')
    Cost_Center_Code = db.Column("[Cost Center Code]", db.String(20), nullable=False, default='')
    ICPartnerCode = db.Column(db.String(50), nullable=False, default='')

    entry = db.relationship("InterfaceInfo",
                            primaryjoin=foreign(Entry_No_) == remote(InterfaceInfo.Entry_No_))

    def __repr__(self):
        return "[Record ID]=%d: <'Type': '%s', 'No': '%s', 'Name': '%s', [Entry No_]: '%s'>" \
               % (self.Record_ID, self.Type, self.No_, self.Name, self.Entry_No_)

    # 来源字段和对象字段不一致的特殊情况
    def __setattr__(self, key, value):
        if key == "No":
            self.__dict__["No_"] = value
        elif key == "Postcode":
            self.__dict__["Post_Code"] = value
        elif key == "ApplicationMethod":
            self.__dict__["Application_Method"] = value
        elif key == "Address2":
            self.__dict__["Address_2"] = value
        elif key == "CostCenterCode":
            self.__dict__["Cost_Center_Code"] = value
        elif key == "Type" and value == "Customer":
            self.__dict__["Type"] = 0
        elif key == "Type" and value == "Vendor":
            self.__dict__["Type"] = 1
        elif key == "Type":
            self.__dict__["Type"] = 2
        else:
            self.__dict__[key] = value

    # 获得当前最大的主键并+1返回
    def getLatestRecordId(self):
        max_record_id = db.session.query(func.max(self.__class__.Record_ID)).scalar()
        return max_record_id + 1 if max_record_id is not None else 1


class FABuffer(db.Model):
    __tablename__ = "FABuffer"
    # 非自增主键
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    FANo_ = db.Column(db.String(20), default='', nullable=False)
    Description = db.Column(db.String(30), default='', nullable=False)
    SerialNo = db.Column(db.String(30), default='', nullable=False)
    Inactive = db.Column(db.Integer, default=0, nullable=False)
    Blocked = db.Column(db.Integer, default=0, nullable=False)
    FAClassCode = db.Column(db.String(10), default='', nullable=False)
    FASubclassCode = db.Column(db.String(10), default='', nullable=False)
    FALocationCode = db.Column(db.String(10), default='', nullable=False)
    BudgetedAsset = db.Column(db.Integer, default=0, nullable=False)
    VendorNo = db.Column(db.String(20), default='', nullable=False)
    MaintenanceVendorNo = db.Column(db.String(20), default='', nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, nullable=False)
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default='', comment="错误消息")
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, default=str(datetime.datetime.now()), nullable=False, comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000", comment="处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')")
    UnderMaintenance = db.Column(db.Integer, nullable=False)
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人, 初始插入数据时插入空字符('')")
    # 如文件或接口里没有值, 初始插入数据时插入('1753-01-01 00:00:00.000')
    NextServiceDate = db.Column(db.DateTime, nullable=False, default="1753-01-01 00:00:00.000")
    # 如文件或接口里没有值, 初始插入数据时插入('1753-01-01 00:00:00.000')
    WarrantyDate = db.Column(db.DateTime, nullable=False, default="1753-01-01 00:00:00.000")
    DepreciationPeriod = db.Column(db.Integer, default=0, nullable=False)
    DepreciationStartingDate = db.Column(db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    CostCenterCode = db.Column(db.String(20), default='', nullable=False)

    entry = db.relationship("InterfaceInfo",
                            primaryjoin=foreign(Entry_No_) == remote(InterfaceInfo.Entry_No_))

    # 来源字段和对象字段不一致的特殊情况
    def __setattr__(self, key, value):
        if key == "FANo":
            self.__dict__["FANo_"] = value
        else:
            self.__dict__[key] = value

    # 获得当前最大的主键并+1返回
    def getLatestRecordId(self):
        max_record_id = db.session.query(func.max(self.__class__.Record_ID)).scalar()
        return max_record_id + 1 if max_record_id is not None else 1


class InvoiceHeaderBuffer(db.Model):
    __tablename__ = "InvoiceHeaderBuffer"
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    InvoiceNo = db.Column(db.String(20), default='', nullable=False)
    Posting_Date = db.Column("[Posting Date]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    Document_Date = db.Column("[Document Date]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    Due_Date = db.Column("[Due Date]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    PayToBillToNo = db.Column(db.String(20), default='', nullable=False)
    SellToBuyFromNo = db.Column(db.String(20), default='', nullable=False)
    CostCenterCode = db.Column(db.String(20), default='', nullable=False)
    VehicleSeries = db.Column(db.String(20), default='', nullable=False)
    ExtDocumentNo = db.Column(db.String(30), default='', nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, default=0, nullable=False)
    InvoiceType = db.Column(db.String(10), default='', nullable=False)
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_handled = db.Column("[DateTime handled]", db.DateTime, nullable=False, default='1753-01-01 00:00:00.000', comment="处理时间")
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default='', comment="错误消息")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    # 发票行里的记录数
    Line_Total_Count = db.Column("[Line Total Count]", db.Integer, default=0, nullable=False, comment="发票行里的记录数")
    PriceIncludeVAT = db.Column(db.Integer, default=0, nullable=False)
    Description = db.Column(db.String(100), default='', nullable=False)
    Location = db.Column(db.String(20), default='', nullable=False)

    entry = db.relationship("InterfaceInfo",
                            primaryjoin=foreign(Entry_No_) == remote(InterfaceInfo.Entry_No_))

    # 来源字段和对象字段不一致的特殊情况
    def __setattr__(self, key, value):
        if key == "No":
            self.__dict__["No_"] = value
        elif key == "PostingDate":
            self.__dict__["Posting_Date"] = value
        elif key == "DocumentDate":
            self.__dict__["Document_Date"] = value
        elif key == "DueDate":
            self.__dict__["Due_Date"] = value
        else:
            self.__dict__[key] = value

    # 获得当前最大的主键并+1返回
    def getLatestRecordId(self):
        max_record_id = db.session.query(func.max(self.__class__.Record_ID)).scalar()
        return max_record_id + 1 if max_record_id is not None else 1


class InvoiceLineBuffer(db.Model):
    __tablename__ = "InvoiceLineBuffer"
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    Line_No_ = db.Column("[Line No_]", db.Integer, default=0, nullable=False)
    DMSItemType = db.Column(db.String(20), default="", nullable=False)
    GLAccount = db.Column(db.String(50), default="", nullable=False)
    Description = db.Column(db.String(100), default="", nullable=False)
    CostCenterCode = db.Column(db.String(20), default="", nullable=False)
    VehicleSeries = db.Column(db.String(20), default="", nullable=False)
    VIN = db.Column(db.String(20), default="", nullable=False)
    Quantity = db.Column(db.DECIMAL(38, 20), default=0, nullable=False)
    Line_Amount = db.Column("[Line Amount]", db.DECIMAL(38, 20), default=0, nullable=False)
    LineCost = db.Column(db.DECIMAL(38, 20), default=0, nullable=False)
    TransactionType = db.Column(db.String(20), default="", nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, default=0, nullable=False)
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), default="", nullable=False, comment="错误消息")
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, default=str(datetime.datetime.now()), nullable=False, comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default='1753-01-01 00:00:00.000', comment="处理时间")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    # Link to Table: InvoiceHeaderBuffer
    InvoiceNo = db.Column(db.String(20), default="", nullable=False)
    Line_Discount_Amount = db.Column("[Line Discount Amount]", db.DECIMAL(38, 20), default=0, nullable=False)
    WIP_No_ = db.Column("[WIP No_]", db.String(20), default="", nullable=False)
    Line_VAT_Amount = db.Column("[Line VAT Amount]", db.DECIMAL(38, 20), default=0, nullable=False)
    Line_VAT_Rate = db.Column("[Line VAT Rate]", db.DECIMAL(38, 20), default=0, nullable=False)
    FromCompanyName = db.Column(db.String(50), default="", nullable=False)
    ToCompanyName = db.Column(db.String(50), default="", nullable=False)
    Location = db.Column(db.String(20), default="", nullable=False)
    MovementType = db.Column(db.String(20), default="", nullable=False)
    OEMCode = db.Column(db.String(20), default="", nullable=False)

    entry = db.relationship("InterfaceInfo",
                            primaryjoin=foreign(Entry_No_) == remote(InterfaceInfo.Entry_No_))
    invoiceHeader = db.relationship("InvoiceHeaderBuffer",
                                    primaryjoin=foreign(InvoiceNo) == remote(InvoiceHeaderBuffer.InvoiceNo))

    # 来源字段和对象字段不一致的特殊情况
    def __setattr__(self, key, value):
        if key == "LineNo":
            self.__dict__["Line_No_"] = value
        elif key == "VINNo":
            self.__dict__["VIN"] = value
        elif key == "QTY":
            self.__dict__["Quantity"] = value
        elif key == "LineAmount":
            self.__dict__["Line_Amount"] = value
        elif key == "LineDiscountAmount":
            self.__dict__["Line_Discount_Amount"] = value
        elif key == "WIPNo":
            self.__dict__["WIP_No_"] = value
        elif key == "LineVATAmount":
            self.__dict__["Line_VAT_Amount"] = value
        elif key == "LineVATRate":
            self.__dict__["Line_VAT_Rate"] = value
        else:
            self.__dict__[key] = value

    # 获得当前最大的主键并+1返回
    def getLatestRecordId(self):
        max_record_id = db.session.query(func.max(self.__class__.Record_ID)).scalar()
        return max_record_id + 1 if max_record_id is not None else 1


class OtherBuffer(db.Model):
    __tablename__ = "OtherBuffer"
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    DocumentNo_ = db.Column(db.String(20), default="", nullable=False)
    TransactionType = db.Column(db.String(20), default="", nullable=False)
    Line_No_ = db.Column("[Line No_]", db.Integer, default=0, nullable=False)
    Posting_Date = db.Column("[Posting Date]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    Document_Date = db.Column("[Document Date]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    ExtDocumentNo_ = db.Column(db.String(20), default="", nullable=False)
    Account_No_ = db.Column("[Account No_]", db.String(50), default="", nullable=False)
    Description = db.Column(db.String(100), default="", nullable=False)
    Debit_Value = db.Column("[Debit Value]", db.DECIMAL(38, 20), default=0, nullable=False)
    Credit_Value = db.Column("[Credit Value]", db.DECIMAL(38, 20), default=0, nullable=False)
    CostCenterCode = db.Column(db.String(20), default="", nullable=False)
    VehicleSeries = db.Column(db.String(20), default="", nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, default=0, nullable=False)
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, default=str(datetime.datetime.now()), nullable=False)
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_handled = db.Column("[DateTime handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000'", comment="处理时间")
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default="", comment="错误消息")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    AccountType = db.Column(db.String(20), default="", nullable=False)
    WIP_No_ = db.Column("[WIP No_]", db.String(20), default="", nullable=False)
    FA_Posting_Type = db.Column("[FA Posting Type]", db.String(20), default="", nullable=False)
    EntryType = db.Column(db.String(20), default="", nullable=False)
    FromCompanyName = db.Column(db.String(50), default="", nullable=False)
    ToCompanyName = db.Column(db.String(50), default="", nullable=False)
    VIN = db.Column(db.String(20), default="", nullable=False)
    SourceType = db.Column(db.String(20), default="", nullable=False)
    SourceNo = db.Column(db.String(30), default="", nullable=False)
    # 初始插入数据时插入0
    NotDuplicated = db.Column(db.Integer, nullable=False, default=0)
    # 初始插入数据时插入空字符('')
    NAVDocumentNo_ = db.Column(db.String(20), nullable=False, default='')
    DMSItemType = db.Column(db.String(20), default="", nullable=False)
    DMSItemTransType = db.Column(db.String(20), default="", nullable=False)
    Location = db.Column(db.String(20), default="", nullable=False)

    entry = db.relationship("InterfaceInfo",
                            primaryjoin=foreign(Entry_No_) == remote(InterfaceInfo.Entry_No_))

    # 来源字段和对象字段不一致的特殊情况
    def __setattr__(self, key, value):
        if key == "DaydookNo":
            self.__dict__["DocumentNo_"] = value
        elif key == "LineNo":
            self.__dict__["Line_No_"] = value
        elif key == "PostingDate":
            self.__dict__["Posting_Date"] = value
        elif key == "DocumentDate":
            self.__dict__["Document_Date"] = value
        elif key == "ExtDocumentNo":
            self.__dict__["ExtDocumentNo_"] = value
        elif key == "AccountNo":
            self.__dict__["Account_No_"] = value
        elif key == "DebitValue":
            self.__dict__["Debit_Value"] = value
        elif key == "CreditValue":
            self.__dict__["Credit_Value"] = value
        elif key == "WIPNo":
            self.__dict__["WIP_No_"] = value
        elif key == "FAPostingType":
            self.__dict__["FA_Posting_Type"] = value
        elif key == "VINNo":
            self.__dict__["VIN"] = value
        else:
            self.__dict__[key] = value

    # 获得当前最大的主键并+1返回
    def getLatestRecordId(self):
        max_record_id = db.session.query(func.max(self.__class__.Record_ID)).scalar()
        return max_record_id + 1 if max_record_id is not None else 1


