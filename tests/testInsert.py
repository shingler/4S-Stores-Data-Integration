#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试以sql的方式入库nav
import pytest

from src import Company
from src.dms.custVend import CustVend
from src.dms.setup import Setup
from src.models import navdb

company_code = "K302ZH"
check_repeat = False


# @pytest.mark.skip("先测别的")
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
    print(custVend_node_dict)
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)

    count = cv_obj.get_count_from_data(data["Transaction"], "CustVendInfo")

    entry_no = navdb.writeInterfaceInfo(company_info.NAV_Company_Code, api_p_out=general_node_dict,
                                        data_dict=general_dict, Type=0, Count=count, XMLFile=path)
    assert entry_no != 0

    # 写cv数据
    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)

    navdb.writeCV(company_info.NAV_Company_Code, api_p_out=custVend_node_dict, data_dict=custVend_dict, entry_no=entry_no)


@pytest.mark.skip("先测别的")
def test_fa(init_app):
    api_code = "FA-xml-correct"


@pytest.mark.skip("先测别的")
def test_inv(init_app):
    api_code = "Invoice-xml-correct"


@pytest.mark.skip("先测别的")
def test_other(init_app):
    api_code = "Other-xml-correct"
