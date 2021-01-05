#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用拼接sql的方式（非建模）写入nav库
import datetime
import os
import threading
import time

from sqlalchemy import MetaData, create_engine, select, text, and_, Table, Numeric, DateTime
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Insert
from sqlalchemy.util import OrderedDict

from src import ApiPOutSetup, cast_chinese_encode
from src import to_local_time, true_or_false_to_tinyint


class NavDB:
    engine = None
    dbo = None
    conn = None
    meta = None
    base = None
    tables = {
        "CustVendBuffer": "CustVendBuffer",
        "FABuffer": "FABuffer",
        "InvoiceHeaderBuffer": "InvoiceHeaderBuffer",
        "InvoiceLineBuffer": "InvoiceLineBuffer",
        "OtherBuffer": "OtherBuffer",
        "DMSInterfaceInfo": "DMSInterfaceInfo"
    }

    DATA_TYPE_CV = 0
    DATA_TYPE_FA = 1
    DATA_TYPE_INV = 2
    DATA_TYPE_OTHER = 3

    def __init__(self, db_host, db_user, db_password, db_name, company_nav_code, only_tables=None):
        if only_tables is None:
            only_tables = []

        conn_str = "mssql+pyodbc://{1}:{2}@{0}:1433/{3}?driver=ODBC+Driver+17+for+SQL+Server".format(db_host, db_user,
                                                                                                     db_password,
                                                                                                     db_name)
        # conn_str = "mssql+pyodbc://{1}:{2}@{0}:1401/{3}?driver=ODBC+Driver+17+for+SQL+Server".format(db_host, db_user, db_password, db_name)
        engine = create_engine(conn_str)
        DBSession = sessionmaker(bind=engine)
        self.dbo = DBSession()
        self.company_nav_code = company_nav_code
        self.meta = MetaData()
        self.conn = engine.connect()
        self.engine = engine
        # 建立反射模型
        if len(only_tables) == 0:
            # 将反射模型存入类字典
            for t in self.tables:
                self.tables[t] = self._getTableName(company_nav_code, t)
            self.meta.reflect(bind=engine, only=list(self.tables.values()))
        else:
            # 自定义加载类，只能以后通过_getTableName来拿
            for i in range(len(only_tables)):
                only_tables[i] = self._getTableName(company_nav_code, only_tables[i])
            self.meta.reflect(bind=engine, only=only_tables)

    @staticmethod
    def _getTableName(company_nav_code: str, data_name) -> str:
        return "{0}${1}".format(company_nav_code, data_name)

    # 根据文件名检查是否重复导入
    def checkRepeatImport(self, path: str) -> bool:
        table_name = self._getTableName(self.company_nav_code, "DMSInterfaceInfo")
        General = self.base.classes[table_name]
        res = self.dbo.query(General).filter(General.XMLFileName.like("%{0}".format(os.path.basename(path)))).first()
        return True if res is not None else False

    def prepare(self):
        Base = automap_base(metadata=self.meta)
        Base.prepare()
        self.base = Base

    # 通过反射拿到表结构
    def getColumns(self, table_name: str) -> list:
        insp = reflection.Inspector.from_engine(self.engine)
        columns = insp.get_columns(table_name)
        return columns

    # 检查数据是否存在不合法的字段名
    # @param data_dict dict 要插入的数据
    # @param table_name str 表名
    # @return dict
    def checkFields(self, data_dict: dict, columns: list) -> dict:
        checked_dict = {}
        # 去掉表结构不存在的字段
        for dk in data_dict.keys():
            if dk in map(lambda x: x["name"], columns):
                checked_dict[dk] = data_dict[dk]
        # 为表结构存在但数据里没有的字段设置默认值（timestamp除外）
        for field in columns:
            if field["name"] not in checked_dict and isinstance(field["type"], Numeric):
                checked_dict[field["name"]] = 0
            elif field["name"] not in checked_dict and isinstance(field["type"], DateTime):
                checked_dict[field["name"]] = "1753-01-01 00:00:00.000"
            elif field["name"] not in checked_dict and field["name"] != "timestamp":
                checked_dict[field["name"]] = ""

        return checked_dict

    # 写入General部分
    def insertGeneral(self, data_dict: dict, api_p_out: dict, Type: int = 0, Count: int = 0, XMLFile: str = "",
                      **kwargs):
        # 需要转换中文编码的字段
        convert_chn_fields = ["DMSTitle", "CompanyTitle", "Creator"]
        # 非xml的数据
        other_data = {"Type": str(Type), "Customer_Vendor Total Count": 0,
                      "FA Total Count": 0, "Invoice Total Count": 0,
                      "Other Transaction Total Count": 0, "XMLFileName": XMLFile,
                      "DateTime Handled": "1753-01-01 00:00:00.000",
                      "Handled by": "", "Status": "INIT", "Error Message": ""}
        if Type == 0:
            other_data["Customer_Vendor Total Count"] = str(Count)
        elif Type == 1:
            other_data["FA Total Count"] = str(Count)
        elif Type == 2:
            other_data["Invoice Total Count"] = str(Count)
        else:
            other_data["Other Transaction Total Count"] = str(Count)
        other_data["DateTime Imported"] = datetime.datetime.utcnow().isoformat(timespec="seconds")
        # 对xml的数据做处理
        data_dict["CreateDateTime"] = to_local_time(data_dict["CreateDateTime"])
        # 合并数据
        data_dict = {**data_dict, **other_data}

        table_name = self._getTableName(self.company_nav_code, "DMSInterfaceInfo")
        General = self.base.classes[table_name]

        # 获取entry_no
        # 加线程锁
        lock = threading.Lock()
        lock.acquire()
        time.sleep(0.5)
        # print("%s已上锁" % threading.current_thread().name)
        trans = self.conn.execution_options(isolation_level="SERIALIZABLE").begin()
        # entry_no = self.getLatestEntryNo(table_name, "Entry No_")
        sql = "SELECT MAX([{1}]) as pk FROM [{0}] WITH (TABLOCKX)".format(table_name, "Entry No_")
        # print(sql)
        max_entry_id = self.conn.execute(sql).scalar()
        # print(max_entry_id)
        entry_no = max_entry_id + 1 if max_entry_id is not None else 1

        # 拼接sql
        data_dict["Entry No_"] = entry_no

        i = 0
        for f in data_dict.keys():
            v = data_dict[f]
            if f in api_p_out:
                f = api_p_out[f].Column_Name
                # 数据处理
                if api_p_out[f].Value_Type == 1 and f in convert_chn_fields:
                    # 处理中文编码
                    v = cast_chinese_encode(v)
                elif api_p_out[f].Value_Type in [2, 3] and type(v) == str:
                    # 布尔类型的节点
                    v = true_or_false_to_tinyint(v)
                elif api_p_out[f].Value_Type in [2, 3] and v is None:
                    # 数字类型的无值节点
                    v = 0
                elif api_p_out[f].Value_Type == 5:
                    # 时间转换
                    v = to_local_time(v)

            data_dict[f] = v

            i += 1

        ins = Insert(General, values=data_dict)
        # print(ins)
        self.conn.execute(ins)
        trans.commit()
        # print(result)

        lock.release()

        return entry_no

    # 获取行数量然后+1
    def getLatestEntryNo(self, table_name, primary_key):
        sql = "SELECT MAX([{1}]) as pk FROM [{0}]".format(table_name, primary_key)
        # print(sql)
        max_entry_id = self.conn.execute(sql).scalar()
        # print(max_entry_id)
        return max_entry_id + 1 if max_entry_id is not None else 1

    # 写入CV部分
    def insertCV(self, data_dict: dict, api_p_out: dict, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["Name", "Address", "City", "Country", "Application_Method",
                              "PaymentTermsCode", "Address 2", "Email", "Cost Center Code", "ICPartnerCode"]
        # 非xml的数据
        other_data = {"Gen_ Bus_ Posting Group": "", "VAT Bus_ Posting Group": "",
                      "Cust_VendPostingGroup": "", "Entry No_": entry_no,
                      "Error Message": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime Handled": "1753-01-01 00:00:00.000", "Handled by": ""}

        table_name = self._getTableName(self.company_nav_code, "CustVendBuffer")
        table_columns = self.getColumns(table_name)

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]

        for row_dict in data_dict:
            # print("every node start", time.perf_counter())
            # 对xml的数据做处理
            if row_dict["Type"] == "Customer":
                row_dict["Type"] = 0
            elif row_dict["Type"] == "Vendor":
                row_dict["Type"] = 1
            else:
                row_dict["Type"] = 2

            if row_dict["PricesIncludingVAT"].lower() == "true":
                row_dict["PricesIncludingVAT"] = 1
            else:
                row_dict["PricesIncludingVAT"] = 0

            # 合并数据
            row_dict = {**row_dict, **other_data}

            record_id = self.getLatestEntryNo(table_name, "Record ID")
            row_dict["Record ID"] = record_id

            # 处理中文转码和字段更名
            ins_data = {}
            for k in row_dict.keys():
                v = row_dict[k]
                if k in api_p_out:
                    f = api_p_out[k].Column_Name
                    # 去掉方括号
                    if f.find("[") != -1:
                        f = f.replace("[", "").replace("]", "")
                    if api_p_out[k].Value_Type == 1 and f in convert_chn_fields:
                        v = cast_chinese_encode(v)
                    elif api_p_out[k].Value_Type in [2, 3] and type(v) == str:
                        # 布尔类型的节点
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type in [2, 3] and v is None:
                        # 数字类型的无值节点
                        v = 0
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""

            ins_data = self.checkFields(ins_data, table_columns)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            # print(ins, ins.compile().params)
            # print("write start", time.perf_counter())
            self.conn.execute(ins)
            # print("write done", time.perf_counter())

    # 写入FA部分
    def insertFA(self, data_dict: dict, api_p_out: dict, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["Description", "SerialNo", "FAClassCode", "FASubclassCode", "FALocationCode",
                              "CostCenterCode"]
        # 非xml的数据
        other_data = {"UnderMaintenance": "", "Entry No_": entry_no, "Error Message": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime Handled": "1753-01-01 00:00:00.000", "Handled by": "",
                      }

        table_name = self._getTableName(self.company_nav_code, "FABuffer")
        table_columns = self.getColumns(table_name)

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]

        for row_dict in data_dict:
            # 合并数据
            row_dict = {**row_dict, **other_data}

            record_id = self.getLatestEntryNo(table_name, "Record ID")
            row_dict["Record ID"] = record_id

            # 处理中文转码和字段更名
            ins_data = {}
            for k in row_dict.keys():
                v = row_dict[k]
                if k in api_p_out:
                    f = api_p_out[k].Column_Name
                    # 去掉方括号
                    if f.find("[") != -1:
                        f = f.replace("[", "").replace("]", "")
                    if api_p_out[k].Value_Type == 1 and f in convert_chn_fields:
                        v = cast_chinese_encode(v)
                    elif api_p_out[k].Value_Type in [2, 3] and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type in [2, 3] and v is None:
                        # 数字类型的无值节点
                        v = 0
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""

            ins_data = self.checkFields(ins_data, table_columns)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            # print(ins, ins.compile().params)
            # print("write start", time.perf_counter())
            self.conn.execute(ins)
            # print("write done", time.perf_counter())

    # 写入发票头部分
    def insertInvHeader(self, data_dict: dict, api_p_out: dict, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["CostCenterCode", "VehicleSeries", "ExtDocumentNo", "Description"]
        # 非xml的数据
        other_data = {"Entry No_": entry_no, "Error Message": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime handled": "1753-01-01 00:00:00.000", "Handled by": ""}

        table_name = self._getTableName(self.company_nav_code, "InvoiceHeaderBuffer")
        table_columns = self.getColumns(table_name)

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]

        for row_dict in data_dict:
            # print("every node start", time.perf_counter())
            # 合并数据
            row_dict = {**row_dict, **other_data}

            record_id = self.getLatestEntryNo(table_name, "Record ID")
            row_dict["Record ID"] = record_id

            # 处理中文转码和字段更名
            ins_data = {}
            for k in row_dict.keys():
                v = row_dict[k]
                if k in api_p_out:
                    f = api_p_out[k].Column_Name
                    # 去掉方括号
                    if f.find("[") != -1:
                        f = f.replace("[", "").replace("]", "")
                    if api_p_out[k].Value_Type == 1 and f in convert_chn_fields:
                        v = cast_chinese_encode(v)
                    elif api_p_out[k].Value_Type in [2, 3] and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type in [2, 3] and v is None:
                        # 数字类型的无值节点
                        v = 0
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""

            ins_data = self.checkFields(ins_data, table_columns)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            # print(ins, ins.compile().params)
            # print("write start", time.perf_counter())
            self.conn.execute(ins)
            # print("write done", time.perf_counter())

    # 写入发票行部分
    def insertInvLines(self, data_dict: dict, api_p_out: dict, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["Description", "CostCenterCode", "VehicleSeries", "VIN", "WIP_No_",
                              "FromCompanyName", "ToCompanyName"]
        # 非xml的数据
        other_data = {"Entry No_": entry_no, "Error Message": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime Handled": "1753-01-01 00:00:00.000", "Handled by": ""}

        table_name = self._getTableName(self.company_nav_code, "InvoiceLineBuffer")
        table_columns = self.getColumns(table_name)

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]

        for row_dict in data_dict:
            # 合并数据
            row_dict = {**row_dict, **other_data}

            record_id = self.getLatestEntryNo(table_name, "Record ID")
            row_dict["Record ID"] = record_id

            # 处理中文转码和字段更名
            ins_data = {}
            for k in row_dict.keys():
                if k == "InvoiceType":
                    continue
                v = row_dict[k]
                if k in api_p_out:
                    f = api_p_out[k].Column_Name
                    # 去掉方括号
                    if f.find("[") != -1:
                        f = f.replace("[", "").replace("]", "")
                    if api_p_out[k].Value_Type == 1 and f in convert_chn_fields:
                        v = cast_chinese_encode(v)
                    elif api_p_out[k].Value_Type == 2 and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type in [2, 3] and v is None:
                        # 数字类型的无值节点
                        v = 0
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""
            # print(ins_data)
            ins_data = self.checkFields(ins_data, table_columns)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            self.conn.execute(ins)

    # 写入other部分
    def insertOther(self, data_dict: dict, api_p_out: dict, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["ExtDocumentNo_", "Description", "CostCenterCode", "VehicleSeries",
                              "WIP_No_", "FromCompanyName", "ToCompanyName", "VIN"]
        # 非xml的数据
        other_data = {"Entry No_": entry_no, "Error Message": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime handled": "1753-01-01 00:00:00.000", "Handled by": "",
                      "NotDuplicated": 0, "NAVDocumentNo_": ""}

        table_name = self._getTableName(self.company_nav_code, "OtherBuffer")
        table_columns = self.getColumns(table_name)

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]

        for row_dict in data_dict:
            # print("every node start", time.perf_counter())
            # 合并数据
            row_dict = {**row_dict, **other_data}

            record_id = self.getLatestEntryNo(table_name, "Record ID")
            row_dict["Record ID"] = record_id

            # 处理中文转码和字段更名
            ins_data = {}
            for k in row_dict.keys():
                v = row_dict[k]
                if k in api_p_out:
                    f = api_p_out[k].Column_Name
                    # 去掉方括号
                    if f.find("[") != -1:
                        f = f.replace("[", "").replace("]", "")
                    if api_p_out[k].Value_Type == 1 and f in convert_chn_fields:
                        v = cast_chinese_encode(v)
                    elif api_p_out[k].Value_Type == 2 and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type in [2, 3] and v is None:
                        v = 0
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""

            ins_data = self.checkFields(ins_data, table_columns)

            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            # print(ins, ins.compile().params)
            # print("write start", time.perf_counter())
            self.conn.execute(ins)
            # print("write done", time.perf_counter())

    # 用于验证的查询
    def getNavDataByEntryNo(self, entry_no, table_name="DMSInterfaceInfo", return_list=True):
        if table_name not in self.tables:
            return None
        table_name = self._getTableName(self.company_nav_code, table_name)
        TABLE_CLASS = self.base.classes[table_name]
        s = select([TABLE_CLASS]).where(text("[Entry No_] = :x"))
        if return_list:
            return self.conn.execute(s, x=entry_no).fetchall()
        else:
            return self.conn.execute(s, x=entry_no).fetchone()

    # 用于验证的查询
    def getInvoiceLines(self, entry_no, invoice_no):
        table_name = self._getTableName(self.company_nav_code, "InvoiceLineBuffer")
        TABLE_CLASS = self.base.classes[table_name]
        s = select([TABLE_CLASS]).where(and_(text("[Entry No_] = :x"), text("InvoiceNo = :y")))

        return self.conn.execute(s, x=entry_no, y=invoice_no).fetchall()
