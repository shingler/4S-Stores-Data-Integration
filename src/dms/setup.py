#!/usr/bin/python
# -*- coding:utf-8 -*-
# 从数据库读取各种配置
from src import db
from src.models import dms


class Setup:
    # 读取api_setup
    @staticmethod
    def load_api_setup(company_code, api_code):
        api_setup = db.session.query(dms.ApiSetup).filter(dms.ApiSetup.Company_Code == company_code) \
            .filter(dms.ApiSetup.API_Code == api_code).first()
        return api_setup

    # 读取api_p_in
    def load_api_p_in(self, company_code, api_code):
        pass

    # 读取出参配置配置
    @staticmethod
    def load_api_p_out_nodes(company_code, api_code, node_type="General", depth=2):
        node_dict = {}
        api_p_out_config = db.session.query(dms.ApiPOutSetup) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .filter(dms.ApiPOutSetup.Level == depth) \
            .filter(dms.ApiPOutSetup.Parent_Node_Name == node_type) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        for one in api_p_out_config:
            if one.P_Name not in node_dict:
                node_dict[one.P_Name] = one
        # print(node_dict)
        return node_dict
