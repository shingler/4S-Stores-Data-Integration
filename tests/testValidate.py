#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试数据校验
import pytest
import xmltodict
from src import validator

xml_cv = '''<?xml version="1.0" encoding="UTF-8"?>
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
xml_fa = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction>
    <General>
        <DMSCode>28976</DMSCode>
        <DMSTitle>Hangzhou Junbaohang</DMSTitle>
        <CompanyCode>28976</CompanyCode>
        <CompanyTitle>Hangzhou Junbaohang</CompanyTitle>
        <CreateDateTime>2011-11-10T15:33:16.753+08:00</CreateDateTime>
        <Creator>AC09CDD6</Creator>
    </General>
    <FA>
        <FANo>FA0001</FANo>
        <Description>本文整理汇总了Python中sqlalchemy.insert方法的典型用法代码示例。如果您正苦于以下问题：Python sqlalchemy.insert方法的具体用法？Python sqlalchemy.insert怎么用？Python sqlalchemy.insert使用的例子？那么恭喜您, 这里精选的方法代码示例或许可以为您提供帮助。</Description>
        <SerialNo>2123453</SerialNo>
        <Inactive>false</Inactive>
        <Blocked>false</Blocked>
        <FAClassCode>TANGIBLE</FAClassCode>
        <FASubclassCode>EQUIPOFFI</FASubclassCode>
        <FALocationCode></FALocationCode>
        <BudgetedAsset>false</BudgetedAsset>
        <VendorNo></VendorNo>
        <MaintenanceVendorNo></MaintenanceVendorNo>
        <UnderMaintenance>false</UnderMaintenance>
        <NextServiceDate></NextServiceDate>
        <WarrantyDate></WarrantyDate>
        <DepreciationPeriod>60</DepreciationPeriod>
        <DepreciationStartingDate>2012-01-04</DepreciationStartingDate>
        <CostCenterCode></CostCenterCode>
    </FA>
</Transaction>'''
xml_inv = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction>
    <General>
        <DMSCode>7000320</DMSCode>
        <DMSTitle>XXXX汽车销售服务有限公司</DMSTitle>
        <CompanyCode>7000320</CompanyCode>
        <CompanyTitle>XXXX汽车销售服务有限公司</CompanyTitle>
        <CreateDateTime>2012-07-03T14:48:36.927Z</CreateDateTime>
        <Creator>sa</Creator>
    </General>
    <Invoice>
        <InvoiceType>ARINV</InvoiceType>
        <INVHeader>
            <InvoiceNo>1183569670</InvoiceNo>
            <PostingDate>2011-02-20</PostingDate>
            <DocumentDate>2011-02-19</DocumentDate>
            <DueDate>2011-02-19</DueDate>
            <PayToBillToNo>835194</PayToBillToNo>
            <SellToBuyFromNo>835194</SellToBuyFromNo>
            <CostCenterCode></CostCenterCode>
            <VehicleSeries></VehicleSeries>
            <ExtDocumentNo></ExtDocumentNo>
            <PriceIncludeVAT>false</PriceIncludeVAT>	
            <Description>在下文中一共展示了sqlalchemy.insert方法的30个代码示例，这些例子默认根据受欢迎程度排序。您可以为喜欢或者感觉有用的代码点赞，您的评价将有助于我们的系统推荐出更棒的Python代码示例。</Description>
            <Location>SR</Location>		
        </INVHeader>
        <INVLine>
            <LineNo>1</LineNo>
            <DMSItemType></DMSItemType>
            <GLAccount>6001040101</GLAccount>
            <Description>4 车轮 已平衡</Description>
            <CostCenterCode>41</CostCenterCode>
            <VehicleSeries>P0104</VehicleSeries>
            <VINNo>WP1AB2920FLA58047</VINNo>
            <QTY>1</QTY>
            <LineAmount>1000</LineAmount>
            <LineCost>0</LineCost>
            <LineDiscountAmount>0</LineDiscountAmount>
            <LineVATAmount>130</LineVATAmount>
            <LineVATRate>0.13</LineVATRate>
            <TransactionType></TransactionType>
            <WIPNo></WIPNo>
            <FromCompanyName></FromCompanyName>
            <ToCompanyName></ToCompanyName>	
            <Location>SR</Location>
            <MovementType></MovementType>
        </INVLine>
        <INVLine>
            <LineNo>2</LineNo>
            <DMSItemType></DMSItemType>
            <GLAccount>6001030104</GLAccount>
            <Description>多用途添加剂，用于 汽油燃料|多用途添加剂，用于 汽油燃料|多用途添加剂，用于 汽油燃料|多用途添加剂，用于 汽油燃料</Description>
            <CostCenterCode>41</CostCenterCode>
            <VehicleSeries>P0104</VehicleSeries>
            <VINNo>WP1AB2920FLA58047</VINNo>
            <QTY>1</QTY>
            <LineAmount>2000</LineAmount>
            <LineCost>0</LineCost>
            <LineDiscountAmount>0</LineDiscountAmount>
            <LineVATAmount>260</LineVATAmount>
            <LineVATRate>0.13</LineVATRate>
            <TransactionType></TransactionType>
            <WIPNo>SRV_320_20_012129</WIPNo>
            <FromCompanyName></FromCompanyName>
            <ToCompanyName></ToCompanyName>	
            <Location>SR</Location>
            <MovementType></MovementType>
        </INVLine>
    </Invoice>
    <Invoice>
        <InvoiceType>ARINV</InvoiceType>
        <INVHeader>
            <InvoiceNo>1183569670</InvoiceNo>
            <PostingDate>2011-02-20</PostingDate>
            <DocumentDate>2011-02-19</DocumentDate>
            <DueDate>2011-02-19</DueDate>
            <PayToBillToNo>835194</PayToBillToNo>
            <SellToBuyFromNo>835194</SellToBuyFromNo>
            <CostCenterCode></CostCenterCode>
            <VehicleSeries></VehicleSeries>
            <ExtDocumentNo></ExtDocumentNo>
            <PriceIncludeVAT>false</PriceIncludeVAT>	
            <Description>test</Description>
            <Location>SR</Location>		
        </INVHeader>
        <INVLine>
            <LineNo>2</LineNo>
            <DMSItemType></DMSItemType>
            <GLAccount>6001030104</GLAccount>
            <Description>多用途添加剂，用于 汽油燃料|多用途添加剂，用于 汽油燃料|多用途添加剂，用于 汽油燃料|多用途添加剂，用于 汽油燃料</Description>
            <CostCenterCode>41</CostCenterCode>
            <VehicleSeries>P0104</VehicleSeries>
            <VINNo>WP1AB2920FLA58047</VINNo>
            <QTY>1</QTY>
            <LineAmount>2000</LineAmount>
            <LineCost>0</LineCost>
            <LineDiscountAmount>0</LineDiscountAmount>
            <LineVATAmount>260</LineVATAmount>
            <LineVATRate>0.13</LineVATRate>
            <TransactionType></TransactionType>
            <WIPNo>SRV_320_20_012129</WIPNo>
            <FromCompanyName></FromCompanyName>
            <ToCompanyName></ToCompanyName>	
            <Location>SR</Location>
            <MovementType></MovementType>
        </INVLine>
    </Invoice>
