#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from src.dms.base import WebServiceHandler
from bin import app, db
from src.dms.fa import FA
from src.dms.setup import Setup
from src.models.dms import Company


# @param string company_code 公司代码
# @param string api_code 执行代码
# @param bool retry 是否重试。retry=false将按照地址1执行；为true则按照地址2执行。
# @param string file_path xml的绝对路径
# @param bool async_ws 是否异步调用web service
def main(company_code, api_code, retry=False, file_path=None, async_ws=False):
    # 读取公司信息，创建业务对象
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    fa_obj = FA(company_info.NAV_Company_Code, force_secondary=retry)

    # 保存数据到nav，需要修改数据库连接设置
    conn_str = company_info.get_nav_connection_string(app.config)
    app.config["SQLALCHEMY_BINDS"][
        "%s-nav" % company_info.NAV_Company_Code] = conn_str

    # 读取API设置，拿到数据
    api_setup = Setup.load_api_setup(company_code, api_code)
    xml_src_path, data = fa_obj.load_data(api_setup, file_path=file_path)

    # 读取输出设置，保存General
    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    general_dict = fa_obj.splice_general_info(data, node_dict=general_node_dict)

    entry_no = fa_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=1,
        Count=fa_obj.get_count_from_data(data["Transaction"], fa_obj.BIZ_NODE_LV1),
        XMLFile=xml_src_path if xml_src_path else "")

    # FA节点配置
    fa_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type=fa_obj.BIZ_NODE_LV1)
    # 拼接fa数据
    fa_dict = fa_obj.splice_data_info(data, node_dict=fa_node_dict)

    if len(fa_dict) > 0:
        fa_obj.save_data_to_nav(nav_data=fa_dict, entry_no=entry_no, TABLE_CLASS=fa_obj.TABLE_CLASS)

    # 读取文件，文件归档
    fa_obj.archive_xml(xml_src_path, api_setup.Archived_Path)

    # 读取web service
    wsh = WebServiceHandler(api_setup, soap_username=company_info.NAV_WEB_UserID,
                            soap_password=company_info.NAV_WEB_Password)
    ws_url = wsh.soapAddress(company_info.NAV_Company_Code)
    ws_env = WebServiceHandler.soapEnvelope(method_name=fa_obj.WS_METHOD, entry_no=entry_no)
    wsh.call_web_service(ws_url, ws_env, direction=fa_obj.DIRECT_NAV, async_invoke=async_ws,
                         soap_action=fa_obj.WS_ACTION)
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "FA-xml-correct"
    entry_no = main(company_code, api_code, retry=False)
    print("脚本运行成功，EntryNo=%s" % entry_no)
