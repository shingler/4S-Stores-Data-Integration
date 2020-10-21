#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from bin import app, db
from src.dms.custVend import CustVend
from src.dms.setup import Setup
from src.models.dms import Company


# @param string company_code 公司代码
# @param string api_code 执行代码
# @param bool retry 是否重试。retry=false将按照地址1执行；为true则按照地址2执行。
def main(company_code, api_code, retry=False):
    # 读取公司信息，创建业务对象
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    cv_obj = CustVend(company_info.NAV_Company_Code, force_secondary=retry)

    # 保存数据到nav，需要修改数据库连接设置
    conn_str = company_info.get_nav_connection_string(app.config)
    app.config["SQLALCHEMY_BINDS"][
        "%s-nav" % company_info.NAV_Company_Code] = conn_str

    # 读取API设置，拿到数据
    api_setup = Setup.load_api_setup(company_code, api_code)
    xml_src_path, data = cv_obj.load_data(api_setup)

    # 读取输出设置，保存General
    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)
    entry_no = cv_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=0,
        Count=cv_obj.get_count_from_data(data["Transaction"], cv_obj.BIZ_NODE_LV1),
        XMLFile=xml_src_path if xml_src_path else "")

    # custVend节点配置
    custVend_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type=cv_obj.BIZ_NODE_LV1)
    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)
    cv_obj.save_data_to_nav(custVend_dict, entry_no=entry_no, TABLE_CLASS=cv_obj.TABLE_CLASS)

    # cv_obj.call_web_service()
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "CustVendInfo-xml-correct"
    entry_no = main(company_code, api_code, retry=False)
    print(entry_no)