</Transaction>
'''
xml_other = '''<?xml version="1.0" encoding="UTF-8"?>
<Transaction>
    <General>
        <DMSCode>7000320</DMSCode>
        <DMSTitle>XXXX汽车销售服务有限公司</DMSTitle>
        <CompanyCode>7000320</CompanyCode>
        <CompanyTitle>XXXX汽车销售服务有限公司</CompanyTitle>
        <CreateDateTime>2012-07-03T14:48:36.927Z</CreateDateTime>
        <Creator>sa</Creator>
    </General>
    <Daydook>
        <DaydookNo>XXXXX</DaydookNo>
        <Line>
            <TransactionType>Default</TransactionType>
            <LineNo>1</LineNo>
            <PostingDate>2012-02-14</PostingDate>
            <DocumentDate>2012-02-14</DocumentDate>
            <ExtDocumentNo></ExtDocumentNo>
            <AccountType>G/L Account</AccountType>
            <AccountNo>220201</AccountNo>
            <Description>支付配件款pay for spareparts</Description>
            <DebitValue>398131.81</DebitValue>
            <CreditValue>0</CreditValue>
            <CostCenterCode></CostCenterCode>
            <VehicleSeries></VehicleSeries>
            <VINNo></VINNo>
            <WIPNo></WIPNo>
            <FAPostingType></FAPostingType>
            <EntryType>Normal</EntryType>
            <FromCompanyName></FromCompanyName>
            <ToCompanyName></ToCompanyName>
            <SourceType>Customer</SourceType>
            <SourceNo>C0000001</SourceNo>
            <DMSItemType></DMSItemType>
            <DMSItemTransType></DMSItemTransType>
            <Location>SR</Location>
        </Line>
        <Line>
            <TransactionType>Default</TransactionType>
            <LineNo>2</LineNo>
            <PostingDate>2012-02-14</PostingDate>
            <DocumentDate>2012-02-14</DocumentDate>
            <ExtDocumentNo></ExtDocumentNo>
            <AccountType>G/L Account</AccountType>
            <AccountNo>100201</AccountNo>
            <Description>支付配件款pay for spareparts|支付配件款pay for spareparts|支付配件款pay for spareparts|支付配件款pay for spareparts</Description>
            <DebitValue>0</DebitValue>
            <CreditValue>398131.81</CreditValue>
            <CostCenterCode></CostCenterCode>
            <VehicleSeries></VehicleSeries>
            <VINNo></VINNo>
            <WIPNo></WIPNo>
            <FAPostingType></FAPostingType>
            <EntryType>Normal</EntryType>
            <FromCompanyName></FromCompanyName>
            <ToCompanyName></ToCompanyName>
            <SourceType>Bank Account</SourceType>
            <SourceNo>BNK_320_11_00003</SourceNo>
            <DMSItemType></DMSItemType>
            <DMSItemTransType></DMSItemTransType>
            <Location>SR</Location>
        </Line>
    </Daydook>
    <Daydook>
        <DaydookNo>XXXXX</DaydookNo>
        <Line>
            <TransactionType>Default</TransactionType>
            <LineNo>1</LineNo>
            <PostingDate>2012-02-14</PostingDate>
            <DocumentDate>2012-02-14</DocumentDate>
            <ExtDocumentNo></ExtDocumentNo>
            <AccountType>G/L Account</AccountType>
            <AccountNo>220201</AccountNo>
            <Description>支付配件款pay for spareparts</Description>
            <DebitValue>398131.81</DebitValue>
            <CreditValue>0</CreditValue>
            <CostCenterCode></CostCenterCode>
            <VehicleSeries></VehicleSeries>
            <VINNo></VINNo>
            <WIPNo></WIPNo>
            <FAPostingType></FAPostingType>
            <EntryType>Normal</EntryType>
            <FromCompanyName></FromCompanyName>
            <ToCompanyName></ToCompanyName>
            <SourceType>Customer</SourceType>
            <SourceNo>C0000001</SourceNo>
            <DMSItemType></DMSItemType>
            <DMSItemTransType></DMSItemTransType>
            <Location>SR</Location>
        </Line>
    </Daydook>
