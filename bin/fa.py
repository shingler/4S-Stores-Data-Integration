#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import os
import sys
from logging import config

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from src.models import navdb
from src.dms.base import WebServiceHandler
from bin import app, db
from src.dms.fa import FA
from src.dms.setup import Setup
from src.models.dms import Company
from src import words
from src.error import ObjectNotFoundError

config.fileConfig(os.path.join(rootPath, "logging.conf"))


# @param string company_code 公司代码
# @param string api_code 执行代码
# @param bool retry 是否重试。retry=false将按照地址1执行；为true则按照地址2执行。
# @param string file_path xml的绝对路径（手动调用时）
# @param dict p_in 输入参数（手动调用时）
# @param string userID 手动调用时传入调用者ID
def main(company_code, api_code, retry=False, file_path=None, p_in: dict = None, userID: str = None):
    # 读取公司信息，创建业务对象
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    if company_info is None:
        raise ObjectNotFoundError(words.WebApi.company_not_found(company_code))

    # 读取api设置
    api_setup = Setup.load_api_setup(company_code, api_code)
    if api_setup is None:
        raise ObjectNotFoundError(words.WebApi.api_not_found(company_code, api_code))

    # 连接nav数据库
    nav = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                      db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                      company_nav_code=company_info.NAV_Company_Code)
    nav.prepare()

    fa_obj = FA(company_code, api_code, force_secondary=retry)
    # 手动调用时设置输入参数
    if p_in is not None:
        fa_obj.set_p_in(p_in)
    path, data = fa_obj.load_data(api_setup, file_path=file_path, userID=userID)

    # 节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    general_node_dict = node_dict['General']
    fa_node_dict = node_dict[fa_obj.BIZ_NODE_LV1]

    # 拼接数据
    general_dict = fa_obj.splice_general_info(data, node_dict=general_node_dict)
    fa_dict = fa_obj.splice_data_info(data, node_dict=fa_node_dict)
    count = fa_obj.get_count_from_data(data["Transaction"], fa_obj.BIZ_NODE_LV1)

    # 写入数据
    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict, Type=1, Count=count, XMLFile=path)
    if len(fa_dict) > 0:
        nav.insertFA(api_p_out=fa_node_dict, data_dict=fa_dict,
                 entry_no=entry_no)

    # 读取文件，文件归档
    if api_setup.API_Type == fa_obj.TYPE_FILE and api_setup.Archived_Path != "":
        fa_obj.archive_xml(path, api_setup.Archived_Path)

    # 读取web service
    wsh = WebServiceHandler(api_setup, soap_username=company_info.NAV_WEB_UserID,
                            soap_password=company_info.NAV_WEB_Password)
    if app.config["LOG_ON"] == 1:
        wsh.setLogger(logging.getLogger("%s-%s" % (company_code, api_code)))
    ws_url = wsh.soapAddress(company_info.NAV_Company_Code)
    ws_env = WebServiceHandler.soapEnvelope(entry_no=entry_no, command_code=api_setup.CallBack_Command_Code)
    wsh.call_web_service(ws_url, ws_env, direction=fa_obj.DIRECT_NAV, soap_action=api_setup.CallBack_SoapAction, userID=userID)
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "FA"
    entry_no = main(company_code, api_code, retry=False)
    print("脚本运行成功，EntryNo=%s" % entry_no)
