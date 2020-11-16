#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试dms的json接口
import pytest
from src.dms import interface
from src import Company
from src.dms.setup import Setup

company_code = "K302ZS"
api_code = "CustVendInfo"


def test_api_cv(init_app):
    # 读取签名配置
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    assert company_info.DMS_Company_Code is not None
    assert company_info.DMS_Group_Code is not None

    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None
    assert api_setup.Secret_Key is not None
    assert api_setup.Signature_Method is not None
    assert api_setup.Command_Code is not None

    p_in_list = Setup.load_api_p_in(company_code, api_code)
    assert type(p_in_list) == list
    assert len(p_in_list) > 0

    res = interface.api_dms(company_info, api_setup, p_in_list)
    assert res is not None
    print(res)

