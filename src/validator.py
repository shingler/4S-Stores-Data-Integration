#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用于做数据合法性校验


class DMSInterfaceInfoValidator:
    _chn_leng = {
        "DMSTitle": 50,
        "CompanyTitle": 50
    }

    @classmethod
    def check_chn_length(cls, key, value):
        if key not in cls._chn_leng:
            return True
        elif cls.chn_length(value) <= cls._chn_leng[key]:
            # 按照旧版本的sql server的规定，一个汉字为两个字符
            return True
        else:
            return False

    @classmethod
    # 按照一个汉字为两个字符计数
    def chn_length(cls, txt):
        if txt is None:
            return 0
        lenTxt = len(txt)
        lenTxt_utf8 = len(txt.encode('utf-8'))
        # utf-8一个汉字占3个字符，减去原计数就是多出来的2/3，再除以2就是增量。再加回去即可
        size = int((lenTxt_utf8 - lenTxt) / 2 + lenTxt)
        return size


class CustVendInfoValidator(DMSInterfaceInfoValidator):
    _chn_leng = {
        "Name": 50,
        "Address": 50,
        "Address_2": 50
    }


class FAValidator(DMSInterfaceInfoValidator):
    _chn_leng = {
        "Description": 30,
        "SerialNo": 30
    }


class InvoiceHeaderValidator(DMSInterfaceInfoValidator):
    _chn_leng = {
        "Description": 100
    }


class InvoiceLineValidator(DMSInterfaceInfoValidator):
    _chn_leng = {
        "Description": 100
    }


class OtherValidator(DMSInterfaceInfoValidator):
    _chn_leng = {
        "Description": 100
    }
