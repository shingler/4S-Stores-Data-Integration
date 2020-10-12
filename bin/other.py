#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from bin import app
from src.dms.other import Other
from src.dms.setup import Setup


def main(company_code, api_code, retry=False):
    other_obj = Other(force_secondary=retry)

    api_setup = Setup.load_api_setup(company_code, api_code)
    xml_src_path, data = other_obj.load_data(api_setup)

    general_node_dict = other_obj.load_api_p_out_nodes(company_code, api_code, node_type="general")
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

    # cv_obj.call_web_service()
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "Other"
    main(company_code, api_code, retry=True)
