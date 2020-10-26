#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import db
from src.dms.base import DMSBase
from src.models import nav


class FA(DMSBase):
    TABLE_CLASS = None
    BIZ_NODE_LV1 = "FA"
    WS_METHOD = "HandleFAWithEntryNo"
    WS_ACTION = "urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI:HandleFAWithEntryNo"

    def __init__(self, company_nav_code, force_secondary=False):
        super(__class__, self).__init__(company_nav_code, force_secondary)
        self.TABLE_CLASS = nav.faBuffer(company_nav_code)

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1,
                                            node_type="list")
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list
