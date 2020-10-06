#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from bin import app
from src.dms.invoice import InvoiceHeader, InvoiceLine
from src.error import DataFieldEmptyError


def main(company_code, api_code):
    invoiceHeader_obj = InvoiceHeader()
    invoiceLine_obj = InvoiceLine()

    api_setup = invoiceHeader_obj.load_config_from_api_setup(company_code, api_code)
    xml_src_path = None
    if api_setup.API_Type == 1:
        data = invoiceHeader_obj.load_data_from_dms_interface()
    else:
        xml_src_path = invoiceHeader_obj.splice_xml_file_path(api_setup)
        data = invoiceHeader_obj.load_data_from_xml(xml_src_path)

    general_node_dict = invoiceHeader_obj.load_api_p_out_nodes(company_code, api_code, node_type="general")
    general_dict = invoiceHeader_obj.splice_general_info(data, node_dict=general_node_dict)

    entry_no = invoiceHeader_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=2,
        Count=invoiceHeader_obj.get_count_from_data(data["Transaction"], "Invoice"),
        XMLFile=xml_src_path if xml_src_path else "")

    # 发票抬头节点配置
    ih_node_dict = invoiceHeader_obj.load_api_p_out_nodes(company_code, api_code,
                                                          node_type=invoiceHeader_obj.BIZ_NODE_LV1)
    # 拼接发票抬头数据
    ih_dict = invoiceHeader_obj.splice_data_info(data, node_dict=ih_node_dict)

    invoiceHeader_obj.save_data_to_nav(nav_data=ih_dict, entry_no=entry_no, TABLE_CLASS=invoiceHeader_obj.TABLE_CLASS)
    # 发票号
    invoice_no = ih_dict[0]["InvoiceNo"]

    # 发票明细节点配置
    il_node_dict = invoiceLine_obj.load_api_p_out_nodes(company_code, api_code, node_type=invoiceLine_obj.BIZ_NODE_LV1)
    # 拼接发票明细数据
    il_dict = invoiceLine_obj.splice_data_info(data, node_dict=il_node_dict, invoice_no=invoice_no)

    invoiceLine_obj.save_data_to_nav(nav_data=il_dict, entry_no=entry_no, TABLE_CLASS=invoiceLine_obj.TABLE_CLASS)

    # cv_obj.call_web_service()


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "Invoice"
    main(company_code, api_code)
