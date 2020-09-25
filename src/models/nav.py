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


class CustVendBuffer(db.Model):
    __tablename__ = "CustVendBuffer"
    # 非自增字段
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, comment="非自增字段")
    No_ = db.Column(db.String(20), nullable=False)
    Name = db.Column(db.String(50), nullable=False)
    Address = db.Column(db.String(50), nullable=False)
    City = db.Column(db.String(30), nullable=False)
    Post_Code = db.Column("[Post Code]", db.String(20), nullable=False)
    # 默认值为'CN-0086'
    Country = db.Column(db.String(10), nullable=False, default="CN-0086")
    # 如果值为'RMB', 则插入空字符('')
    Currency = db.Column(db.String(10), nullable=False, comment="FA记录数, 对应FA文件或接口")
    # 插入空字符('')
    Gen_Bus_Posting_Group = db.Column("[Gen_ Bus_ Posting Group]", db.String(10), nullable=False, default='')
    # 插入空字符('')
    VAT_Bus_Posting_Group = db.Column("[VAT Bus_ Posting Group]", db.String(10), nullable=False, default='')
    # 插入空字符('')
    Cust_VendPostingGroup = db.Column(db.String(10), nullable=False, default="")
    Application_Method = db.Column("[Application Method]", db.String(20), nullable=False)
    PaymentTermsCode = db.Column(db.String(10), nullable=False)
    Template = db.Column(db.String(20), nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, db.ForeignKey("DMSInterfaceInfo."), nullable=False)
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default="")
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False, comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000", comment="处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')")
    # 类型(0 - Customer, 1 - Vendor, 3 - Unknow)
    Type = db.Column(db.Integer, nullable=False, comment="类型(0 - Customer, 1 - Vendor, 3 - Unknow)")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, comment="F处理人, [Entry No_]初始插入数据时插入空字符('')", default='')
    Address_2 = db.Column("[Address 2]", db.String(50), nullable=False)
    PhoneNo = db.Column(db.String(30), nullable=False)
    FaxNo = db.Column(db.String(30), nullable=False)
    Blocked = db.Column(db.String(10), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    ARAPAccountNo = db.Column(db.String(50), nullable=False)
    PricesIncludingVAT = db.Column(db.Integer, nullable=False)
    PaymentMethodCode = db.Column(db.String(20), nullable=False)
    Cost_Center_Code = db.Column("[Cost Center Code]", db.String(20), nullable=False)
    ICPartnerCode = db.Column(db.String(50), nullable=False)

    entry = db.relationship("InterfaceInfo")

class FABuffer(db.Model):
    __tablename__ = "FABuffer"
    # 非自增主键
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    FANo_ = db.Column(db.String(20), nullable=False)
    Description = db.Column(db.String(30), nullable=False)
    SerialNo = db.Column(db.String(30), nullable=False)
    Inactive = db.Column(db.Integer, nullable=False)
    Blocked = db.Column(db.Integer, nullable=False)
    FAClassCode = db.Column(db.String(10), nullable=False)
    FASubclassCode = db.Column(db.String(10), nullable=False)
    FALocationCode = db.Column(db.String(10), nullable=False)
    BudgetedAsset = db.Column(db.Integer, nullable=False)
    VendorNo = db.Column(db.String(20), nullable=False)
    MaintenanceVendorNo = db.Column(db.String(20), nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, db.ForeignKey("DMSInterfaceInfo.[Entry No_]"), nullable=False)
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default='', comment="错误消息")
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False, comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000", comment="处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')")
    UnderMaintenance = db.Column(db.Integer, nullable=False)
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人, 初始插入数据时插入空字符('')")
    # 如文件或接口里没有值, 初始插入数据时插入('1753-01-01 00:00:00.000')
    NextServiceDate = db.Column(db.DateTime, nullable=False, default="1753-01-01 00:00:00.000")
    # 如文件或接口里没有值, 初始插入数据时插入('1753-01-01 00:00:00.000')
    WarrantyDate = db.Column(db.DateTime, nullable=False, default="1753-01-01 00:00:00.000")
    DepreciationPeriod = db.Column(db.Integer, nullable=False)
    DepreciationStartingDate = db.Column(db.DateTime, nullable=False)
    CostCenterCode = db.Column(db.String(20), nullable=False)

    entry = db.relationship("InterfaceInfo")


