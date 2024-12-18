#!/usr/bin/python
# -*- coding:utf-8 -*-
from collections import OrderedDict

from src import words, validator
from src.dms.base import DMSBase
from src.dms.setup import Setup
from src.error import InvoiceEmptyError, NodeNotExistError
from src.validator import InvoiceHeaderValidator, InvoiceLineValidator


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
    def load_api_p_out_nodes(self, company_code, api_code, is_General=True):
        param_dict = Setup.load_api_p_out(company_code, api_code)
        if is_General:
            return param_dict["General"]
        else:
            return {
                InvoiceHeader.BIZ_NODE_LV1: param_dict[InvoiceHeader.BIZ_NODE_LV1],
                InvoiceHeader.BIZ_NODE_LV2: param_dict[InvoiceHeader.BIZ_NODE_LV2],
                InvoiceLine.BIZ_NODE_LV2: param_dict[InvoiceLine.BIZ_NODE_LV2]
            }

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

    # 从数据库读取一级二级节点
    def __init__(self, company_code, api_code, force_secondary=False, check_repeat=True):
        super().__init__(company_code, api_code, force_secondary, check_repeat)
        # 加载0级节点
        node_lv0 = Setup.load_api_p_out_nodes(company_code, api_code, "/", 0)
        if node_lv0 == {}:
            raise NodeNotExistError(words.DataImport.param_out_setup_error(company_code, api_code, "/"))
        for node in node_lv0.values():
            self.NODE_LV0 = node.P_Code

        # 加载1级节点
        node_lv1 = Setup.load_api_p_out_nodes(company_code, api_code, self.NODE_LV0, 1)
        if node_lv1 == {}:
            raise NodeNotExistError(words.DataImport.param_out_setup_error(company_code, api_code, self.NODE_LV0))
        for node in node_lv1.values():
            if node.Table_Name == "InvoiceHeaderBuffer":
                self.BIZ_NODE_LV1 = node.P_Code

        # 加载2级节点
        node_lv2 = Setup.load_api_p_out_nodes(company_code, api_code, self.BIZ_NODE_LV1, 2)
        if node_lv2 == {}:
            raise NodeNotExistError(words.DataImport.param_out_setup_error(company_code, api_code, self.BIZ_NODE_LV1))
        for node in node_lv2.values():
            if node.Table_Name == "InvoiceHeaderBuffer" and node.Value_Type == 6:
                self.BIZ_NODE_LV2 = node.P_Code
            elif node.Value_Type == 1:
                self._COMMON_FILED = node.P_Code
        # print(self.BIZ_NODE_LV1, self.BIZ_NODE_LV2)

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1,
                                            node_type="list")
        # 多Invoice会变成列表，所以改用列表来处理
        data_list = []
        for inv in data_dict_list:
            # 获取INVHeader
            one_header = {}
            # 因为多了一级，所以需要做二次数据拼接处理
            for key, value in inv[self.BIZ_NODE_LV2].items():
                if key in node_dict:
                    one_header[key] = value
            # 将InvoiceType与INVHeader合并
            one_header[self._COMMON_FILED] = inv[self._COMMON_FILED]
            # 统计发票行数量
            if type(inv[InvoiceLine.BIZ_NODE_LV2]) != list:
                inv[InvoiceLine.BIZ_NODE_LV2] = [inv[InvoiceLine.BIZ_NODE_LV2]]
            line_count = len(inv[InvoiceLine.BIZ_NODE_LV2])
            # one_header["Line_Total_Count"] = line_count
            one_header["Line Total Count"] = line_count

            data_list.append(one_header)

        return data_list

    # 校验节点内容长度
    def _is_valid(self, data_dict) -> (bool, dict):
        res_bool = True
        res_keys = {}

        if InvoiceHeader.BIZ_NODE_LV1 in data_dict["Transaction"]:
            # 只有存在节点时才判断
            data_list = data_dict["Transaction"][InvoiceHeader.BIZ_NODE_LV1]
            if type(data_list) != list:
                data_list = [data_list]
            i = 0
            header_validator = InvoiceHeaderValidator(self.company_code, self.api_code)
            line_validator = InvoiceLineValidator(self.company_code, self.api_code)
            for invoice in data_list:
                # 发票头
                inv_header = invoice[InvoiceHeader.BIZ_NODE_LV2]
                for k, v in inv_header.items():
                    is_valid = header_validator.check_chn_length(k, v)
                    if not is_valid and header_validator.overleng_handle == header_validator.OVERLENGTH_WARNING:
                        res_bool = False
                        res_keys = {
                            "key": "%s.%s" % (InvoiceHeader.BIZ_NODE_LV2, k),
                            "expect": header_validator.expect_length(k),
                            "content": v
                        }
                        return res_bool, res_keys
                    elif not is_valid and header_validator.overleng_handle == header_validator.OVERLENGTH_CUT:
                        # 按长度截断
                        inv_header[k] = v.encode("gbk")[0:header_validator.expect_length(k)].decode(
                                "gbk", "ignore")

                # 发票明细
                j = 0
                inv_line = invoice[InvoiceLine.BIZ_NODE_LV2]
                if type(inv_line) != list:
                    inv_line = [inv_line]
                for line in inv_line:
                    for k, v in line.items():
                        is_valid = line_validator.check_chn_length(k, v)
                        if not is_valid and line_validator.overleng_handle == line_validator.OVERLENGTH_WARNING:
                            res_bool = False
                            res_keys = {
                                "key": "%s.%s" % (InvoiceLine.BIZ_NODE_LV2, k),
                                "expect": line_validator.expect_length(k),
                                "content": v
                            }
                            return res_bool, res_keys
                        elif not is_valid and line_validator.overleng_handle == line_validator.OVERLENGTH_CUT:
                            # 按长度截断
                            line[k] = v.encode("gbk")[0:line_validator.expect_length(k)].decode(
                                "gbk", 'ignore')
                    j += 1
                i += 1

        return res_bool, res_keys

    # 校验数据完整性（子类实现）
    def _is_integrity(self, data_dict, company_code, api_code) -> (bool, dict):
        res_bool = True
        res_keys = []

        if self.BIZ_NODE_LV1 in data_dict["Transaction"]:
            # 只有存在节点时才判断

            # 加载配置
            inv_dict = self.load_api_p_out_nodes(company_code, api_code, is_General=False)
            inv_header_dict = inv_dict[InvoiceHeader.BIZ_NODE_LV2]
            inv_line_dict = inv_dict[InvoiceLine.BIZ_NODE_LV2]

            data_list = data_dict["Transaction"][self.BIZ_NODE_LV1]
            if type(data_list) != list:
                data_list = [data_list]
            i = 0
            for invoice in data_list:
                # 先检查发票整体结构
                for inv in inv_dict[InvoiceHeader.BIZ_NODE_LV1].values():
                    if inv.P_Name not in invoice:
                        res_bool = False
                        miss_key = "%s.%s" % (self.BIZ_NODE_LV1, inv.P_Name)
                        if miss_key not in res_keys:
                            res_keys.append(miss_key)
                        return res_bool, res_keys

                # 再检查发票头
                inv_header_data = invoice[InvoiceHeader.BIZ_NODE_LV2]
                # print(inv_header_dict)
                for hd in inv_header_dict.values():
                    if hd.Level == 2:
                        continue
                    if hd.P_Name not in inv_header_data:
                        res_bool = False
                        miss_key = "%s.%s" % (self.BIZ_NODE_LV2, hd.P_Name)
                        if miss_key not in res_keys:
                            res_keys.append(miss_key)

                # 再检查发票行
                if res_bool:
                    # print(inv_line_dict, type(inv_line_dict))
                    inv_lines_data = invoice[InvoiceLine.BIZ_NODE_LV2]
                    if type(inv_lines_data) != list:
                        inv_lines_data = [inv_lines_data]

                    for one_line in inv_lines_data:
                        one_line_keys = one_line.keys()
                        for ld in inv_line_dict.values():
                            if ld.Level != 3:
                                continue
                            if ld.P_Name not in one_line_keys:
                                res_bool = False
                                miss_key = "%s.%s" % (InvoiceLine.BIZ_NODE_LV2, ld.P_Name)
                                if miss_key not in res_keys:
                                    res_keys.append(miss_key)
                                    # 本意是都报出来。但既然只要一个，就break吧。万一以后又都要呢
                                    break

        return res_bool, res_keys


class InvoiceLine(Invoice):
    BIZ_NODE_LV1 = "Invoice"
    BIZ_NODE_LV2 = "INVLine"

    # 从数据库读取一级二级节点
    def __init__(self, company_code, api_code, force_secondary=False, check_repeat=True):
        super().__init__(company_code, api_code, force_secondary, check_repeat)
        # 加载0级节点
        node_lv0 = Setup.load_api_p_out_nodes(company_code, api_code, "/", 0)
        if node_lv0 == {}:
            raise NodeNotExistError(words.DataImport.param_out_setup_error(company_code, api_code, "/"))
        for node in node_lv0.values():
            self.NODE_LV0 = node.P_Code

        # 加载1级节点
        node_lv1 = Setup.load_api_p_out_nodes(company_code, api_code, self.NODE_LV0, 1)
        if node_lv1 == {}:
            raise NodeNotExistError(words.DataImport.param_out_setup_error(company_code, api_code, self.NODE_LV0))
        for node in node_lv1.values():
            if node.Table_Name == "InvoiceLineBuffer":
                self.BIZ_NODE_LV1 = node.P_Code

        # 加载2级节点
        node_lv2 = Setup.load_api_p_out_nodes(company_code, api_code, self.BIZ_NODE_LV1, 2)
        if node_lv2 == {}:
            raise NodeNotExistError(words.DataImport.param_out_setup_error(company_code, api_code, self.BIZ_NODE_LV1))
        for node in node_lv2.values():
            if node.Table_Name == "InvoiceLineBuffer" and node.Value_Type == 6:
                self.BIZ_NODE_LV2 = node.P_Code
            elif node.Value_Type == 1:
                self._COMMON_FILED = node.P_Code

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
                one_dict = {}
                # 因为多了一级，所以需要做二次数据过滤拼接处理
                for key, value in inv[self.BIZ_NODE_LV2].items():
                    if key in node_dict:
                        one_dict[key] = value

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
                        if key in node_dict:
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

