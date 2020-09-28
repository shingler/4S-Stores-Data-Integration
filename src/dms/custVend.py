#!/usr/bin/python
# -*- coding:utf-8 -*-
from .base import DMSBase
from src.models import nav
from src import db


class CustVend(DMSBase):

    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1="CustVendInfo", node_type="list")
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list

    # 根据API_P_Out写入CustVendInfo库
    def save_data_to_custVendInfo(self, custVend_data, entry_no):
        if type(custVend_data) == "dict":
            custVend_data = [custVend_data]

        for row in custVend_data:
            custVend_obj = nav.CustVendBuffer(Entry_No_=entry_no)
            custVend_obj.Record_ID = custVend_obj.getLatestRecordId()
            for key, value in row.items():
                if key == "Type" and value == "Customer":
                    value = 0
                elif key == "Type" and value == "Vendor":
                    value = 1
                elif key == "Type":
                    value = 2

                # 自动赋值
                custVend_obj.__setattr__(key, value)
            # print(custVend_obj)
            db.session.add(custVend_obj)
        db.session.commit()

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass
