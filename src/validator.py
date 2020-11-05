#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用于做数据合法性校验


class DMSInterfaceInfo:
    chn_leng = {
        "DMSTitle": 50,
        "CompanyTitle": 50
    }

    @classmethod
    def check_chn_length(cls, key, value):
        if key not in cls.chn_leng:
            return True
        elif len(value)/2 <= cls.chn_leng[key]:
            # 按照旧版本的sql server的规定，一个汉字为两个字符
            return True
        else:
            return False


class CustVendInfo(DMSInterfaceInfo):
    chn_leng = {
        "Name": 50,
        "Address": 50,
        "Address_2": 50
    }


class FA(DMSInterfaceInfo):
    chn_leng = {
        "Description": 30,
        "SerialNo": 30
    }


class InvoiceHeader(DMSInterfaceInfo):
    chn_leng = {
        "Description": 100
    }


class InvoiceLine(DMSInterfaceInfo):
    chn_leng = {
        "Description": 100
    }


class Other(DMSInterfaceInfo):
    chn_leng = {
        "Description": 100
    }