</Transaction>
'''

def test_valid_cv():
    data_dict = xmltodict.parse(xml_cv)
    for k, v in data_dict["Transaction"]["General"].items():
        is_valid = validator.DMSInterfaceInfoValidator.check_chn_length(k, v)
        if k == "DMSTitle":
            assert is_valid == True
        elif k == "CompanyTitle":
            assert is_valid == False

    data_list = data_dict["Transaction"]["CustVendInfo"]
    if type(data_dict["Transaction"]["CustVendInfo"]) != list:
        data_list = [data_list]
    i = 0
    for line in data_list:
        for k, v in line.items():
            is_valid = validator.CustVendInfoValidator.check_chn_length(k, v)
            if i == 0 and k == "Name":
                assert is_valid == False
        i += 1


def test_valid_fa():
    data_dict = xmltodict.parse(xml_fa)
    for k, v in data_dict["Transaction"]["General"].items():
        is_valid = validator.DMSInterfaceInfoValidator.check_chn_length(k, v)
        if k == "DMSTitle":
            assert is_valid == True
        elif k == "CompanyTitle":
            assert is_valid == True

    data_list = data_dict["Transaction"]["FA"]
    if type(data_list) != list:
        data_list = [data_list]
    i = 0
    for line in data_list:
        for k, v in line.items():
            is_valid = validator.FAValidator.check_chn_length(k, v)
            if i == 0 and k == "Description":
                assert is_valid == False
        i += 1


def test_valid_inv():
    data_dict = xmltodict.parse(xml_inv)
    for k, v in data_dict["Transaction"]["General"].items():
        is_valid = validator.DMSInterfaceInfoValidator.check_chn_length(k, v)
        if k == "DMSTitle":
            assert is_valid == True
        elif k == "CompanyTitle":
            assert is_valid == True

    data_list = data_dict["Transaction"]["Invoice"]
    if type(data_list) != list:
        data_list = [data_list]
    i = 0
    for invoice in data_list:
        # 发票头
        inv_header = invoice["INVHeader"]
        for k, v in inv_header.items():
            is_valid = validator.InvoiceHeaderValidator.check_chn_length(k, v)
            if i == 0 and k == "Description":
                assert is_valid == False
            elif i == 1 and k == "Description":
                assert is_valid == True
        # 发票明细
        j = 0
        inv_line = invoice["INVLine"]
        if type(inv_line) != list:
            inv_line = [inv_line]
        for line in inv_line:
            for k, v in line.items():
                is_valid = validator.InvoiceLineValidator.check_chn_length(k, v)
                if i == 0 and j == 1 and k == "Description":
                    # print(v, validator.InvoiceLine.chn_length(v), is_valid)
                    assert is_valid == False
                elif i == 1 and j == 0 and k == "Description":
                    assert is_valid == False
            j += 1
        i += 1


def test_valid_other():
    data_dict = xmltodict.parse(xml_other)
    for k, v in data_dict["Transaction"]["General"].items():
        is_valid = validator.DMSInterfaceInfoValidator.check_chn_length(k, v)
        if k == "DMSTitle":
            assert is_valid == True
        elif k == "CompanyTitle":
            assert is_valid == True

    data_list = data_dict["Transaction"]["Daydook"]
    if type(data_list) != list:
        data_list = [data_list]
    i = 0
    for dd in data_list:
        lines = dd["Line"]
        if type(lines) != list:
            lines = [lines]
        j = 0
        for line in lines:
            for k, v in line.items():
                is_valid = validator.OtherValidator.check_chn_length(k, v)
                if i == 0 and j == 1 and k == "Description":
                    # print(v, validator.InvoiceLine.chn_length(v), is_valid)
                    assert is_valid == False
            j += 1
        i += 1


def test_chn_length():
    txt = "你好啊,123"
    assert validator.DMSInterfaceInfoValidator.chn_length(txt) == 10
