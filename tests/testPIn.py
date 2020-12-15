#!/usr/bin/python
# -*- coding:utf-8 -*-
import pytest

from bin import cust_vend


def test_p_in(init_app):
    company_code = "K302ZS"
    api_code = "CustVendInfo"
    file_path = None
    retry = False
    options = {"apiQueryDateEnd":"2020-12-11 23:59:59","apiQueryDateBegin":"2020-12-11 00:00:00"}
    runner = cust_vend
    entry_no = runner.main(company_code=company_code, api_code=api_code, file_path=file_path,
                           p_in=options, retry=True if retry else False)
    assert entry_no is not None
