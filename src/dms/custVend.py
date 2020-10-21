#!/usr/bin/python
# -*- coding:utf-8 -*-
from .base import DMSBase
from src.models import nav
from src import db


class CustVend(DMSBase):
    TABLE_CLASS = None
    BIZ_NODE_LV1 = "CustVendInfo"

    def __init__(self, company_name, force_secondary=False):
        super(__class__, self).__init__(company_name, force_secondary)
        # 根据公司名动态获得nav表名
        self.TABLE_CLASS = nav.custVendBuffer(company_name)

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1, node_type="list")
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass
