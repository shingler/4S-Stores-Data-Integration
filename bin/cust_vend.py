#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
import logging
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from src.models import navdb
from src.dms.base import WebServiceHandler
from bin import app, db
from src.dms.custVend import CustVend
from src.dms.setup import Setup
from src.models.dms import Company
from src import words
from src.error import ObjectNotFoundError
from logging import config
config.fileConfig("logging.conf")


# @param string company_code 公司代码
# @param string api_code 执行代码
# @param bool retry 是否重试。retry=false将按照地址1执行；为true则按照地址2执行。
# @param string file_path xml的绝对路径
# @param bool async_ws 是否异步调用web service
def main(company_code, api_code, retry=False, file_path=None, async_ws=False):
    # 读取公司信息，创建业务对象
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    if company_info is None:
        raise ObjectNotFoundError(words.WebApi.company_not_found(company_code))

    # 连接nav库
    nav = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                      db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                      company_nav_code=company_info.NAV_Company_Code)
    nav.prepare()

    api_setup = Setup.load_api_setup(company_code, api_code)
    if api_setup is None:
        raise ObjectNotFoundError(words.WebApi.api_not_found(company_code, api_code))
    # 读取数据
    cv_obj = CustVend(company_code, api_code, force_secondary=retry)
    path, data = cv_obj.load_data(api_setup, file_path=file_path)

    # custVend节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    general_node_dict = node_dict["General"]
    custVend_node_dict = node_dict[cv_obj.BIZ_NODE_LV1]

    # 解析数据
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)

    count = cv_obj.get_count_from_data(data["Transaction"], "CustVendInfo")

    # 写入数据
    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict, Type=0, Count=count, XMLFile=path)
    if len(custVend_dict) > 0:
        nav.insertCV(api_p_out=custVend_node_dict, data_dict=custVend_dict, entry_no=entry_no)

    # 读取文件，文件归档
    if api_setup.API_Type == cv_obj.TYPE_FILE or api_setup.Archived_Path != "":
        cv_obj.archive_xml(path, api_setup.Archived_Path)

    # 读取web service
    wsh = WebServiceHandler(api_setup, soap_username=company_info.NAV_WEB_UserID, soap_password=company_info.NAV_WEB_Password)
    if app.config["LOG_ON"] == 1:
        wsh.setLogger(logging.getLogger("%s-%s" % (company_code, api_code)))
    ws_url = wsh.soapAddress(company_info.NAV_Company_Code)
    ws_env = WebServiceHandler.soapEnvelope(entry_no=entry_no, command_code=api_setup.CallBack_Command_Code)
    wsh.call_web_service(ws_url, ws_env, direction=cv_obj.DIRECT_NAV, soap_action=api_setup.CallBack_SoapAction, async_invoke=async_ws)
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "CustVendInfo"
    entry_no = main(company_code, api_code, retry=False)
    print("脚本运行成功，EntryNo=%s" % entry_no)
