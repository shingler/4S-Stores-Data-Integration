#!/usr/bin/python
# -*- coding:utf-8 -*-
from collections import OrderedDict

from src.dms.base import DMSBase
from src.models import nav
from src.error import InvoiceEmptyError


class Invoice(DMSBase):
    BIZ_NODE_LV1 = ""
    BIZ_NODE_LV2 = ""
    TABLE_CLASS = None

    _COMMON_FILED = "InvoiceType"

    # 读取出参配置配置
    def load_api_p_out_nodes(self, company_code, api_code, node_type="general", depth=3):
        node_dict = super().load_api_p_out_nodes(company_code, api_code, node_type, depth - 1)
        if node_type == "general":
            return node_dict

        node_dict["INVHeader"] = super().load_api_p_out_nodes(company_code, api_code, node_type=self.BIZ_NODE_LV2, depth=depth)
        # print(node_dict)
        return node_dict

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict, invoice_no=""):
        data_dict_list = self._splice_field_by_name(data, node_dict, invoice_no)
        if type(data_dict_list) == OrderedDict:
            data_dict_list = [data_dict_list]
        return data_dict_list

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict, invoice_no):
        pass

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass


class InvoiceHeader(Invoice):
    BIZ_NODE_LV1 = "Invoice"
    BIZ_NODE_LV2 = "INVHeader"
    TABLE_CLASS = nav.InvoiceHeaderBuffer

    # 根据节点名处理二级/三级层级数据（假设一个xml文件里只有1个发票抬头）
    def _splice_field_by_name(self, data, node_dict, invoice_no=""):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1,
                                            node_type="node")
        data_list = data_dict_list[self.BIZ_NODE_LV2]
        data_list[self._COMMON_FILED] = data_dict_list[self._COMMON_FILED]

        return data_list


class InvoiceLine(Invoice):
    BIZ_NODE_LV1 = "Invoice"
    BIZ_NODE_LV2 = "INVLine"
    TABLE_CLASS = nav.InvoiceLineBuffer

    # 根据节点名处理二级/三级层级数据
    def _splice_field_by_name(self, data, node_dict, invoice_no):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1=self.BIZ_NODE_LV1,
                                            node_type="node")
        # print(data_dict_list)
        # 用node的方式装载出来是字典，还需要再处理成有冗余字段的列表
        data_list = []
        if type(data_dict_list[self.BIZ_NODE_LV2]) == OrderedDict:
            # 单个数据对象
            one_dict = data_dict_list[self.BIZ_NODE_LV2]
            one_dict[self._COMMON_FILED] = data_dict_list[self._COMMON_FILED]
            data_list = [one_dict, ]
        else:
            # 数组对象
            print(data_dict_list[self.BIZ_NODE_LV2], type(data_dict_list[self.BIZ_NODE_LV2]))
            for one in data_dict_list[self.BIZ_NODE_LV2]:
                one_dict = {self._COMMON_FILED: data_dict_list[self._COMMON_FILED]}
                # print(type(one))
                for key, value in one.items():
                    one_dict[key] = value
                data_list.append(one_dict)
        # print(data_list)
        # 把发票号放入明细中
        data_list = self.set_invoice_no(data_list, invoice_no=invoice_no)
        return data_list

    # 把发票号放入明细中
    def set_invoice_no(self, nav_data, invoice_no=""):
        if not invoice_no:
            raise InvoiceEmptyError("发票号不能为空")
        for one in nav_data:
            one["InvoiceNo"] = invoice_no
        return nav_data

