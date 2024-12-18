#!/usr/bin/python
# -*- coding:utf-8 -*-
# 公用逻辑：
# 1. 根据公司列表和接口设置确定数据源
# 2. 从数据源（xml / json）读取数据
# 3. 读取DMS_API_P_Out读取要保存的General的字段
# 4. 根据配置字段将数据里的数据写入InterfaceInfo并返回entry no
import datetime
import json
import logging
import os
import threading
import time
from collections import OrderedDict

import requests
import xmltodict
from requests_ntlm import HttpNtlmAuth
from sqlalchemy.exc import InvalidRequestError

from src import db, Company, ApiSetup, ApiPInSetup
from src.dms import interface
from src.dms.logger import Logger
from src.dms.setup import Setup
from src.error import DataFieldEmptyError, DataLoadError, DataLoadTimeOutError, DataImportRepeatError, \
    DataContentTooBig, NodeNotExistError
from src.models import to_local_time, dms, navdb
from src import words
from src.validator import DMSInterfaceInfoValidator


class DMSBase:
    # 公司代码
    company_code = ""
    # API代码
    api_code = ""

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

    # 根节点名
    NODE_LV0 = "Transaction"

    # DMS接口输入参数
    P_IN = []

    def __init__(self, company_code, api_code, force_secondary=False, check_repeat=True):
        self.company_code = company_code
        self.api_code = api_code
        self.force_secondary = force_secondary
        self.check_repeat = check_repeat
        self.P_IN = []

    # 拼接xml文件路径
    # @param src.models.dms.ApiSetup apiSetup
    def _splice_xml_file_path(self, apiSetUp: dms.ApiSetup) -> str:
        if apiSetUp.API_Type == self.TYPE_API:
            return ""

        cur_date = datetime.datetime.now().strftime("%Y%m%d")
        last_date = (datetime.date.today() + datetime.timedelta(-1)).strftime("%Y%m%d")
        if apiSetUp.File_Name_Format == "":
            raise DataFieldEmptyError(words.DataImport.field_is_empty("File_Name_Format"))

        # 文件名格式支持“PYYYYMMDD”、“PYYYY.MM.DD”，“PYYYY-MM-DD”取前一天日期，不带P取当天日期
        if apiSetUp.File_Name_Format.find("PYYYYMMDD") > -1:
            file_name = apiSetUp.File_Name_Format.replace("PYYYYMMDD", last_date)
        elif apiSetUp.File_Name_Format.find("PYYYY.MM.DD") > -1:
            file_name = apiSetUp.File_Name_Format.replace("PYYYYMMDD", last_date)
        elif apiSetUp.File_Name_Format.find("PYYYY-MM-DD") > -1:
            file_name = apiSetUp.File_Name_Format.replace("PYYYYMMDD", last_date)
        elif apiSetUp.File_Name_Format.find("YYYYMMDD") > -1:
            file_name = apiSetUp.File_Name_Format.replace("YYYYMMDD", cur_date)
        elif apiSetUp.File_Name_Format.find("YYYY.MM.DD") > -1:
            file_name = apiSetUp.File_Name_Format.replace("YYYYMMDD", cur_date)
        elif apiSetUp.File_Name_Format.find("YYYY-MM-DD") > -1:
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

    # 根据手动设置的输入参数，构建APIPIn对象列表
    def set_p_in(self, p_in: dict):
        if len(p_in) == 0:
            return
        for k, v in p_in.items():
            p_in_obj = ApiPInSetup(P_Code=k, Value_Type=5, Value_Source=1, Value=v)
            self.P_IN.append(p_in_obj)

    # 读取接口
    # @param string format 数据解析格式（JSON | XML）
    # @param int time_out 超时时间，单位为秒。为0表示不判断超时
    def _load_data_from_dms_interface(self, apiSetup: dms.ApiSetup):
        # print(self.P_IN)
        if len(self.P_IN) == 0:
            p_in_list = Setup.load_api_p_in(apiSetup.Company_Code, apiSetup.API_Code)
        else:
            p_in_list = self.P_IN

        company_info = db.session.query(Company).filter(Company.Code == apiSetup.Company_Code).first()
        # 请求接口
        req, resp = interface.api_dms(company_info, api_setup=apiSetup, p_in_list=p_in_list)

        # 如果resp是Exception的子类，则说明发生异常被捕获了
        if isinstance(resp, requests.ConnectTimeout):
            return InterfaceResult(status=self.STATUS_TIMEOUT, request=req, error_msg=words.DataImport.load_timeout(resp))
        elif isinstance(resp, Exception):
            return InterfaceResult(status=self.STATUS_ERROR, request=req, error_msg=words.DataImport.json_request_fail(self.company_code, self.api_code, resp))

        if resp.status_code != 200:
            return InterfaceResult(status=self.STATUS_ERROR, request=req, error_msg=words.DataImport.json_http_error(self.company_code, self.api_code, resp.status_code))
        # 完整的返回内容，用于入日志表
        original_result = resp.text
        # 业务处理需要做一些加工
        code, res = interface.parse(resp.json())
        if code != '200':
            return InterfaceResult(status=self.STATUS_ERROR, content=original_result, request=req, error_msg=words.DataImport.json_request_fail(self.company_code, self.api_code, res))
        if res is None:
            return InterfaceResult(status=self.STATUS_ERROR, content=original_result, request=req)
        elif len(res) == 0:
            return InterfaceResult(status=self.STATUS_ERROR, content=original_result, request=req, error_msg=words.DataImport.json_is_empty(self.company_code, self.api_code))
        else:
            return InterfaceResult(status=self.STATUS_FINISH, content=original_result, request=req, data=res)

    # 读取xml,返回InterfaceResult对象
    # @param string format 数据解析格式（JSON | XML）
    # @param int file_size_limit 文件大小限制，单位为M。为0表示无限制
    def _load_data_from_file(self, path, format="xml", file_size_limit=0):
        # 文件是否存在
        if not os.path.exists(path):
            error_msg = words.DataImport.file_not_exist(path)
            return InterfaceResult(status=self.STATUS_ERROR, error_msg=error_msg)
        # 文件大小检查
        try:
            filesize = os.path.getsize(path)
        except OSError:
            error_msg = words.DataImport.file_not_exist(path)
            return InterfaceResult(status=self.STATUS_ERROR, error_msg=error_msg)
        filesize = filesize / 1024 / 1024

        if 0 < file_size_limit < filesize:
            return InterfaceResult(status=self.STATUS_ERROR, error_msg=words.DataImport.file_too_big(file_size_limit, round(filesize, 2)))

        # 重复性检查
        repeated = self.checkRepeatImport(path)
        if self.check_repeat and repeated:
            error_msg = words.DataImport.file_is_repeat(path)
            return InterfaceResult(status=self.STATUS_REPEAT, error_msg=error_msg)

        # 读取文件内容
        with open(path, "r", encoding="UTF-8") as xml_handler:
            data = xml_handler.read()

        res = InterfaceResult(status=self.STATUS_FINISH, content=data)
        if format == self.FORMAT_XML:
            res.data = xmltodict.parse(data)
        else:
            res.data = json.loads(data, encoding="utf-8")
        return res

    # 校验数据长度合法性
    def is_valid(self, data_dict) -> (bool, dict):
        # 检查general
        validator = DMSInterfaceInfoValidator(self.company_code, self.api_code)
        for k, v in data_dict["Transaction"]["General"].items():
            is_valid = validator.check_chn_length(k, v)
            if not is_valid and validator.overleng_handle == validator.OVERLENGTH_WARNING:
                res_bool = False
                res_keys = {
                    "key": "%s.%s" % ("General", k),
                    "expect": validator.expect_length(k),
                    "content": v
                }
                return res_bool, res_keys
            elif not is_valid and validator.overleng_handle == validator.OVERLENGTH_CUT:
                # 按长度截断
                data_dict["Transaction"]["General"][k] = v.encode("gbk")[0:validator.expect_length(k)].decode("gbk")

        # 检查具体部分，由子类实现
        res_bool2, res_keys2 = self._is_valid(data_dict)
        return res_bool2, res_keys2

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
            path = apiSetup.API_Address1
            res = self._load_data_from_dms_interface(apiSetup)
        elif apiSetup.API_Type == self.TYPE_FILE and file_path is not None:
            # 直接提供XML地址
            path = file_path
            res = self._load_data_from_file(file_path, format=apiSetup.Data_Format, file_size_limit=apiSetup.File_Max_Size)
        elif apiSetup.API_Type == self.TYPE_FILE:
            # 使用当天的XML文件
            try:
                path = self._splice_xml_file_path(apiSetup)
            except DataFieldEmptyError as dfe:
                # 记录错误日志并再次抛出异常
                logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=str(dfe))
                raise DataFieldEmptyError(str(dfe))
            res = self._load_data_from_file(path, format=apiSetup.Data_Format, file_size_limit=apiSetup.File_Max_Size)
        # print(res)

        # 根据结果进行后续处理
        if res.status == self.STATUS_ERROR:
            # 记录错误日志并抛出异常
            logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=res.error_msg, p_in=res.request)
            raise DataLoadError(res.error_msg)
        elif res.status == self.STATUS_TIMEOUT:
            # 记录错误日志并抛出异常
            logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=res.error_msg, p_in=res.request)
            raise DataLoadTimeOutError(res.error_msg)
        elif res.status == self.STATUS_REPEAT:
            # 记录错误日志并抛出异常
            logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=res.error_msg, p_in=res.request)
            raise DataImportRepeatError(res.error_msg)
        else:
            # 处理成功，校验数据完整性
            is_integrity, keys = self.is_integrity(res.data, apiSetup.Company_Code, apiSetup.API_Code)
            # print(is_integrity, keys)
            if not is_integrity:
                error_msg = words.DataImport.node_not_exists(keys)
                logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=error_msg, data=res.content, p_in=res.request)
                raise NodeNotExistError(error_msg)

            # 处理成功，校验数据长度是否合法
            is_valid, keys = self.is_valid(res.data)
            # print(is_valid, keys)
            if not is_valid:
                error_msg = words.DataImport.content_is_too_big(path, keys, )
                logger.update_api_log_when_finish(status=self.STATUS_ERROR, error_msg=error_msg, data=res.content, p_in=res.request)
                raise DataContentTooBig(error_msg)

            # 校验成功，更新日志
            logger.update_api_log_when_finish(data=res.content, status=self.STATUS_FINISH, p_in=res.request)
            return path, res.data

    # 根据文件名检查是否重复导入
    def checkRepeatImport(self, path: str) -> bool:
        company_info = db.session.query(Company).filter(Company.Code == self.company_code).first()
        nav = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                          db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                          company_nav_code=company_info.NAV_Company_Code, only_tables=["DMSInterfaceInfo"])
        nav.prepare()
        return nav.checkRepeatImport(path)

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
        @param str node_lv0 顶部节点名 Transaction
        @param str node_lv1 一级节点名 General/CustVend/Invoice等等
        @param str node_type 节点类型，node=对象节点，list=数组节点
    '''

    def _splice_field(self, data, node_dict, node_lv0, node_lv1, node_type="node"):
        if node_type == "node":
            # 按单节点（对象）取值
            data_dict = {}
            for key, value in data[node_lv0][node_lv1].items():
                if key in node_dict:
                    data_dict[key] = value
            return data_dict
        else:
            # 按多节点（数组）取值
            data_dict_list = []
            if node_lv1 in data[node_lv0]:
                list_node = data[node_lv0][node_lv1]
                if type(list_node) != list:
                    list_node = [list_node, ]

                for row in list_node:
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

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        pass

    # xml文件归档
    # @param string xml_path xml源文件路径（完整路径）
    # @param string archive_path 要归档的目录（不含文件名及公司名）
    def archive_xml(self, xml_path, archive_path):
        # 如果归档目录为空，则什么都不做
        if archive_path != "":
            # 如果目录不存在，就创建
            if not os.path.exists(archive_path):
                os.makedirs(archive_path, 0o777)

            archive_file_path = os.path.join(archive_path, os.path.basename(xml_path))
            # 如果文件存在则附加当前时间
            if os.path.exists(archive_file_path):
                file_name = "%s_%s%s" % (os.path.splitext(os.path.basename(xml_path))[0], datetime.datetime.now().strftime("%Y%m%d_%H.%M.%S"), os.path.splitext(os.path.basename(xml_path))[1])
                archive_file_path = os.path.join(archive_path, file_name)

            try:
                os.replace(xml_path, archive_file_path)
            except OSError:
                # 归档失败不要影响后续流程
                logger = logging.getLogger("%s-%s" % (self.company_code, self.api_code))
                logger.warning("file archive failed! src={0}, dest={1}".format(xml_path, archive_file_path))

    # 访问接口/文件时先新增一条API日志，并返回API_Log的主键用于后续更新
    @staticmethod
    def add_new_api_log_when_start(apiSetup: ApiSetup, direction: int = 1, apiPIn: list = None,
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
    # 返回的消息数据，基本上是字典
    data = None
    # 请求的数据
    request = None

    def __init__(self, status, error_msg="", content="", data=None, request=None):
        self.status = status
        self.error_msg = error_msg
        self.content = content
        self.data = data
        self.request = request

    def __repr__(self):
        return "<%s> {status=%d, error_msg=%s, length of content=%d}" \
               % (self.__class__, self.status, self.error_msg, len(self.content))


# 把对web service的操作封装起来吧
class WebServiceHandler:
    # 认证器
    auth = None
    # 接口设置 @see src.models.dms.ApiSetup
    api_setup = None
    # 日志对象
    logger = None
    # 超时时间
    timeout = None

    # 构造认证器
    def __init__(self, api_setup: ApiSetup, soap_username: str, soap_password: str):
        self.api_setup = api_setup
        if api_setup.Time_out > 0:
            self.timeout = 60 * api_setup.Time_out
        self.auth = HttpNtlmAuth(soap_username, soap_password)
        if self.logger is not None:
            self.logger.info("web service auth username is {0}, password is {1}".format(soap_username, soap_password))

    # 设置了日志对象才写文件日志
    def setLogger(self, logger: logging.Logger):
        self.logger = logger

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self, ws_url, envelope, direction, soap_action, userID=None):
        if self.logger is not None:
            self.logger.info("web service calling start: ws_url='{0}', envelope='{1}', soap_action='{2}'".format(ws_url, envelope, soap_action))

        # 新插入一条日志
        logger = DMSBase.add_new_api_log_when_start(self.api_setup, direction=direction, userID=userID)

        req = self.invoke(ws_url, soap_action=soap_action, data=envelope)

        # 更新日志（只有当状态码为40x，才认为发生错误）
        if 400 <= req.status_code < 500:
            logger.update_api_log_when_finish(status=DMSBase.STATUS_ERROR, error_msg=req.text)
            return False
        else:
            logger.update_api_log_when_finish(status=DMSBase.STATUS_FINISH, data=req.text)
            return True

    # 生成soap报文
    @staticmethod
    def soapEnvelope(entry_no, command_code):
        postcontent = '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><DMSDataInterfaceIn xmlns="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI"><entryNo>{0}</entryNo><commandCode>{1}</commandCode></DMSDataInterfaceIn></soap:Body></soap:Envelope>'.format(
            entry_no, command_code)
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
        req = requests.post(url, headers=headers, auth=self.auth, data=data.encode('utf-8'), timeout=self.timeout)
        if self.logger is not None:
            self.logger.info("web service calling result: status_code='{0}', text='{1}'".format(req.status_code, req.text))
        return req
