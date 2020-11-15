#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用拼接sql的方式写入nav库
import datetime
import threading
import time

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Insert
from sqlalchemy.util import OrderedDict

from src import ApiPOutSetup, cast_chinese_encode
from src import to_local_time, true_or_false_to_tinyint


class NavDB:
    dbo = None
    conn = None
    meta = None
    base = None

    def __init__(self, db_host, db_user, db_password, db_name):
        conn_str = "mssql+pyodbc://{1}:{2}@{0}:1433/{3}?driver=ODBC+Driver+17+for+SQL+Server".format(db_host, db_user, db_password, db_name)
        engine = create_engine(conn_str)
        DBSession = sessionmaker(bind=engine)
        self.dbo = DBSession()
        self.meta = MetaData()
        self.meta.reflect(bind=engine)
        self.conn = engine.connect()

    @staticmethod
    def _getTableName(company_nav_code: str, data_name) -> str:
        return "{0}${1}".format(company_nav_code, data_name)

    def prepare(self):
        Base = automap_base(metadata=self.meta)
        Base.prepare()
        self.base = Base
        for c in Base.classes:
            print(c, type(c))

    # 写入General部分
    def insertGeneral(self, company_nav_code: str, data_dict: dict, api_p_out: ApiPOutSetup, Type: int = 0, Count: int = 0, XMLFile: str = "", **kwargs):
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


        table_name = self._getTableName(company_nav_code, "DMSInterfaceInfo")

        General = self.base.classes[table_name]

        # 获取entry_no
        # 加线程锁
        lock = threading.Lock()
        lock.acquire()
        time.sleep(0.5)
        # print("%s已上锁" % threading.current_thread().name)
        entry_no = self.getLatestEntryNo(table_name, "Entry No_")

        # 拼接sql
        data_dict["Entry No_"] = entry_no

        i = 0
        # print(fields, data_dict)
        for f in data_dict.keys():
            v = data_dict[f]
            if f in api_p_out:
                f = api_p_out[f].Column_Name
                # 数据处理
                if api_p_out[f].Value_Type == 1 and f in convert_chn_fields:
                    # 处理中文编码
                    v = cast_chinese_encode(v)
                elif api_p_out[f].Value_Type == 5:
                    # 时间转换
                    v = to_local_time(v)

            data_dict[f] = v

            i += 1

        ins = Insert(General, values=data_dict)
        # print(ins)
        # print(ins.compile().params)
        self.conn.execute(ins)
        # print(result)

        lock.release()

        return entry_no

    # 获取行数量然后+1
    def getLatestEntryNo(self, table_name, primary_key):
        sql = "SELECT MAX([{1}]) as pk FROM [{0}]".format(table_name, primary_key)
        print(sql)
        max_entry_id = self.conn.execute(sql).scalar()
        print(max_entry_id)
        return max_entry_id + 1 if max_entry_id is not None else 1

    # 写入CV部分
    def insertCV(self, company_nav_code: str, data_dict: dict, api_p_out: ApiPOutSetup, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["Name", "Address", "City", "Country", "Application_Method",
                              "PaymentTermsCode", "Address 2", "Email", "Cost Center Code", "ICPartnerCode"]
        # 非xml的数据
        other_data = {"Gen_ Bus_ Posting Group": "", "VAT Bus_ Posting Group": "",
                      "Cust_VendPostingGroup": "", "Entry No_": entry_no,
                      "Error Message": "", "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime Handled": "1753-01-01 00:00:00.000", "Handled by": "''"}

        table_name = self._getTableName(company_nav_code, "CustVendBuffer")

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]

        for row_dict in data_dict:

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
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""
            # print(ins_data)
            CustVendTable = self.base.classes[table_name]
            ins = Insert(CustVendTable, values=ins_data)
            # print(ins, ins.compile().params)
            self.conn.execute(ins)

    # 写入FA部分
    def insertFA(self, company_nav_code: str, data_dict: dict, api_p_out: ApiPOutSetup, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["Description", "SerialNo", "FAClassCode", "FASubclassCode", "FALocationCode",
                          "CostCenterCode"]
        # 非xml的数据
        other_data = {"UnderMaintenance": "", "Entry No_": entry_no, "DepreciationPeriod": 0,
                      "Error Message": "", "CostCenterCode": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime Handled": "1753-01-01 00:00:00.000", "Handled by": "",
                      "NextServiceDate": "1753-01-01 00:00:00.000", "WarrantyDate": "1753-01-01 00:00:00.000",
                      "DepreciationStartingDate": datetime.datetime.utcnow().isoformat(timespec="seconds")}

        table_name = self._getTableName(company_nav_code, "FABuffer")

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
                    elif api_p_out[k].Value_Type == 2 and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""
            # print(ins_data)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            # print(ins, ins.compile().params)
            self.conn.execute(ins)

    # 写入发票部分
    def insertInv(self, company_nav_code: str, data_dict: dict, api_p_out: ApiPOutSetup, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["Description", "SerialNo", "FAClassCode", "FASubclassCode", "FALocationCode",
                              "CostCenterCode"]
        # 非xml的数据
        other_data = {"UnderMaintenance": "", "Entry No_": entry_no, "DepreciationPeriod": 0,
                      "Error Message": "", "CostCenterCode": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime Handled": "1753-01-01 00:00:00.000", "Handled by": "",
                      "NextServiceDate": "1753-01-01 00:00:00.000", "WarrantyDate": "1753-01-01 00:00:00.000",
                      "DepreciationStartingDate": datetime.datetime.utcnow().isoformat(timespec="seconds")}

        table_name = self._getTableName(company_nav_code, "FABuffer")

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
                    elif api_p_out[k].Value_Type == 2 and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out[k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""
            # print(ins_data)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            # print(ins, ins.compile().params)
            self.conn.execute(ins)

    # 写入other部分
    def insertOther(self, company_nav_code: str, data_dict: dict, api_p_out: ApiPOutSetup, entry_no: int):
        # 需要转中文编码的字段
        convert_chn_fields = ["ExtDocumentNo_", "Description", "CostCenterCode", "VehicleSeries",
                              "WIP_No_", "FromCompanyName", "ToCompanyName", "VIN"]
        # 非xml的数据
        other_data = {"Entry No_": entry_no, "Error Message": "",
                      "DateTime Imported": datetime.datetime.utcnow().isoformat(timespec="seconds"),
                      "DateTime handled": "1753-01-01 00:00:00.000", "Handled by": "",
                      "NotDuplicated": 0, "NAVDocumentNo_": ""}

        table_name = self._getTableName(company_nav_code, "OtherBuffer")

        # 写cv
        if type(data_dict) == OrderedDict:
            data_dict = [data_dict]
        print("======")
        print(api_p_out)
        for row_dict in data_dict:
            # 合并数据
            row_dict = {**row_dict, **other_data}

            record_id = self.getLatestEntryNo(table_name, "Record ID")
            row_dict["Record ID"] = record_id

            # 处理中文转码和字段更名
            ins_data = {}
            for k in row_dict.keys():
                v = row_dict[k]
                if k in api_p_out["Daydook"]["Line"]:
                    f = api_p_out["Daydook"]["Line"][k].Column_Name
                    # 去掉方括号
                    if f.find("[") != -1:
                        f = f.replace("[", "").replace("]", "")
                    if api_p_out["Daydook"]["Line"][k].Value_Type == 1 and f in convert_chn_fields:
                        v = cast_chinese_encode(v)
                    elif api_p_out["Daydook"]["Line"][k].Value_Type == 2 and type(v) == str:
                        v = true_or_false_to_tinyint(v)
                    elif api_p_out["Daydook"]["Line"][k].Value_Type == 5:
                        v = to_local_time(v)
                    ins_data[f] = v if v is not None else ""
                else:
                    ins_data[k] = v if v is not None else ""
            ins_data["DocumentNo_"] = ins_data["DaydookNo"]
            del ins_data["DaydookNo"]
            print(ins_data)
            FaTable = self.base.classes[table_name]
            ins = Insert(FaTable, values=ins_data)
            print(ins, ins.compile().params)
            self.conn.execute(ins)
