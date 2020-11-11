#!/usr/bin/python
# -*- coding:utf-8 -*-
from collections import OrderedDict

from src import validator
from src.dms.base import DMSBase
from src.dms.setup import Setup
from src.models import nav


class Other(DMSBase):
    TABLE_CLASS = None
    WS_METHOD = "HandleOtherWithEntryNo"

    # 数据一级节点
    BIZ_NODE_LV1 = "Daydook"
    # 数据二级节点
    BIZ_NODE_LV2 = "Line"
    # 通用字段
    _COMMON_FILED = "DaydookNo"

    def __init__(self, company_nav_code, force_secondary=False, check_repeat=True):
        super(__class__, self).__init__(company_nav_code, force_secondary, check_repeat)
        self.TABLE_CLASS = nav.otherBuffer(company_nav_code)

    # 读取出参配置配置
    def load_api_p_out_nodes(self, company_code, api_code, node_type="general", depth=3):
        node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type, depth - 1)
        if node_type == "general":
            return node_dict

        node_dict[node_type] = Setup.load_api_p_out_nodes(company_code, api_code,
                                                       node_type=node_type, depth=depth)
        # print(node_dict)
        return node_dict

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict, node_lv2):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction",
                                            node_lv1=self.BIZ_NODE_LV1, node_type="list")
        # print(data_dict_list)
        data_list = []
        # 多DayDook会变成列表，所以改用列表来处理
        for day_dook in data_dict_list:
            # 用node的方式装载出来是字典，还需要再处理成有冗余字段的列表
            lines = day_dook["Line"]
            # 单节点会被解析成字典，需要转成列表
            if type(lines) != list:
                lines = [lines]
            for one in lines:
                one_dict = {self._COMMON_FILED: day_dook[self._COMMON_FILED]}
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

    # 获取指定节点的数量（xml可以节点同名。在json这里，则判断节点是否是数组。是，则返回长度；非，则返回1。
    def get_count_from_data(self, data, node_name="Daydook") -> int:
        if node_name not in data:
            return 0
        # if type(data[node_name]) == OrderedDict:
        #     return 1
        count = 0
        # other不看daydook
        if type(data[node_name]) == list:
            # daydook有多个
            for dd in data[node_name]:
                # daydook里有多行
                if type(dd["Line"]) == list:
                    count += len(dd["Line"])
                else:
                    # daydook只有一行
                    count += 1
        else:
            # 只有一个daydook
            dd = data[node_name]["Line"]
            # daydook里有多行
            if type(dd) == list:
                count += len(dd)
            else:
                # daydook只有一行
                count += 1
        return count

    # 校验节点内容长度
    def _is_valid(self, data_dict) -> (bool, dict):
        res_bool = True
        res_keys = {}

        if self.BIZ_NODE_LV1 in data_dict["Transaction"]:
            # 只有存在节点时才判断

            data_list = data_dict["Transaction"][self.BIZ_NODE_LV1]
            if type(data_list) != list:
                data_list = [data_list]
            i = 0
            for dd in data_list:
                lines = dd[self.BIZ_NODE_LV2]
                if type(lines) != list:
                    lines = [lines]
                j = 0
                for line in lines:
                    for k, v in line.items():
                        is_valid = validator.OtherValidator.check_chn_length(k, v)
                        if not is_valid:
                            res_bool = False
                            res_keys["%s.%s" % (self.BIZ_NODE_LV1, k)] = validator.OtherValidator.expect_length(k)
                    j += 1
                i += 1

        return res_bool, res_keys

    # 校验数据完整性（子类实现）
    def _is_integrity(self, data_dict, company_code, api_code) -> (bool, list):
        res_bool = True
        res_keys = []

        if self.BIZ_NODE_LV1 in data_dict["Transaction"]:
            # 只有存在节点时才判断

            # 读取2级，3级配置
            other_node_lv2_dict = self.load_api_p_out_nodes(company_code, api_code, node_type=self.BIZ_NODE_LV1, depth=2)
            other_node_lv3_dict = self.load_api_p_out_nodes(company_code, api_code, node_type=self.BIZ_NODE_LV2, depth=3)

            data_list = data_dict["Transaction"][self.BIZ_NODE_LV1]
            # 按list处理
            if type(data_list) != list:
                data_list = [data_list]

            for dd in data_list:
                # 检查2级节点

                for node in other_node_lv2_dict[self.BIZ_NODE_LV1].values():
                    if node.P_Name not in dd.keys():
                        res_bool = False
                        miss_key = "%s.%s" % (self.BIZ_NODE_LV1, node.P_Name)
                        if miss_key not in res_keys:
                            res_keys.append(miss_key)
                        return res_bool, res_keys

                # 检查3级节点
                lines = dd[self.BIZ_NODE_LV2]
                if type(lines) != list:
                    lines = [lines]
                for line in lines:
                    line_keys = line.keys()
                    for node in other_node_lv3_dict[self.BIZ_NODE_LV2].values():
                        if node.P_Name not in line_keys:
                            res_bool = False
                            miss_key = "%s.%s" % (self.BIZ_NODE_LV2, node.P_Name)
                            if miss_key not in res_keys:
                                res_keys.append(miss_key)

        return res_bool, res_keys
