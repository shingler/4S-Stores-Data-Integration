#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import db
from src.dms.base import DMSBase
from src.models import nav


class FA(DMSBase):
    # 从api_p_out获取数据
    def splice_data_info(self, data, node_dict):
        data_dict_list = self._splice_field(data, node_dict, node_lv0="Transaction", node_lv1="FA",
                                            node_type="list")
        if type(data_dict_list) == "dict":
            data_dict_list = [data_dict_list]
        return data_dict_list

    # 根据API_P_Out写入nav表
    def save_data_to_nav(self, nav_data, entry_no):
        if type(nav_data) == "dict":
            custVend_data = [nav_data]

        for row in nav_data:
            fa_obj = nav.FABuffer(Entry_No_=entry_no)
            fa_obj.Record_ID = fa_obj.getLatestRecordId()
            for key, value in row.items():
                # 自动赋值
                fa_obj.__setattr__(key, value)
            # print(custVend_obj)
            db.session.add(fa_obj)
        db.session.commit()

    # 将entry_no作为参数写入指定的ws
    def call_web_service(self):
        pass