class InvoiceHeaderBuffer(db.Model):
    __tablename__ = "InvoiceHeaderBuffer"
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    InvoiceNo = db.Column(db.String(20), nullable=False)
    Posting_Date = db.Column("[Posting Date]", db.DateTime, nullable=False)
    Document_Date = db.Column("[Document Date]", db.DateTime, nullable=False)
    Due_Date = db.Column("[Due Date]", db.DateTime, nullable=False)
    PayToBillToNo = db.Column(db.String(20), nullable=False)
    SellToBuyFromNo = db.Column(db.String(20), nullable=False)
    CostCenterCode = db.Column(db.String(20), nullable=False)
    VehicleSeries = db.Column(db.String(20), nullable=False)
    ExtDocumentNo = db.Column(db.String(30), nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, db.ForeignKey("DMSInterfaceInfo.[Entry No_]"), nullable=False)
    InvoiceType = db.Column(db.String(10), nullable=False)
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False)
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_handled = db.Column("[DateTime handled]", db.DateTime, nullable=False, default='1753-01-01 00:00:00.000', comment="处理时间")
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default='', comment="错误消息")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    # 发票行里的记录数
    Line_Total_Count = db.Column("[Line Total Count]", db.Integer, nullable=False, comment="发票行里的记录数")
    PriceIncludeVAT = db.Column(db.Integer, nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    Location = db.Column(db.String(20), nullable=False)

    entry = db.relationship("InterfaceInfo")


class InvoiceLineBuffer(db.Model):
    __tablename__ = "InvoiceLineBuffer"
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    Line_No_ = db.Column("[Line No_]", db.Integer, nullable=False)
    DMSItemType = db.Column(db.String(20), nullable=False)
    GLAccount = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    CostCenterCode = db.Column(db.String(20), nullable=False)
    VehicleSeries = db.Column(db.String(20), nullable=False)
    VIN = db.Column(db.String(20), nullable=False)
    Quantity = db.Column(db.DECIMAL(38, 20), nullable=False)
    Line_Amount = db.Column("[Line Amount]", db.DECIMAL(38, 20), nullable=False)
    LineCost = db.Column(db.DECIMAL(38, 20), nullable=False)
    TransactionType = db.Column(db.String(20), nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, db.ForeignKey("DMSInterfaceInfo.[Entry No_]"), nullable=False)
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default='', comment="错误消息")
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False, comment="导入时间")
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_Handled = db.Column("[DateTime Handled]", db.DateTime, nullable=False, default='1753-01-01 00:00:00.000', comment="处理时间")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    # Link to Table: InvoiceHeaderBuffer
    InvoiceNo = db.Column(db.String(20), db.ForeignKey("InvoiceHeaderBuffer.[Record ID]"), nullable=False)
    Line_Discount_Amount = db.Column("[Line Discount Amount]", db.DECIMAL(38, 20), nullable=False)
    WIP_No_ = db.Column("[WIP No_]", db.String(20), nullable=False)
    Line_VAT_Amount = db.Column("[Line VAT Amount]", db.DECIMAL(38, 20), nullable=False)
    Line_VAT_Rate = db.Column("[Line VAT Rate]", db.String(38, 20), nullable=False)
    FromCompanyName = db.Column(db.String(50), nullable=False)
    ToCompanyName = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(20), nullable=False)
    MovementType = db.Column(db.String(20), nullable=False)
    OEMCode = db.Column(db.String(20), nullable=False)

    entry = db.relationship("InterfaceInfo")
    invoiceHeader = db.relationship("InvoiceHeaderBuffer")


class OtherBuffer(db.Model):
    __tablename__ = "OtherBuffer"
    Record_ID = db.Column("[Record ID]", db.Integer, nullable=False, primary_key=True, autoincrement=False)
    DocumentNo_ = db.Column(db.String(20), nullable=False)
    TransactionType = db.Column(db.String(20), nullable=False)
    Line_No_ = db.Column("[Line No_]", db.Integer, nullable=False)
    Posting_Date = db.Column("[Posting Date]", db.DateTime, nullable=False)
    Document_Date = db.Column("[Document Date]", db.DateTime, nullable=False)
    ExtDocumentNo_ = db.Column(db.String(20), nullable=False)
    Account_No_ = db.Column("[Account No_]", db.String(50), nullable=False)
    Description = db.Column(db.String(100), nullable=False)
    Debit_Value = db.Column("[Debit Value]", db.DECIMAL(38, 20), nullable=False)
    Credit_Value = db.Column("[Credit Value]", db.DECIMAL(38, 20), nullable=False)
    CostCenterCode = db.Column(db.String(20), nullable=False)
    VehicleSeries = db.Column(db.String(20), nullable=False)
    # Link to Table: DMSInterfaceInfo
    Entry_No_ = db.Column("[Entry No_]", db.Integer, db.ForeignKey("DMSInterfaceInfo.[Entry No_]"), nullable=False)
    # 导入时间
    DateTime_Imported = db.Column("[DateTime Imported]", db.DateTime, nullable=False)
    # 处理时间, 初始插入数据时插入('1753-01-01 00:00:00.000')
    DateTime_handled = db.Column("[DateTime handled]", db.DateTime, nullable=False, default="1753-01-01 00:00:00.000'", comment="处理时间")
    # 错误消息, 初始插入数据时插入空字符('')
    Error_Message = db.Column("[Error Message]", db.String(250), nullable=False, default="", comment="错误消息")
    # 处理人, 初始插入数据时插入空字符('')
    Handled_by = db.Column("[Handled by]", db.String(20), nullable=False, default='', comment="处理人")
    AccountType = db.Column(db.String(20), nullable=False)
    WIP_No_ = db.Column("[WIP No_]", db.String(20), nullable=False)
    FA_Posting_Type = db.Column("[FA Posting Type]", db.String(20), nullable=False)
    EntryType = db.Column(db.String(20), nullable=False)
    FromCompanyName = db.Column(db.String(50), nullable=False)
    ToCompanyName = db.Column(db.String(50), nullable=False)
    VIN = db.Column(db.String(20), nullable=False)
    SourceType = db.Column(db.String(20), nullable=False)
    SourceNo = db.Column(db.String(30), nullable=False)
    # 初始插入数据时插入0
    NotDuplicated = db.Column(db.Integer, nullable=False, default=0)
    # 初始插入数据时插入空字符('')
    NAVDocumentNo_ = db.Column(db.String(20), nullable=False, default='')
    DMSItemType = db.Column(db.String(20), nullable=False)
    DMSItemTransType = db.Column(db.String(20), nullable=False)
    Location = db.Column(db.String(20), nullable=False)

    entry = db.relationship("InterfaceInfo")


