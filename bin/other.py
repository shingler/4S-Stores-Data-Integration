#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from bin import app, db
from src.dms.other import Other
from src.dms.setup import Setup
from src.models.dms import Company


def main(company_code, api_code, retry=False, cur_date=None):
    # 读取公司信息，创建业务对象
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    other_obj = Other(company_info.NAV_Company_Code, force_secondary=retry)

    # 保存数据到nav，需要修改数据库连接设置
    conn_str = company_info.get_nav_connection_string(app.config)
    app.config["SQLALCHEMY_BINDS"][
        "%s-nav" % company_info.NAV_Company_Code] = conn_str

    # 读取API设置，拿到数据
    api_setup = Setup.load_api_setup(company_code, api_code)
    xml_src_path, data = other_obj.load_data(api_setup, cur_date=cur_date)

    # 读取输出设置，保存General
    general_node_dict = other_obj.load_api_p_out_nodes(company_code, api_code, node_type="General")
    general_dict = other_obj.splice_general_info(data, node_dict=general_node_dict)

    entry_no = other_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=3,
        Count=other_obj.get_count_from_data(data["Transaction"], other_obj.BIZ_NODE_LV1),
        XMLFile=xml_src_path if xml_src_path else "")

    # FA节点配置
    fa_node_dict = other_obj.load_api_p_out_nodes(company_code, api_code, node_type=other_obj.BIZ_NODE_LV1)
    # 拼接fa数据
    fa_dict = other_obj.splice_data_info(data, node_dict=fa_node_dict)

    other_obj.save_data_to_nav(nav_data=fa_dict, entry_no=entry_no, TABLE_CLASS=other_obj.TABLE_CLASS)

    # 读取文件，文件归档
    other_obj.archive_xml(xml_src_path, api_setup.Archived_Path)

    # 调用web service
    other_obj.call_web_service(entry_no, api_setup=api_setup, user_id=company_info.NAV_WEB_UserID,
                                     password=company_info.NAV_WEB_Password)
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "Other-xml-correct"
    main(company_code, api_code, retry=False)
