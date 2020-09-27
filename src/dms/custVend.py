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
        api_setup = db.session.query(dms.ApiSetup).filter(dms.ApiSetup.Company_Code == company_code)\
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

    # 写入interfaceinfo获得entry_no
    def save_data_to_interfaceinfo(self, DMSCode, DMSTitle, CompanyCode, CompanyTitle, CreateDateTime, Creator,
                                   Type, Count, XMLFile=""):
        # 用数据初始化对象
        interfaceInfo = nav.InterfaceInfo(
            DMSCode=DMSCode,
            DMSTitle=DMSTitle,
            CompanyCode=CompanyCode,
            CompanyTitle=CompanyTitle,
            CreateDateTime=CreateDateTime,
            Creator=Creator,
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

        interfaceInfo.Entry_No_ = self.getNewEntryNo()

        db.session.add(interfaceInfo)
        db.session.commit()
        db.session.flush()
        return interfaceInfo.Entry_No_

    # 单线程版获取最大id然后+1
    def getNewEntryNo(self):
        max_entry_id = db.session.query(func.max(nav.InterfaceInfo).label("max")).first()
        return max_entry_id+1

    # 根据API_P_Out写入CustVendInfo库
    def save_data_to_custVendInfo(self):
        pass

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass

