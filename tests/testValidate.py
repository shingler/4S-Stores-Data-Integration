#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试数据校验
import pytest
import xmltodict
from src import validator

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction>
    <General>
        <DMSCode>7000320</DMSCode>
        <DMSTitle>中国太平洋财产保险股份有限公司宁波分公司</DMSTitle>
        <CompanyCode>7000320</CompanyCode>
        <CompanyTitle>中国太平洋财产保险股份有限公司宁波分公司|中国太平洋财产保险股份有限公司宁波分公司</CompanyTitle>
        <CreateDateTime>2012-07-03T14:48:36.927Z</CreateDateTime>
        <Creator>sa</Creator>
    </General>
    <CustVendInfo>
        <Type>Customer</Type>
        <No>835194</No>
        <Name>中国太平洋财产保险股份有限公司宁波分公司|中国太平洋财产保险股份有限公司宁波分公司</Name>
        <Address></Address>
        <Address2></Address2>		
        <PhoneNo>1234567</PhoneNo>
        <FaxNo>1234567</FaxNo>
        <Blocked></Blocked>
        <Email></Email>
        <Postcode></Postcode>
        <City>杭州市</City>
        <Country>CN-0086</Country>
        <Currency>RMB</Currency>
        <ARAPAccountNo>112201</ARAPAccountNo>
        <PricesIncludingVAT>true</PricesIncludingVAT>
        <ApplicationMethod></ApplicationMethod>
        <PaymentTermsCode></PaymentTermsCode>
        <PaymentMethodCode></PaymentMethodCode>
        <CostCenterCode></CostCenterCode>
        <Template></Template>
        <ICPartnerCode></ICPartnerCode>
    </CustVendInfo>
    <CustVendInfo>
        <Type>Vendor</Type>
        <No>V00000002</No>
        <Name>XXXX汽车贸易有限公司</Name>
        <Address></Address>
        <Address2></Address2>
        <PhoneNo>1234567</PhoneNo>
        <FaxNo>1234567</FaxNo>
        <Blocked></Blocked>
        <Email></Email>
        <Postcode></Postcode>
        <City>北京市</City>
        <Country>CN-0086</Country>
        <Currency>RMB</Currency>
        <ARAPAccountNo>11230102</ARAPAccountNo>
        <PricesIncludingVAT>true</PricesIncludingVAT>
        <ApplicationMethod></ApplicationMethod>
        <PaymentTermsCode></PaymentTermsCode>
        <PaymentMethodCode></PaymentMethodCode>
        <CostCenterCode></CostCenterCode>
        <Template></Template>
        <ICPartnerCode></ICPartnerCode>
    </CustVendInfo>
</Transaction>
'''


def test_valid():
    data_dict = xmltodict.parse(xml)
    print(type(data_dict["Transaction"]["General"]))
    print(data_dict["Transaction"]["General"])
    for k, v in data_dict["Transaction"]["General"].items():
        is_valid = validator.DMSInterfaceInfo.check_chn_length(k, v)
        if k == "DMSTitle":
            assert is_valid == True
        elif k == "CompanyTitle":
            assert is_valid == False


def test_chn_length():
    txt = "你好啊,123"
    assert validator.DMSInterfaceInfo.chn_length(txt) == 10
