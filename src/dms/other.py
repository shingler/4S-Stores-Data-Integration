#!/usr/bin/python
# -*- coding:utf-8 -*-
from src.dms.base import DMSBase
from src import db
from src.dms.setup import Setup
from src.models import dms, nav


class Other(DMSBase):
    TABLE_CLASS = None
    WS_METHOD = "HandleOtherWithEntryNo"
    WS_ACTION = "urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI:HandleOtherWithEntryNo"

    # 数据一级节点
    BIZ_NODE_LV1 = "Daydook"
    # 数据二级节点
    BIZ_NODE_LV2 = "Line"
    # 通用字段
    _COMMON_FILED = "DaydookNo"


    def __init__(self, company_nav_code, force_secondary=False):
        super(__class__, self).__init__(company_nav_code, force_secondary)
        self.TABLE_CLASS = nav.otherBuffer(company_nav_code)

    # 读取出参配置配置
    def load_api_p_out_nodes(self, company_code, api_code, node_type="general", depth=3):
        node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type, depth-1)
        if node_type == "general":
            return node_dict

        node_dict["Line"] = Setup.load_api_p_out_nodes(company_code, api_code,
                                                         node_type=self.BIZ_NODE_LV2, depth=depth)
        # print(node_dict)
        return node_dict

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict, node_lv2):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction",
                                            node_lv1=self.BIZ_NODE_LV1, node_type="node")
        # print(data_dict_list)
        # 用node的方式装载出来是字典，还需要再处理成有冗余字段的列表
        data_list = []
        for one in data_dict_list["Line"]:
            one_dict = {self._COMMON_FILED: data_dict_list[self._COMMON_FILED]}
            for key, value in one.items():
                one_dict[key] = value
            data_list.append(one_dict)
        # print(data_list)
        return data_list

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field_by_name(data, node_dict, node_lv2=self.BIZ_NODE_LV2)
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list
