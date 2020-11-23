#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试以sql的方式入库nav
import pytest

from src import Company, words
from src.dms.base import InterfaceResult
from src.dms.custVend import CustVend
from src.dms.fa import FA
from src.dms.invoice import Invoice, InvoiceHeader, InvoiceLine
from src.dms.other import Other
from src.dms.setup import Setup
from src.error import DataImportRepeatError
from src.models import navdb

company_code = "K302ZH"
check_repeat = False


# @pytest.mark.skip("先测别的")
def test_cv(init_app):
    api_code = "CustVendInfo"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    # 连接nav库
    nav = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                      db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                      company_nav_code=company_info.NAV_Company_Code)
    nav.prepare()

    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None

    cv_obj = CustVend(company_code, api_code, check_repeat=check_repeat)
    path, data = cv_obj.load_data(api_setup)

    # custVend节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    assert node_dict is not None
    general_node_dict = node_dict["General"]
    custVend_node_dict = node_dict[cv_obj.BIZ_NODE_LV1]
    # print(custVend_node_dict)
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)

    count = cv_obj.get_count_from_data(data["Transaction"], "CustVendInfo")

    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict, Type=0, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写cv数据
    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)

    nav.insertCV(api_p_out=custVend_node_dict, data_dict=custVend_dict, entry_no=entry_no)


# @pytest.mark.skip("先测别的")
def test_fa(init_app):
    api_code = "FA"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None

    fa_obj = FA(company_code, api_code, check_repeat=check_repeat)
    path, data = fa_obj.load_data(api_setup)

    # 节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    assert node_dict is not None
    general_node_dict = node_dict['General']
    fa_node_dict = node_dict[fa_obj.BIZ_NODE_LV1]

    general_dict = fa_obj.splice_general_info(data, node_dict=general_node_dict)

    count = fa_obj.get_count_from_data(data["Transaction"], "FA")

    nav = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                      db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                      company_nav_code=company_info.NAV_Company_Code)
    nav.prepare()
    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict, Type=1, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写cv数据
    # 拼接custVend数据
    fa_dict = fa_obj.splice_data_info(data, node_dict=fa_node_dict)

    nav.insertFA(api_p_out=fa_node_dict, data_dict=fa_dict,
                 entry_no=entry_no)


# @pytest.mark.skip("先测别的")
def test_inv(init_app):
    api_code = "Invoice"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    api_setup = Setup.load_api_setup(company_code, api_code)
    invh_obj = InvoiceHeader(company_code, api_code, check_repeat=check_repeat)
    invl_obj = InvoiceLine(company_code, api_code, check_repeat=check_repeat)

    # 节点配置
    # other_node_dict = inv_obj.load_api_p_out_nodes(company_code, api_code, node_type=InvoiceHeader.BIZ_NODE_LV1)
    inv_node_dict = Setup.load_api_p_out(company_code, api_code)

    general_node_dict = inv_node_dict["General"]
    inv_header_node_dict = {**inv_node_dict[InvoiceHeader.BIZ_NODE_LV1], **inv_node_dict[InvoiceHeader.BIZ_NODE_LV2]}
    inv_line_node_dict = {**inv_node_dict[InvoiceLine.BIZ_NODE_LV1], **inv_node_dict[InvoiceLine.BIZ_NODE_LV2]}
    # print("======")
    # print(inv_line_node_dict)
    path, data = invh_obj.load_data(api_setup)

    general_dict = invh_obj.splice_general_info(data, node_dict=general_node_dict)

    count = invh_obj.get_count_from_data(data["Transaction"], InvoiceHeader.BIZ_NODE_LV1)

    nav = navdb.NavDB('127.0.0.1', 'sa', 'msSqlServer2020', 'NAV', company_nav_code=company_info.NAV_Company_Code)
    nav.prepare()
    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict, Type=2, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写发票头数据
    invh_dict = invh_obj.splice_data_info(data, node_dict=inv_header_node_dict)
    nav.insertInvHeader(api_p_out=inv_header_node_dict, data_dict=invh_dict, entry_no=entry_no)

    # 写发票行数据
    invl_dict = invl_obj.splice_data_info(data, node_dict=inv_line_node_dict)
    nav.insertInvLines(api_p_out=inv_line_node_dict, data_dict=invl_dict, entry_no=entry_no)


# @pytest.mark.skip("先测别的")
def test_other(init_app):
    api_code = "Other"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    api_setup = Setup.load_api_setup(company_code, api_code)

    other_obj = Other(company_code, api_code, check_repeat=check_repeat)
    path, data = other_obj.load_data(api_setup)

    # 节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    general_node_dict = node_dict["General"]
    other_node_dict = {**node_dict[other_obj.BIZ_NODE_LV1], **node_dict[other_obj.BIZ_NODE_LV2]}
    # print(other_node_dict)
    general_dict = other_obj.splice_general_info(data, node_dict=general_node_dict)

    count = other_obj.get_count_from_data(data["Transaction"], "Daydook")

    nav = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                      db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                      company_nav_code=company_info.NAV_Company_Code)
    nav.prepare()
    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict, Type=3, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写cv数据
    # 拼接custVend数据
    other_dict = other_obj.splice_data_info(data, node_dict=other_node_dict)

    nav.insertOther(api_p_out=other_node_dict, data_dict=other_dict,
                 entry_no=entry_no)


@pytest.mark.skip("先测别的")
def test():
    nav = navdb.NavDB('127.0.0.1', 'sa', '123', 'NAV')
    nav.prepare()
    print(type(nav.base.classes))
    print(len(nav.base.classes))
    print(nav.base.classes["K302 Zhuhai JJ$CustVendBuffer"])
