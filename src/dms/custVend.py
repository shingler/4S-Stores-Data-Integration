#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime
import os

from sqlalchemy import func

from src.error import DataFieldEmptyError
from .base import DMSBase
from src.models import dms
from src.models import nav
from src import db
import xmltodict


class CustVend(DMSBase):

    # 根据公司列表和接口设置确定数据源
    def load_config_from_api_setup(self, company_code, api_code) -> dms.ApiSetup:
        api_setup = db.session.query(dms.ApiSetup).filter(dms.ApiSetup.Company_Code == company_code) \
            .filter(dms.ApiSetup.API_Code == api_code).first()
        return api_setup

    # 拼接xml文件路径
    def splice_xml_file_path(self, apiSetUp, secondary=False) -> str:
        if apiSetUp.API_Type == 1:
            return ""
        if not secondary:
            if apiSetUp.API_Address1 == "" or apiSetUp.Archived_Path == "":
                raise DataFieldEmptyError("API_Address或Archived_Path为空")
            xml_src = "%s/%s" % (apiSetUp.API_Address1, apiSetUp.Archived_Path)
        else:
            if apiSetUp.API_Address2 == "" or apiSetUp.Archived_Path == "":
                raise DataFieldEmptyError("API_Address或Archived_Path为空")
            xml_src = "%s/%s" % (apiSetUp.API_Address2, apiSetUp.Archived_Path)
        return xml_src

    # 读取接口
    def load_data_from_dms_interface(self):
        return []

    # 读取xml
    def load_data_from_xml(self, xml_src_path):
        if not os.path.exists(xml_src_path):
            raise FileNotFoundError("找不到xml文件：%s" % xml_src_path)

        with open(xml_src_path, "rb") as xml_handler:
            data = xmltodict.parse(xml_handler.read())
        return data

    # 读取general配置
    def load_api_p_out_nodes(self, company_code, api_code, node_type="general"):
        node_dict = {}
        api_p_out_lv2_config = db.session.query(dms.ApiPOutSetup) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .filter(dms.ApiPOutSetup.Level == 2) \
            .filter(dms.ApiPOutSetup.Parent_Node_Name == node_type) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        for one in api_p_out_lv2_config:
            if one.P_Name not in node_dict:
                node_dict[one.P_Name] = one
        print(node_dict)
        return node_dict

    # 从api_p_out获取数据
    def splice_general_info(self, data, node_dict):
        data_dict = {}
        for key, value in data["Transaction"]["General"].items():
            if key in node_dict:
                data_dict[key] = value
        # print(data_dict)
        return data_dict

    # 写入interfaceinfo获得entry_no
    def save_data_to_interfaceinfo(self, general_data, Type, Count, XMLFile=""):
        # 用数据初始化对象
        interfaceInfo = nav.InterfaceInfo(
            DMSCode=general_data["DMSCode"],
            DMSTitle=general_data["DMSTitle"],
            CompanyCode=general_data["CompanyCode"],
            CompanyTitle=general_data["CompanyTitle"],
            CreateDateTime=general_data["CreateDateTime"],
            Creator=general_data["Creator"],
            XMLFileName=XMLFile,
            Type=Type,
            Customer_Vendor_Total_Count=0,
            Other_Transaction_Total_Count=0,
            FA_Total_Count=0,
            Invoice_Total_Count=0
        )
        # 再补充一些默认值
        interfaceInfo.DateTime_Imported = str(datetime.datetime.now())

        if Type == 0:
            interfaceInfo.Customer_Vendor_Total_Count = Count
        elif Type == 1:
            interfaceInfo.FA_Total_Count = Count
        elif Type == 2:
            interfaceInfo.Invoice_Total_Count = Count
        else:
            interfaceInfo.Other_Transaction_Total_Count = Count

        interfaceInfo.Entry_No_ = interfaceInfo.getLatestEntryNo()

        db.session.add(interfaceInfo)
        db.session.commit()
        db.session.flush()
        return interfaceInfo.Entry_No_

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = []
        if len(data["Transaction"]["CustVendInfo"]) == 1:
            data["Transaction"]["CustVendInfo"] = [data["Transaction"]["CustVendInfo"]]
        for row in data["Transaction"]["CustVendInfo"]:
            data_dict = {}
            for key, value in row.items():
                if key in node_dict:
                    data_dict[key] = value
            # print(data_dict)
            data_dict_list.append(data_dict)
        return data_dict_list

    # 根据API_P_Out写入CustVendInfo库
    def save_data_to_custVendInfo(self, custVend_data, entry_no):
        if type(custVend_data) == "dict":
            custVend_data = [custVend_data]

        for row in custVend_data:
            custVend_obj = nav.CustVendBuffer(Entry_No_=entry_no)
            custVend_obj.Record_ID = custVend_obj.getLatestRecordId()
            for key, value in row.items():
                if key == "Type" and value == "Customer":
                    value = 0
                elif key == "Type" and value == "Vendor":
                    value = 1
                elif key == "Type":
                    value = 2

                # 自动赋值
                custVend_obj.__setattr__(key, value)
            # print(custVend_obj)
            db.session.add(custVend_obj)
        db.session.commit()

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass
