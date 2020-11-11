#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import validator
from src.dms.setup import Setup
from .base import DMSBase
from src.models import nav


class CustVend(DMSBase):
    TABLE_CLASS = None
    # 数据一级节点名
    BIZ_NODE_LV1 = "CustVendInfo"
    WS_METHOD = "HandleCVInfoWithEntryNo"

    def __init__(self, company_nav_code, force_secondary=False, check_repeat=True):
        super(__class__, self).__init__(company_nav_code, force_secondary, check_repeat)
        # 根据公司名动态获得nav表名
        self.TABLE_CLASS = nav.custVendBuffer(company_nav_code)

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1, node_type="list")
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list

    # 校验节点内容长度
    def _is_valid(self, data_dict) -> (bool, dict):
        res_bool = True
        res_keys = {}
        data_list = data_dict["Transaction"][self.BIZ_NODE_LV1]
        if type(data_list) != list:
            data_list = [data_list]
        i = 0
        for line in data_list:
            for k, v in line.items():
                is_valid = validator.CustVendInfoValidator.check_chn_length(k, v)
                if not is_valid:
                    res_bool = False
                    res_keys["%s.%s" % (self.BIZ_NODE_LV1, k)] = validator.CustVendInfoValidator.expect_length(k)
            i += 1
        return res_bool, res_keys

    # 校验数据完整性（子类实现）
    def _is_integrity(self, data_dict, company_code, api_code) -> (bool, list):
        res_bool = True
        res_keys = []
        custVend_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type=self.BIZ_NODE_LV1)
        data_list = data_dict["Transaction"][self.BIZ_NODE_LV1]
        if type(data_list) != list:
            data_list = [data_list]
        i = 0
        for node in custVend_node_dict:
            for one_node in data_list:
                if node not in one_node.keys():
                    res_bool = False
                    miss_key = "%s.%s" % (self.BIZ_NODE_LV1, node)
                    if miss_key not in res_keys:
                        res_keys.append(miss_key)
            i += 1
        return res_bool, res_keys
