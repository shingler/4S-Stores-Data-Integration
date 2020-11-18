#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用于做数据合法性校验
from src.dms.setup import Setup


class DMSInterfaceInfoValidator:
    _table_name = "DMSInterfaceInfo"

    def __init__(self, company_code, api_code):
        conf = Setup.load_api_p_out_value_length(company_code, api_code, self._table_name)
        self._chn_leng = {}
        for item in conf:
            self._chn_leng[item.P_Name] = item.Value_Length
        print(self._chn_leng)

    # 返回字段内容预期长度
    def expect_length(self, key) -> int:
        return self._chn_leng.get(key, 0)

    # 检查value的长度是否符合key的长度配置
    def check_chn_length(self, key, value):
        if key not in self._chn_leng:
            return True
        elif self.chn_length(value) <= self._chn_leng[key]:
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
    _table_name = "CustVendBuffer"


class FAValidator(DMSInterfaceInfoValidator):
    _table_name = "FABuffer"


class InvoiceHeaderValidator(DMSInterfaceInfoValidator):
    _table_name = "InvoiceHeaderBuffer"


class InvoiceLineValidator(DMSInterfaceInfoValidator):
    _table_name = "InvoiceLineBuffer"


class OtherValidator(DMSInterfaceInfoValidator):
    _table_name = "OtherBuffer"
