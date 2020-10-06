#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from bin import app
from src.dms.custVend import CustVend
from src.models import nav
from src.error import DataFieldEmptyError


def main(company_code, api_code):
    cv_obj = CustVend()

    api_setup = cv_obj.load_config_from_api_setup(company_code, api_code)
    xml_src_path = None
    if api_setup.API_Type == 1:
        data = cv_obj.load_data_from_dms_interface()
    else:
        xml_src_path = cv_obj.splice_xml_file_path(api_setup)
        data = cv_obj.load_data_from_xml(xml_src_path)

    general_node_dict = cv_obj.load_api_p_out_nodes(company_code, api_code, node_type="general")
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)

    entry_no = cv_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=0,
        Count=cv_obj.get_count_from_data(data["Transaction"], cv_obj.BIZ_NODE_LV1),
        XMLFile=xml_src_path if xml_src_path else "")

    # custVend节点配置
    custVend_node_dict = cv_obj.load_api_p_out_nodes(company_code, api_code, node_type=cv_obj.BIZ_NODE_LV1)
    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)
    cv_obj.save_data_to_nav(custVend_dict, entry_no=entry_no, TABLE_CLASS=cv_obj.TABLE_CLASS)

    # cv_obj.call_web_service()


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "CustVendInfo"
    main(company_code, api_code)
