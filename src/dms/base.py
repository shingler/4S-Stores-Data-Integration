#!/usr/bin/python
# -*- coding:utf-8 -*-
# 公用逻辑：
# 1. 根据公司列表和接口设置确定数据源
# 2. 从数据源（xml / json）读取数据
# 3. 读取DMS_API_P_Out读取要保存的General的字段
# 4. 根据配置字段将数据里的数据写入InterfaceInfo并返回entry no
import datetime
import json
import os
import threading
import time
import urllib
from collections import OrderedDict
from urllib.parse import urlencode

import requests
import xmltodict
from requests_ntlm import HttpNtlmAuth
from sqlalchemy.exc import InvalidRequestError

from src import db, Company, ApiSetup, ApiPInSetup, validator
from src.dms.logger import Logger
from src.dms.setup import Setup
from src.error import DataFieldEmptyError, DataLoadError, DataLoadTimeOutError, DataImportRepeatError, \
    DataContentTooBig, NodeNotExistError
from src.models import nav, to_local_time
from src import words


class DMSBase:
    # 公司的NAV代码（作为nav表的前缀）
    company_nav_code = ""
    # General表模型
    GENERAL_CLASS = None
    # 强制启用备用地址
    force_secondary = False
    # 是否检查重复导入
    check_repeat = True
    # NAV的WebService的SOAPAction
    WS_ACTION = "urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI:DMSDataInterfaceIn"

    # NAV的WebService方法名
    WS_METHOD = ""

    # ------- 下面是常量 --------#
    # dms方向
    DIRECT_DMS = 1
    # NAV方向
    DIRECT_NAV = 2

    # 状态：执行中
    STATUS_PENDING = 1
    # 状态：完成
    STATUS_FINISH = 2
    # 状态：重复导入
    STATUS_REPEAT = 7
    # 状态：超时
    STATUS_TIMEOUT = 8
    # 状态：错误
    STATUS_ERROR = 9

    # 格式：JSON
    FORMAT_JSON = 1
    # 格式：XML
    FORMAT_XML = 2

    # 接口类型：WebAPI
    TYPE_API = 1
    # 接口类型：文件
    TYPE_FILE = 2

    def __init__(self, company_nav_code, force_secondary=False, check_repeat=True):
        self.company_nav_code = company_nav_code
        self.force_secondary = force_secondary
        self.check_repeat = check_repeat
        self.GENERAL_CLASS = nav.dmsInterfaceInfo(company_nav_code)

    # 拼接xml文件路径
    # @param src.models.dms.ApiSetup apiSetup
    def _splice_xml_file_path(self, apiSetUp) -> str:
        if apiSetUp.API_Type == self.TYPE_API:
            return ""

        cur_date = datetime.datetime.now().strftime("%Y%m%d")
        if apiSetUp.File_Name_Format == "":
            raise DataFieldEmptyError(words.DataImport.field_is_empty("File_Name_Format"))

        # 文件名格式支持“YYYYMMDD”、“YYYY.MM.DD”，“YYYY-MM-DD”
        if apiSetUp.File_Name_Format.startswith("YYYYMMDD"):
            file_name = apiSetUp.File_Name_Format.replace("YYYYMMDD", cur_date)
        elif apiSetUp.File_Name_Format.startswith("YYYY.MM.DD"):
            file_name = apiSetUp.File_Name_Format.replace("YYYYMMDD", cur_date)
        elif apiSetUp.File_Name_Format.startswith("YYYY-MM-DD"):
            file_name = apiSetUp.File_Name_Format.replace("YYYYMMDD", cur_date)
        else:
            file_name = apiSetUp.File_Name_Format

        if not self.force_secondary:
            if apiSetUp.API_Address1 == "":
                raise DataFieldEmptyError(words.DataImport.field_is_empty("API_Address1"))
            xml_src = "%s/%s" % (apiSetUp.API_Address1, file_name)
        else:
            if apiSetUp.API_Address2 == "":
                raise DataFieldEmptyError(words.DataImport.field_is_empty("API_Address2"))
            xml_src = "%s/%s" % (apiSetUp.API_Address2, file_name)
        return xml_src

    # 读取接口
    # @param string format 数据解析格式（JSON | XML）
    # @param int time_out 超时时间，单位为秒。为0表示不判断超时
    def _load_data_from_dms_interface(self, path, format="json", time_out=0):
        return InterfaceResult(status=self.STATUS_FINISH, content="")

    # 读取xml,返回InterfaceResult对象
    # @param string format 数据解析格式（JSON | XML）
    # @param int time_out 超时时间，单位为秒。为0表示不判断超时
    def _load_data_from_file(self, path, format="xml", time_out=0):
        # 重复性检查
        repeated = db.session.query(self.GENERAL_CLASS).filter(self.GENERAL_CLASS.XMLFileName == path).all()
        if self.check_repeat and len(repeated) > 0:
            error_msg = words.DataImport.file_is_repeat(path)
            return InterfaceResult(status=self.STATUS_REPEAT, error_msg=error_msg)
        if not os.path.exists(path):
            error_msg = words.DataImport.file_not_exist(path)
            return InterfaceResult(status=self.STATUS_ERROR, error_msg=error_msg)

        with open(path, "r", encoding="UTF-8") as xml_handler:
            data = xml_handler.read()
        # 模拟超时
        # time.sleep(90)
        if time_out > 0 and time.perf_counter() >= time_out * 60:
            return InterfaceResult(status=self.STATUS_TIMEOUT, error_msg=words.DataImport.load_timeout(path))

        # print(data, type(data))
        res = InterfaceResult(status=self.STATUS_FINISH, content=data)
        if format == self.FORMAT_XML:
            res.data = xmltodict.parse(data)
        else:
            res.data = json.loads(data, encoding="utf-8")
        return res

    # 校验数据长度合法性
    def is_valid(self, data_dict) -> (bool, dict):
        res_bool = True
        res_keys = {}
        for k, v in data_dict["Transaction"]["General"].items():
            is_valid = validator.DMSInterfaceInfoValidator.check_chn_length(k, v)
            if not is_valid:
                res_bool = False
                res_keys["%s.%s" % ("General", k)] = validator.DMSInterfaceInfoValidator.expect_length(k)

        res_bool2, res_keys2 = self._is_valid(data_dict)

        return res_bool and res_bool2, {**res_keys, **res_keys2}

    # 校验数据长度合法性（子类实现）
    def _is_valid(self, data_dict) -> (bool, dict):
        pass

    # 校验数据完整性
    def is_integrity(self, data_dict, company_code, api_code) -> (bool, list):
        res_bool = True
        res_keys = []
        general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
        # print(general_node_dict)
        # 检查规定的节点是否存在于data中
        for node in general_node_dict:
            # print(node, type(node))
            if node not in data_dict["Transaction"]["General"]:
                res_bool = False
                res_keys.append("%s.%s" % ("General", node))

        res_bool2, res_keys2 = self._is_integrity(data_dict, company_code, api_code)
        # 合并结果
        res_keys.extend(res_keys2)
        # print(res_keys)
        return res_bool and res_bool2, res_keys

    # 校验数据完整性（子类实现）
    def _is_integrity(self, data_dict, company_code, api_code) -> (bool, list):
        pass

    # 读取数据
    def load_data(self, apiSetup, userID=None, file_path=None) -> (str, dict):
        # 先写一条日志，记录执行时间
        logger = self.add_new_api_log_when_start(apiSetup, direction=self.DIRECT_DMS, userID=userID)

        path = ""
        res = None
        if apiSetup.API_Type == self.TYPE_API:
            # 读取JSON API
            path = ""
            res = self._load_data_from_dms_interface(path, format=apiSetup.Data_Format, time_out=apiSetup.Time_out * 60)
        elif apiSetup.API_Type == self.TYPE_FILE and file_path is not None:
            # 直接提供XML地址
            path = file_path
            res = self._load_data_from_file(file_path, format=apiSetup.Data_Format, time_out=apiSetup.Time_out * 60)
        elif apiSetup.API_Type == self.TYPE_FILE:
            # 使用当天的XML文件
            path = self._splice_xml_file_path(apiSetup)
            res = self._load_data_from_file(path, format=apiSetup.Data_Format, time_out=apiSetup.Time_out * 60)
        # print(res)

        # 根据结果进行后续处理
        if res.status == self.STATUS_ERROR:
            # 记录错误日志并抛出异常
            logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=res.error_msg)
            raise DataLoadError(res.error_msg)
        elif res.status == self.STATUS_TIMEOUT:
            # 记录错误日志并抛出异常
            logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=res.error_msg)
            raise DataLoadTimeOutError(res.error_msg)
        elif res.status == self.STATUS_REPEAT:
            # 记录错误日志并抛出异常
            logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=res.error_msg)
            raise DataImportRepeatError(res.error_msg)
        else:
            # 处理成功，校验数据完整性
            is_integrity, keys = self.is_integrity(res.data, apiSetup.Company_Code, apiSetup.API_Code)
            print(is_integrity, keys)
            if not is_integrity:
                error_msg = words.DataImport.node_not_exists(keys)
                logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=error_msg)
                raise NodeNotExistError(error_msg)

            # 处理成功，校验数据长度是否合法
            is_valid, keys = self.is_valid(res.data)
            # print(is_valid, keys)
            if not is_valid:
                error_msg = words.DataImport.content_is_too_big(path, keys)
                logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=error_msg)
                raise DataContentTooBig(error_msg)

            # 校验成功，更新日志
            logger.update_api_log_when_finish(data=str(res.content), status=self.STATUS_FINISH)
            return path, res.data

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
            if node_lv1 in data[node_lv0]:
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
        InterfaceClass = self.GENERAL_CLASS
        # 处理sql server的identity_insert问题
        # db.session.execute("SET IDENTITY_INSERT [%s] ON" % InterfaceClass.__tablename__)
        interfaceInfo = InterfaceClass(
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
        # print(self.company_nav_code, interfaceInfo.__bind_key__)
        # 再补充一些默认值
        interfaceInfo.DateTime_Imported = datetime.datetime.utcnow().isoformat(timespec="seconds")

        if Type == 0:
            interfaceInfo.Customer_Vendor_Total_Count = Count
        elif Type == 1:
            interfaceInfo.FA_Total_Count = Count
        elif Type == 2:
            interfaceInfo.Invoice_Total_Count = Count
        else:
            interfaceInfo.Other_Transaction_Total_Count = Count

        # 加线程锁
        lock = threading.Lock()
        lock.acquire()
        time.sleep(0.5)
        # print("%s已上锁" % threading.current_thread().name)
        interfaceInfo.Entry_No_ = interfaceInfo.getLatestEntryNo()
        lock.release()
        # print("%s的锁已释放" % threading.current_thread().name)

        db.session.add(interfaceInfo)
        # db.session.execute("SET IDENTITY_INSERT [%s] OFF" % InterfaceClass.__tablename__)
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
            try:
                model_obj = TABLE_CLASS(Entry_No_=entry_no)
                model_obj.Record_ID = model_obj.getLatestRecordId()
                for key, value in row.items():
                    # 自动赋值
                    model_obj.__setattr__(key, value)
                db.session.add(model_obj)
                db.session.commit()
            except InvalidRequestError:
                db.session.rollback()

    # xml文件归档
    # @param string xml_path xml源文件路径（完整路径）
    # @param string archive_path 要归档的目录（不含文件名及公司名）
    @staticmethod
    def archive_xml(xml_path, archive_path):
        # 如果目录不存在，就创建
        if not os.path.exists(archive_path):
            os.makedirs(archive_path, 0o777)

        archive_path = "%s/%s" % (archive_path, os.path.basename(xml_path))
        os.replace(xml_path, archive_path)

    # 访问接口/文件时先新增一条API日志，并返回API_Log的主键用于后续更新
    @staticmethod
    def add_new_api_log_when_start(apiSetup: ApiSetup, direction: int = 1, apiPIn: ApiPInSetup = None,
                                   userID: str = None) -> object:
        return Logger.add_new_api_log(apiSetup, direction, apiPIn, userID)

    # 判断是否超时
    @staticmethod
    def time_out_or_not(apiSetup, api_log) -> bool:
        # 开始时间
        start = api_log.ExecuteDT
        # 当前时间
        now = datetime.datetime.now()
        # 间隔设置
        time_out = apiSetup.Time_out
        delta = now - start
        if delta.total_seconds() / 60 > time_out:
            # 超时返回False
            return False
        return True

    # 获得公司信息
    @staticmethod
    def get_company(code) -> Company:
        return db.session.query(Company).filter(Company.Code == code).first()


# DMS接口访问结果
class InterfaceResult:
    # 状态码，可参考DMSBase里的定义
    status = 0
    # 错误消息，成功则为空
    error_msg = ""
    # 消息内容，对应xml或json文本
    content = ""
    # 消息数据，基本上是字典
    data = None

    def __init__(self, status, error_msg="", content="", data=None):
        self.status = status
        self.error_msg = error_msg
        self.content = content
        self.data = data

    def __repr__(self):
        return "<%s> {status=%d, error_msg=%s, length of content=%d}" \
               % (self.__class__, self.status, self.error_msg, len(self.content))


import grequests


# 把对web service的操作封装起来吧
class WebServiceHandler:
    # 认证器
    auth = None
    # 接口设置 @see src.models.dms.ApiSetup
    api_setup = None

    # 构造认证器
    def __init__(self, api_setup: ApiSetup, soap_username: str, soap_password: str):
        self.api_setup = api_setup
        self.auth = HttpNtlmAuth(soap_username, soap_password)

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self, ws_url, envelope, direction, soap_action, async_invoke=False):
        # 新插入一条日志
        logger = DMSBase.add_new_api_log_when_start(self.api_setup, direction=direction)

        if async_invoke:
            req = self.invoke_async(ws_url, soap_action=soap_action, data=envelope)
        else:
            req = self.invoke(ws_url, soap_action=soap_action, data=envelope)

        # 更新日志（只有当状态码为40x，才认为发生错误）
        if 400 <= req.status_code < 500:
            logger.update_api_log_when_finish(status=DMSBase.STATUS_ERROR, error_msg=req.text)
            return True
        else:
            logger.update_api_log_when_finish(status=DMSBase.STATUS_FINISH, data=req.text)
            return False

    # 生成soap报文
    @staticmethod
    def soapEnvelope(method_name, entry_no, command_code):
        postcontent = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><{0} xmlns="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI"><entryNo>{1}</entryNo><_CalledBy>0</_CalledBy><CommandCode>{2}</CommandCode></{0}></soap:Body></soap:Envelope>'.format(
            method_name, entry_no, command_code)
        return postcontent

    # 获取动态ws地址
    # e.g: "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI"
    def soapAddress(self, company_nav_code):
        url = self.api_setup.CallBack_Address
        if '%NAVCOMPANYCODE%' in url:
            url = url.replace('%NAVCOMPANYCODE%', company_nav_code)
        return url

    # 执行请求
    def invoke(self, url, soap_action, data):
        headers = {
            "Content-Type": "text/xml",
            "SOAPAction": soap_action
        }
        req = requests.post(url, headers=headers, auth=self.auth, data=data.encode('utf-8'))
        # print(req)
        return req

    # 将entry_no作为参数写入指定的ws（异步版本）
    def invoke_async(self, url, soap_action, data):
        # print("async ver")
        headers = {
            "Content-Type": "text/xml",
            "SOAPAction": soap_action
        }
        rs = [grequests.post(url, headers=headers, auth=self.auth, data=data.encode('utf-8'))]
        res = grequests.map(rs)
        # print(res)
        if len(res) > 0:
            return res[0]
        return None
