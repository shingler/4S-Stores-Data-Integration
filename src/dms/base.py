#!/usr/bin/python
# -*- coding:utf-8 -*-
# 公用逻辑：
# 1. 根据公司列表和接口设置确定数据源
# 2. 从数据源（xml / json）读取数据
# 3. 读取DMS_API_P_Out读取要保存的General的字段
# 4. 根据配置字段将数据里的数据写入InterfaceInfo并返回entry no
import datetime
import os
import time
from collections import OrderedDict

import xmltodict

from src import db
from src.error import DataFieldEmptyError
from src.models import dms, nav, to_local_time
from src.models.log import APILog


class DMSBase:
    # 强制启用备用地址
    force_secondary = False
    # dms方向
    DIRECT_DMS = 1
    # NAV方向
    DIRECT_NAV = 2
    # 状态：执行中
    STATUS_PENDING = 1
    # 状态：完成
    STATUS_FINISH = 2
    # 状态：错误
    STATUS_ERROR = 9

    def __init__(self, force_secondary=False):
        self.force_secondary = force_secondary

    # 拼接xml文件路径
    def _splice_xml_file_path(self, apiSetUp) -> str:
        if apiSetUp.API_Type == 1:
            return ""
        if not self.force_secondary:
            if apiSetUp.API_Address1 == "" or apiSetUp.Archived_Path == "":
                raise DataFieldEmptyError("API_Address或Archived_Path为空")
            xml_src = "%s/%s" % (apiSetUp.API_Address1, apiSetUp.Archived_Path)
        else:
            if apiSetUp.API_Address2 == "" or apiSetUp.Archived_Path == "":
                raise DataFieldEmptyError("API_Address或Archived_Path为空")
            xml_src = "%s/%s" % (apiSetUp.API_Address2, apiSetUp.Archived_Path)
        return xml_src

    # 读取接口
    def _load_data_from_dms_interface(self, apiSetup) -> dict:
        return []

    # 读取xml
    def _load_data_from_xml(self, xml_src_path):
        if not os.path.exists(xml_src_path):
            raise FileNotFoundError("找不到xml文件：%s" % xml_src_path)

        with open(xml_src_path, "rb") as xml_handler:
            data = xml_handler.read()
        return data

    # 读取数据
    def load_data(self, apiSetup, userID=None) -> (str, dict):
        # 先写一条日志，记录执行时间
        log_pk = self.add_new_api_log_when_start(apiSetup, direction=self.DIRECT_DMS, userID=userID)
        # 模拟执行
        # time.sleep(2)
        if apiSetup.API_Type == 1:
            path = ""
            data = self._load_data_from_dms_interface(apiSetup)
            # 处理成功，更新日志
            self.update_api_log_when_finish(log_pk, data=data, status=self.STATUS_FINISH)
        else:
            path = self._splice_xml_file_path(apiSetup)
            xml_data = self._load_data_from_xml(path)
            # 处理成功，更新日志
            self.update_api_log_when_finish(log_pk, data=xml_data, status=self.STATUS_FINISH)
            # 将xml转为字典
            data = xmltodict.parse(xml_data)

        return path, data

    # 获取指定节点的数量（xml可以节点同名。在json这里，则判断节点是否是数组。是，则返回长度；非，则返回1。
    def get_count_from_data(self, data, node_name) -> int:
        if node_name not in data:
            return 0
        if type(data[node_name]) == OrderedDict:
            return 1
        return len(data[node_name])

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
            CreateDateTime=to_local_time(general_data["CreateDateTime"]),
            Creator=general_data["Creator"],
            XMLFileName=XMLFile,
            Type=Type,
            Customer_Vendor_Total_Count=0,
            Other_Transaction_Total_Count=0,
            FA_Total_Count=0,
            Invoice_Total_Count=0
        )
        # 再补充一些默认值
        interfaceInfo.DateTime_Imported = datetime.datetime.now().isoformat(timespec="seconds")

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
        # db.session.query(interfaceInfo.Entry_No_ == interfaceInfo.Entry_No_).first()
        db.session.expire_all()
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
            db.session.add(other_obj)
        db.session.commit()

    # 访问接口/文件时先新增一条API日志，并返回API_Log的主键用于后续更新
    def add_new_api_log_when_start(self, apiSetup, direction=1, apiPIn=None, userID=None):
        logger = APILog(
            Company_Code=apiSetup.Company_Code,
            API_Code=apiSetup.API_Code,
            API_Direction=direction,
            API_P_In=apiPIn if apiPIn is not None else "",
            API_Content="",
            Content_Type=apiSetup.Data_Format,
            Status=1,
            Executed_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Finished_DT="",
            Error_Message="",
            Executed_By=1 if userID is None else 2,
            UserID="System" if userID is None else userID
        )
        db.session.add(logger)
        db.session.commit()
        db.session.flush()
        return logger.ID

    # 读取接口/文件成功后，通过主键更新日志
    def update_api_log_when_finish(self, pk, status, data=None, error_msg=""):
        db.session.query(APILog).filter(APILog.ID == pk).update({
            "Status": status,
            "API_Content": data,
            "Finished_DT": datetime.datetime.now().isoformat(timespec="milliseconds"),
            "Error_Message": error_msg
        })

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass
