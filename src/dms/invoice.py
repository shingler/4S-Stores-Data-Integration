#!/usr/bin/python
# -*- coding:utf-8 -*-
from collections import OrderedDict

from src import validator, words
from src.dms.base import DMSBase
from src.dms.setup import Setup
from src.models import nav
from src.error import InvoiceEmptyError


class Invoice(DMSBase):
    TABLE_CLASS = None
    WS_METHOD = "HandleInvoiceWithEntryNo"

    # 数据一级节点
    BIZ_NODE_LV1 = ""
    # 数据一级节点
    BIZ_NODE_LV2 = ""
    # 通用字段
    _COMMON_FILED = "InvoiceType"

    # 读取出参配置配置
    def load_api_p_out_nodes(self, company_code, api_code, node_type="general", depth=3):
        node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type, depth - 1)
        if node_type == "general":
            return node_dict

        node_dict[node_type] = Setup.load_api_p_out_nodes(company_code, api_code, node_type=node_type, depth=depth)
        # print(node_dict)
        return node_dict

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field_by_name(data, node_dict)
        if type(data_dict_list) == OrderedDict:
            data_dict_list = [data_dict_list]
        return data_dict_list

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict):
        pass


class InvoiceHeader(Invoice):
    BIZ_NODE_LV1 = "Invoice"
    BIZ_NODE_LV2 = "INVHeader"
    TABLE_CLASS = None

    def __init__(self, company_name, force_secondary=False, check_repeat=True):
        super(__class__, self).__init__(company_name, force_secondary, check_repeat)
        self.TABLE_CLASS = nav.invoiceHeaderBuffer(company_name)

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1,
                                            node_type="list")
        # 多Invoice会变成列表，所以改用列表来处理
        data_list = []
        for inv in data_dict_list:
            # 获取INVHeader
            one_header = inv[self.BIZ_NODE_LV2]
            # 将InvoiceType与INVHeader合并
            one_header[self._COMMON_FILED] = inv[self._COMMON_FILED]
            # 统计发票行数量
            if type(inv[InvoiceLine.BIZ_NODE_LV2]) != list:
                inv[InvoiceLine.BIZ_NODE_LV2] = [inv[InvoiceLine.BIZ_NODE_LV2]]
            line_count = len(inv[InvoiceLine.BIZ_NODE_LV2])
            one_header["Line_Total_Count"] = line_count

            data_list.append(one_header)

        return data_list

    # 校验节点内容长度
    def _is_valid(self, data_dict) -> (bool, dict):
        res_bool = True
        res_keys = {}
        data_list = data_dict["Transaction"][InvoiceHeader.BIZ_NODE_LV1]
        if type(data_list) != list:
            data_list = [data_list]
        i = 0
        for invoice in data_list:
            # 发票头
            inv_header = invoice[InvoiceHeader.BIZ_NODE_LV2]
            for k, v in inv_header.items():
                is_valid = validator.InvoiceHeaderValidator.check_chn_length(k, v)
                if not is_valid:
                    res_bool = False
                    res_keys["%s.%s" % (InvoiceHeader.BIZ_NODE_LV2, k)] = validator.InvoiceHeaderValidator.expect_length(k)
            # 发票明细
            j = 0
            inv_line = invoice[InvoiceLine.BIZ_NODE_LV2]
            if type(inv_line) != list:
                inv_line = [inv_line]
            for line in inv_line:
                for k, v in line.items():
                    is_valid = validator.InvoiceLineValidator.check_chn_length(k, v)
                    if not is_valid:
                        res_bool = False
                        res_keys[
                            "%s.%s" % (InvoiceLine.BIZ_NODE_LV2, k)] = validator.InvoiceLineValidator.expect_length(k)
                j += 1
            i += 1
        return res_bool, res_keys

    # 校验数据完整性（子类实现）
    def _is_integrity(self, data_dict, company_code, api_code) -> (bool, dict):
        res_bool = True
        res_keys = []
        # 加载配置
        inv_header_dict = self.load_api_p_out_nodes(company_code, api_code, node_type=self.BIZ_NODE_LV2, depth=3)
        inv_line_dict = self.load_api_p_out_nodes(company_code, api_code, node_type=InvoiceLine.BIZ_NODE_LV2, depth=3)

        data_list = data_dict["Transaction"][self.BIZ_NODE_LV1]
        if type(data_list) != list:
            data_list = [data_list]
        i = 0
        for invoice in data_list:
            # 先检查发票头
            inv_header_data = invoice[InvoiceHeader.BIZ_NODE_LV2]
            # print(inv_header_dict)
            for hd in inv_header_dict[InvoiceHeader.BIZ_NODE_LV2].values():
                if hd.Level == 2:
                    continue
                if hd.P_Name not in inv_header_data:
                    res_bool = False
                    res_keys.append("%s.%s" % (self.BIZ_NODE_LV2, hd.P_Name))
            # 再检查发票行
            if res_bool:
                # print(inv_line_dict, type(inv_line_dict))
                inv_lines_data = invoice[InvoiceLine.BIZ_NODE_LV2]
                if type(inv_lines_data) != list:
                    inv_lines_data = [inv_lines_data]

                for one_line in inv_lines_data:
                    one_line_keys = one_line.keys()

                    for hd in inv_line_dict[InvoiceLine.BIZ_NODE_LV2].values():
                        if hd.Level != 3:
                            continue
                        if hd.P_Name not in one_line_keys:
                            res_bool = False
                            res_keys.append("%s.%s" % (InvoiceLine.BIZ_NODE_LV2, hd.P_Name))
        return res_bool, res_keys


class InvoiceLine(Invoice):
    BIZ_NODE_LV1 = "Invoice"
    BIZ_NODE_LV2 = "INVLine"
    TABLE_CLASS = None

    def __init__(self, company_nav_code, force_secondary=False, check_repeat=True):
        super(__class__, self).__init__(company_nav_code, force_secondary, check_repeat)
        self.TABLE_CLASS = nav.invoiceLineBuffer(company_nav_code)

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1,
                                            node_type="list")
        # print(data_dict_list)
        # 用node的方式装载出来是字典，还需要再处理成有冗余字段的列表
        data_list = []
        # 多Invoice会变成列表，所以改用列表来处理
        for inv in data_dict_list:
            # inv是一个完整的invoice节点
            # print(inv[self.BIZ_NODE_LV2])
            if type(inv[self.BIZ_NODE_LV2]) == OrderedDict:
                # 单个发票行数据对象INVLine
                one_dict = inv[self.BIZ_NODE_LV2]
                # 将InvoiceType放入INVLine
                one_dict[self._COMMON_FILED] = inv[self._COMMON_FILED]
                # 将发票号放入INVLine
                one_dict["InvoiceNo"] = inv[InvoiceHeader.BIZ_NODE_LV2]["InvoiceNo"]
                data_list.append(one_dict)
            else:
                # 数组对象
                for one in inv[self.BIZ_NODE_LV2]:
                    one_dict = {self._COMMON_FILED: inv[self._COMMON_FILED]}
                    # print(type(one))
                    for key, value in one.items():
                        one_dict[key] = value
                        # 将发票号放入INVLine
                        one_dict["InvoiceNo"] = inv[InvoiceHeader.BIZ_NODE_LV2]["InvoiceNo"]
                    data_list.append(one_dict)
        # print(data_list)

        return data_list

    # 把发票号放入明细中
    def set_invoice_no(self, nav_data, invoice_no=""):
        if not invoice_no:
            raise InvoiceEmptyError(words.DataImport.field_is_empty("invoiceNo"))
        for one in nav_data:
            one["InvoiceNo"] = invoice_no
        return nav_data

