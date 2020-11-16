#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试以sql的方式入库nav
import pytest

from src import Company
from src.dms.custVend import CustVend
from src.dms.fa import FA
from src.dms.other import Other
from src.dms.setup import Setup
from src.models import navdb

company_code = "K302ZH"
check_repeat = False


@pytest.mark.skip("先测别的")
def test_cv(init_app):
    api_code = "CustVendInfo-xml-correct"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    # 修改bind
    conn_str = company_info.get_nav_connection_string(app.config)
    assert conn_str.startswith(app.config["DATABASE_ENGINE"])
    app.config["SQLALCHEMY_BINDS"]["%s-nav" % company_info.NAV_Company_Code] = conn_str

    api_setup = Setup.load_api_setup(company_code, api_code)

    cv_obj = CustVend(company_info.NAV_Company_Code, check_repeat=check_repeat)
    path, data = cv_obj.load_data(api_setup)

    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    # custVend节点配置
    custVend_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="CustVendInfo")
    # print(custVend_node_dict)
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)

    count = cv_obj.get_count_from_data(data["Transaction"], "CustVendInfo")

    nav = navdb.NavDB('127.0.0.1', 'sa', '123', 'NAV')
    nav.prepare()
    entry_no = nav.insertGeneral(company_info.NAV_Company_Code, api_p_out=general_node_dict,
                                        data_dict=general_dict, Type=0, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写cv数据
    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)

    nav.insertCV(company_info.NAV_Company_Code, api_p_out=custVend_node_dict, data_dict=custVend_dict, entry_no=entry_no)

@pytest.mark.skip("先测别的")
def test_fa(init_app):
    api_code = "FA-xml-correct"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    # 修改bind
    conn_str = company_info.get_nav_connection_string(app.config)
    assert conn_str.startswith(app.config["DATABASE_ENGINE"])
    app.config["SQLALCHEMY_BINDS"]["%s-nav" % company_info.NAV_Company_Code] = conn_str

    api_setup = Setup.load_api_setup(company_code, api_code)

    fa_obj = FA(company_info.NAV_Company_Code, check_repeat=check_repeat)
    path, data = fa_obj.load_data(api_setup)

    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    # 节点配置
    fa_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="FA")
    # print(custVend_node_dict)
    general_dict = fa_obj.splice_general_info(data, node_dict=general_node_dict)

    count = fa_obj.get_count_from_data(data["Transaction"], "FA")

    nav = navdb.NavDB('127.0.0.1', 'sa', '123', 'NAV')
    nav.prepare()
    entry_no = nav.insertGeneral(company_info.NAV_Company_Code, api_p_out=general_node_dict,
                                 data_dict=general_dict, Type=1, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写cv数据
    # 拼接custVend数据
    fa_dict = fa_obj.splice_data_info(data, node_dict=fa_node_dict)

    nav.insertFA(company_info.NAV_Company_Code, api_p_out=fa_node_dict, data_dict=fa_dict,
                 entry_no=entry_no)


@pytest.mark.skip("先测别的")
def test_inv(init_app):
    api_code = "Invoice-xml-correct"


# @pytest.mark.skip("先测别的")
def test_other(init_app):
    api_code = "Other"
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()

    # 修改bind
    conn_str = company_info.get_nav_connection_string(app.config)
    assert conn_str.startswith(app.config["DATABASE_ENGINE"])
    app.config["SQLALCHEMY_BINDS"]["%s-nav" % company_info.NAV_Company_Code] = conn_str

    api_setup = Setup.load_api_setup(company_code, api_code)

    other_obj = Other(company_info.NAV_Company_Code, check_repeat=check_repeat)
    path, data = other_obj.load_data(api_setup)

    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    # 节点配置
    other_node_dict = other_obj.load_api_p_out_nodes(company_code, api_code, node_type="Daydook")
    # print(other_node_dict)
    other_node_dict["Daydook"] = other_obj.load_api_p_out_nodes(company_code, api_code, node_type="Line")
    general_dict = other_obj.splice_general_info(data, node_dict=general_node_dict)

    count = other_obj.get_count_from_data(data["Transaction"], "Daydook")

    nav = navdb.NavDB('127.0.0.1', 'sa', '123', 'NAV')
    nav.prepare()
    entry_no = nav.insertGeneral(company_info.NAV_Company_Code, api_p_out=general_node_dict,
                                 data_dict=general_dict, Type=1, Count=count, XMLFile=path)
    assert entry_no is not None and entry_no != 0
    # 写cv数据
    # 拼接custVend数据
    other_dict = other_obj.splice_data_info(data, node_dict=other_node_dict)

    nav.insertOther(company_info.NAV_Company_Code, api_p_out=other_node_dict, data_dict=other_dict,
                 entry_no=entry_no)


def test():
    nav = navdb.NavDB('127.0.0.1', 'sa', '123', 'NAV')
    nav.prepare()
    print(type(nav.base.classes))
    print(len(nav.base.classes))
    print(nav.base.classes["K302 Zhuhai JJ$CustVendBuffer"])
