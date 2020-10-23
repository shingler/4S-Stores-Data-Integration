#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys, os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

import requests
from bin import app, db
from src.dms.invoice import InvoiceHeader, InvoiceLine
from src.dms.setup import Setup
from src.models.dms import Company


def main(company_code, api_code, retry=False):
    # 读取公司信息，创建业务对象
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    invoiceHeader_obj = InvoiceHeader(company_info.NAV_Company_Code, force_secondary=retry)
    invoiceLine_obj = InvoiceLine(company_info.NAV_Company_Code)

    # 保存数据到nav，需要修改数据库连接设置
    conn_str = company_info.get_nav_connection_string(app.config)
    app.config["SQLALCHEMY_BINDS"][
        "%s-nav" % company_info.NAV_Company_Code] = conn_str

    # 读取API设置，拿到数据
    api_setup = Setup.load_api_setup(company_code, api_code)
    xml_src_path, data = invoiceHeader_obj.load_data(api_setup)

    # 读取输出设置，保存General
    general_node_dict = invoiceHeader_obj.load_api_p_out_nodes(company_code, api_code, node_type="General")
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

    # 读取文件，文件归档
    invoiceLine_obj.archive_xml(xml_src_path, api_setup.Archived_Path)

    # cv_obj.call_web_service()
    return entry_no


if __name__ == '__main__':
    # 应由task提供
    company_code = "K302ZH"
    api_code = "Invoice-xml-correct"
    main(company_code, api_code, retry=False)
