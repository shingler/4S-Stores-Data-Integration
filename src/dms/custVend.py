#!/usr/bin/python
# -*- coding:utf-8 -*-
from .base import DMSBase
from src.models import nav


class CustVend(DMSBase):
    TABLE_CLASS = None
    # 数据一级节点名
    BIZ_NODE_LV1 = "CustVendInfo"
    WS_METHOD = "HandleCVInfoWithEntryNo"
    # NAV的WebService的SOAPAction
    WS_ACTION = "urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI:HandleCVInfoWithEntryNo"

    def __init__(self, company_nav_code, force_secondary=False):
        super(__class__, self).__init__(company_nav_code, force_secondary)
        # 根据公司名动态获得nav表名
        self.TABLE_CLASS = nav.custVendBuffer(company_nav_code)

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1, node_type="list")
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list
