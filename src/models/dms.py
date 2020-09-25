#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
from src import db


class Company(db.Model):
    __tablename__ = "DMS_Company_List"
    # 公司代码
    Code = db.Column(db.String(20), primary_key=True, autoincrement=False, comment="公司代码")
    # 公司名称
    Name = db.Column(db.String(200), nullable=True, default="", comment="公司名称")
    # 品牌
    Brand = db.Column(db.String(20), nullable=True, default="", comment="品牌")
    # 启用DMS接口
    DMS_Interface_Activated = db.Column(db.Boolean, nullable=False, default=False, comment="启用DMS接口")
    # DMS里的公司代码
    DMS_Company_Code = db.Column(db.String(20), nullable=True, default="", comment="DMS里的公司代码")
    # DMS里的公司名称
    DMS_Company_Name = db.Column(db.String(100), nullable=True, default="", comment="DMS里的公司名称")
    # DMS经销商集团代码
    DMS_Group_Code = db.Column(db.String(20), nullable=True, default="", comment="DMS经销商集团代码")
    # 数据库名称
    NAV_DB_Name = db.Column(db.String(50), nullable=True, default="", comment="数据库名称")
    # 数据库地址
    NAV_DB_Address = db.Column(db.String(100), nullable=True, default="", comment="数据库地址")
    # 数据库登陆用户ID
    NAV_DB_UserID = db.Column(db.String(50), nullable=True, default="", comment="数据库登陆用户ID")
    # 数据库登陆密码
    NAV_DB_Password = db.Column(db.String(50), nullable=True, default="", comment="数据库登陆密码")
    # NAV里的公司代码(NAV里的数据表名有公司代码前缀, e.g.[K302 Zhuhai JJ$DMSInterfaceInfo])
    NAV_Company_Code = db.Column(db.String(50), nullable=True, default="", comment="NAV里的公司代码")
    # NAV里的公司名称
    NAV_Company_Name = db.Column(db.String(100), nullable=True, default="", comment="NAV里的公司名称")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")
    # NAV WEB Service用户ID
    NAV_WEB_UserID = db.Column(db.String(50), nullable=True, comment="NAV WEB Service用户ID")
    # NAV WEB Service密码
    NAV_WEB_Password = db.Column(db.String(50), nullable=True, comment="NAV WEB Service密码")


class ApiSetup(db.Model):
    __tablename__ = "DMS_API_Setup"
    # 公司代码(Link to table: DMS_Company_List)
    Company_Code = db.Column(db.String(20), db.ForeignKey("DMS_Company_List.Code"), nullable=False, primary_key=True, comment="公司代码")
    # 接口代码
    API_Code = db.Column(db.String(100), nullable=False, primary_key=True, comment="接口代码")
    # 接口名称
    API_Name = db.Column(db.String(100), nullable=False, comment="接口名称")
    # 接口类型(1 - Web API, 2 - XML File)
    API_Type = db.Column(db.Integer, nullable=False, default=2, comment="接口类型")
    # 接口地址(主), 如果接口类型为2 - XML File, 该字段内容为XML文件的存储路径
    API_Address1 = db.Column(db.String(500), nullable=False, comment="接口地址(主)")
    # 接口地址(备), 如果接口类型为2 - XML File, 该字段内容为XML文件的存储路径
    API_Address2 = db.Column(db.String(500), nullable=False, comment="接口地址(备)")
    # 命令代码
    Command_Code = db.Column(db.String(20), nullable=True, comment="命令代码")
    # 数据格式(1 - JSON, 2 - XML)
    Data_Format = db.Column(db.Integer, nullable=True, comment="数据格式")
    # 签名版本
    Signature_Verision = db.Column(db.String(20), nullable=True, comment="签名版本")
    # 签名方法
    Signature_Method = db.Column(db.String(50), nullable=True, comment="签名方法")
    # 签名信息
    Signature = db.Column(db.String(200), nullable=True, comment="签名信息")
    # 启用接口
    Activated = db.Column(db.Boolean, nullable=False, default=False, comment="启用接口")
    # 如果接口类型为2 - XML File, 该字段内容为XML文件名的格式(e.g.YYYYMMDD_CustVendInfo.XML)
    File_Name_Format = db.Column(db.String(100), nullable=True, comment="XML文件名的格式")
    # 启用邮件提醒
    Notification_Activated = db.Column(db.Boolean, nullable=False, default=False, comment="启用邮件提醒")
    # 回调地址
    CallBack_Address = db.Column(db.String(200), nullable=True, comment="回调地址")
    # 超时时间(单位: 分钟)
    Time_out = db.Column(db.Integer, nullable=False, default=0, comment="超时时间(单位: 分钟)")
    # XML文件最大容量(单位: M兆)
    File_Max_Size = db.Column(db.Integer, nullable=False, default=0, comment="XML文件最大容量(单位: M兆)")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=True, comment="最后修改人")
    # XML文件成功导入后的归档地址
    Archived_Path = db.Column(db.String(500), nullable=True, comment="XML文件成功导入后的归档地址")

    company = db.relationship("Company", backref="ApiSetup")


class ApiPInSetup(db.Model):
    __tablename__ = "DMS_API_P_In_Setup"
    # 公司代码(Link to table: DMS_API_Setup)
    Company_Code = db.Column(db.String(20), nullable=False, primary_key=True, autoincrement=False, comment="公司代码")
    # 接口代码(Link to table: DMS_API_Setup)
    API_Code = db.Column(db.String(100), nullable=False, primary_key=True, autoincrement=False, comment="接口代码")
    # 参数代码
    P_Code = db.Column(db.String(100), nullable=False, primary_key=True, autoincrement=False, comment="参数代码")
    # 参数名称(与JSON里的标签一致)
    P_Name = db.Column(db.String(200), nullable=False, comment="参数名称(与JSON里的标签一致)")
    # 顺序号
    Sequence = db.Column(db.Integer, nullable=True, comment="顺序号")
    # 参数值类型(1 - String, 2 - Int, 3 - Decimal, 4 - Date, 5 - Datetime, 6 - Array)
    Value_Type = db.Column(db.Integer, nullable=True, comment="参数值类型(1 - String, 2 - Int, 3 - Decimal, 4 - Date, 5 - Datetime, 6 - Array)")
    # 参数值来源(1 - 固定值, 2 - 公式[CD:当天日期, CDT:当前日期时间, TDTB:当天0点, TDTE:当天24点, 等等])
    Value_Source = db.Column(db.Integer, nullable=True, comment="参数值来源(1 - 固定值, 2 - 公式[CD:当天日期, CDT:当前日期时间, TDTB:当天0点, TDTE:当天24点, 等等])")
    # 参数值
    Value = db.Column(db.String(100), nullable=True, comment="参数值")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")

    # __table_args__ = (
    #     ForeignKeyConstraint(["Company_Code", "API_Code"], ["DMS_API_Setup.Company_Code", "DMS_API_Setup.API_Code"])
    # )
    apiSetup = db.relationship("ApiSetup", primaryjoin="(DMS_API_P_In_Setup.Company_Code == DMS_API_Setup.Company_Code) \
                && (DMS_API_P_In_Setup.API_Code == DMS_API_Setup.API_Code)")


class ApiPOutSetup(db.Model):
    __tablename__ = "DMS_API_P_Out_Setup"
    # 公司代码(Link to table: DMS_API_Setup)
    Company_Code = db.Column(db.String(20), nullable=False, primary_key=True, autoincrement=False, comment="公司代码")
    # 接口代码(Link to table: DMS_API_Setup)
    API_Code = db.Column(db.String(100), nullable=False, primary_key=True, autoincrement=False, comment="接口代码")
    # 顺序号
    Sequence = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=False, comment="顺序号")
    # 参数代码
    P_Code = db.Column(db.String(100), nullable=False, comment="参数代码")
    # 参数名称(与JSON或者XML文件里的标签一致)
    P_Name = db.Column(db.String(200), nullable=False, comment="参数名称(与JSON或者XML文件里的标签一致)")
    # 层级(0 - 根, 1 - 1级), 仅支持3层数据结构
    Level = db.Column(db.Integer, nullable=False, default=0, comment="层级")
    # 父节点名称
    Parent_Node_Name = db.Column(db.String(200), nullable=True, comment="父节点名称")
    # 参数值类型(1 - String, 2 - Int, 3 - Decimal, 4 - Date, 5 - Datetime, 6 - Array)
    Value_Type = db.Column(db.Integer, nullable=True, default=1, comment="参数值类型")
    # NAV数据表名称(存储接口中的数据, e.g.DMSInterfaceInfo)
    Table_Name = db.Column(db.String(100), nullable=True, comment="NAV数据表名称(存储接口中的数据, e.g.DMSInterfaceInfo)")
    # 字段名称
    Column_Name = db.Column(db.String(100), nullable=False, comment="字段名称")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")

    apiSetup = db.relationship("ApiSetup", primaryjoin="(DMS_API_P_Out_Setup.Company_Code == DMS_API_Setup.Company_Code) \
                    && (DMS_API_P_Out_Setup.API_Code == DMS_API_Setup.API_Code)")


class NotificationUser(db.Model):
    __tablename__ = "DMS_Notification_User"
    # 公司代码(Link to table: DMS_Company_List)
    Company_Code = db.Column(db.String(20), nullable=False, primary_key=True, autoincrement=False, comment="公司代码")
    # 用户名
    User_Name = db.Column(db.String(50), nullable=False, primary_key=True, autoincrement=False, comment="用户名")
    # 邮件地址
    Email_Address = db.Column(db.String(200), nullable=False, comment="邮件地址")
    # 启用
    Activated = db.Column(db.Boolean, nullable=False, comment="启用")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")

    company = db.relationship("Company", backref="notificationUser")


class ApiTaskSetup(db.Model):
    __tablename__ = "DMS_API_Task_Setup"
    # 公司代码(Link to table: DMS_API_Setup)
    Company_Code = db.Column(db.String(20), nullable=False, primary_key=True, autoincrement=False, comment="公司代码")
    # 顺序号
    Sequence = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=False, comment="顺序号")
    # 任务名称
    Task_Name = db.Column(db.String(100), nullable=True, comment="任务名称")
    # 需执行的API代码
    API_Code = db.Column(db.String(100), nullable=False, comment="需执行的API代码")
    # 执行时间
    Execute_Time = db.Column(db.Time, nullable=False, comment="执行时间")
    # 失败处理(1 - Nothing, 2 - Retry, 3 - Retry & Notify)
    Fail_Handle = db.Column(db.Integer, nullable=False, comment="失败处理(1 - Nothing, 2 - Retry, 3 - Retry & Notify)")
    # 最后修改时间
    Last_Modified_DT = db.Column(db.DateTime, nullable=False, comment="最后修改时间")
    # 最后修改人
    Last_Modified_By = db.Column(db.String(20), nullable=False, comment="最后修改人")
    # 重复时间间隔（每天，每2天，每7天等等，e.g. 值为3, 意思是每3天执行一次）
    Recurrence_Day = db.Column(db.Integer, nullable=False, comment="重复时间间隔（每天，每2天，每7天等等，e.g. 值为3, 意思是每3天执行一次）")
    # 上次成功执行时间
    Last_Executed_Time = db.Column(db.DateTime, nullable=False, comment="上次成功执行时间")

    setup = db.relationship("ApiSetup", backref="task")