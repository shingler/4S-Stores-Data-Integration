#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
from bin import app
from src.dms.fa import FA
from src.models import nav
from src.error import DataFieldEmptyError


def main(company_code, api_code):
    fa_obj = FA()

    api_setup = fa_obj.load_config_from_api_setup(company_code, api_code)
    xml_src_path = None
    if api_setup.API_Type == 1:
        data = fa_obj.load_data_from_dms_interface()
    else:
        xml_src_path = fa_obj.splice_xml_file_path(api_setup)
        data = fa_obj.load_data_from_xml(xml_src_path)

    general_node_dict = fa_obj.load_api_p_out_nodes(company_code, api_code, node_type="general")
    general_dict = fa_obj.splice_general_info(data, node_dict=general_node_dict)

    entry_no = fa_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=1,
        Count=fa_obj.get_count_from_data(data["Transaction"], fa_obj.BIZ_NODE_LV1),
        XMLFile=xml_src_path if xml_src_path else "")

    # FA节点配置
    fa_node_dict = fa_obj.load_api_p_out_nodes(company_code, api_code, node_type=fa_obj.BIZ_NODE_LV1)
    # 拼接fa数据
    fa_dict = fa_obj.splice_data_info(data, node_dict=fa_node_dict)

    fa_obj.save_data_to_nav(nav_data=fa_dict, entry_no=entry_no, TABLE_CLASS=fa_obj.TABLE_CLASS)

    # cv_obj.call_web_service()


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "FA"
    main(company_code, api_code)
