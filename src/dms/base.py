#!/usr/bin/python
# -*- coding:utf-8 -*-
# 公用逻辑：
# 1. 根据公司列表和接口设置确定数据源
# 2. 从数据源（xml / json）读取数据
# 3. 读取DMS_API_P_Out读取要保存的General的字段
# 4. 根据配置字段将数据里的数据写入InterfaceInfo并返回entry no
import datetime
import os
from collections import OrderedDict

import xmltodict

from src import db
from src.error import DataFieldEmptyError
from src.models import dms, nav


class DMSBase:
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
    def load_data_from_dms_interface(self) -> dict:
        return []

    # 读取xml
    def load_data_from_xml(self, xml_src_path) -> dict:
        if not os.path.exists(xml_src_path):
            raise FileNotFoundError("找不到xml文件：%s" % xml_src_path)

        with open(xml_src_path, "rb") as xml_handler:
            data = xmltodict.parse(xml_handler.read())
        return data

    # 获取指定节点的数量（xml可以节点同名。在json这里，则判断节点是否是数组。是，则返回长度；非，则返回1。
    def get_count_from_data(self, data, node_name) -> int:
        # print(type(data[node_name]), type(data[node_name]) == OrderedDict)
        if node_name not in data:
            return 0
        if type(data[node_name]) == OrderedDict:
            return 1
        return len(data[node_name])

    # 读取出参配置配置
    def load_api_p_out_nodes(self, company_code, api_code, node_type="general", depth=2):
        node_dict = {}
        api_p_out_config = db.session.query(dms.ApiPOutSetup) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .filter(dms.ApiPOutSetup.Level == depth) \
            .filter(dms.ApiPOutSetup.Parent_Node_Name == node_type) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        for one in api_p_out_config:
            if one.P_Name not in node_dict:
                node_dict[one.P_Name] = one
        # print(node_dict)
        return node_dict

    '''
    从api_p_out获取数据
        @param dict data 要处理的源数据
        @param dict node_dict 要处理的数据字段字典
        @param str node_lv0 顶部节点名
        @param str node_lv1 一级节点名
        @param str node_type 节点类型，node=对象节点，list=数组节点
    '''
    def _splice_field(self, data, node_dict, node_lv0, node_lv1, node_type="node"):
        if node_type == "node":
            data_dict = {}
            for key, value in data[node_lv0][node_lv1].items():
                if key in node_dict:
                    data_dict[key] = value
            return data_dict
        else:
            data_dict_list = []
            list_node = data[node_lv0][node_lv1]
            data[node_lv0][node_lv1] = list_node if type(list_node) == list else [list_node, ]

            for row in data[node_lv0][node_lv1]:
                # print(row, type(row))
                data_dict = {}
                for key, value in row.items():
                    if key in node_dict:
                        data_dict[key] = value
                # print(data_dict)
                data_dict_list.append(data_dict)
            # print(data_dict_list)
            return data_dict_list

    # 从api_p_out获取General数据
    def splice_general_info(self, data, node_dict):
        return self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1="General", node_type="node")

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
        pass

    # 根据API_P_Out写入nav表
    def save_data_to_nav(self, nav_data, entry_no, TABLE_CLASS):
        if type(nav_data) == OrderedDict:
            nav_data = [nav_data]

        for row in nav_data:
            other_obj = TABLE_CLASS(Entry_No_=entry_no)
            other_obj.Record_ID = other_obj.getLatestRecordId()
            for key, value in row.items():
                # 自动赋值
                other_obj.__setattr__(key, value)
            # print(custVend_obj)
            db.session.add(other_obj)
        db.session.commit()

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass
