#!/usr/bin/python
# -*- coding:utf-8 -*-
# 从数据库读取各种配置
import datetime

from sqlalchemy import and_

from src import db, SystemSetup
from src.models import dms


class Setup:
    # 读取api_setup
    @staticmethod
    def load_api_setup(company_code, api_code) -> dms.ApiSetup:
        api_setup = db.session.query(dms.ApiSetup).filter(dms.ApiSetup.Company_Code == company_code) \
            .filter(dms.ApiSetup.API_Code == api_code).first()
        return api_setup

    # 读取api_p_in
    @staticmethod
    def load_api_p_in(company_code, api_code) -> list:
        p_in_list = db.session.query(dms.ApiPInSetup).filter(
            and_(dms.ApiPInSetup.Company_Code == company_code, dms.ApiPInSetup.API_Code == api_code)).all()
        return p_in_list

    # 读取出参配置配置
    @staticmethod
    def load_api_p_out_nodes(company_code, api_code, node_type="General", depth=2) -> dict:
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

    # 按层级关系读取所有出参配置
    @staticmethod
    def load_api_p_out(company_code, api_code) -> dict:
        node_dict = {}
        api_p_out_config = db.session.query(dms.ApiPOutSetup) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        for one in api_p_out_config:
            # 根节点
            if one.Parent_Node_Name == '':
                one.Parent_Node_Name = "/"
            # 构造上级节点
            if one.Parent_Node_Name not in node_dict:
                node_dict[one.Parent_Node_Name] = {}

            # 按层级组装
            node_dict[one.Parent_Node_Name][one.P_Name] = one

        # print(node_dict)
        return node_dict

    # 读取字段长度配置
    @staticmethod
    def load_api_p_out_value_length(company_code, api_code, table_name):
        api_p_out_config = db.session.query(dms.ApiPOutSetup.P_Name, dms.ApiPOutSetup.Value_Length) \
            .filter(dms.ApiPOutSetup.Company_Code == company_code) \
            .filter(dms.ApiPOutSetup.API_Code == api_code) \
            .filter(dms.ApiPOutSetup.Value_Length != None) \
            .filter(dms.ApiPOutSetup.Table_Name == table_name) \
            .order_by(dms.ApiPOutSetup.Sequence.asc()).all()
        return api_p_out_config

    # 读取系统设置里对超长内容的判断
    @staticmethod
    def load_system_Value_Overlenth_Handle():
        return db.session.query(SystemSetup.Value_Overlenth_Handle).first().Value_Overlenth_Handle


# 日期公式转换
class ParamConvert:

    # CD:当天日期
    @property
    def CD(self):
        return datetime.date.today().isoformat()

    # CDT:当前日期时间
    @property
    def CDT(self):
        return datetime.datetime.today().strftime("%Y-%m-%d %H:%I:%S")

    # TDTB:当天0点
    @property
    def TDTB(self):
        return datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")

    # TDTE:当天24点
    @property
    def TDTE(self):
        return datetime.datetime.now().strftime("%Y-%m-%d 23:59:59")

    # PDTB:前一天0点
    @property
    def PDTB(self):
        last_date = datetime.datetime.now() - datetime.timedelta(1)
        return last_date.strftime("%Y-%m-%d 00:00:00")

    # PDTE:前一天24点
    @property
    def PDTE(self):
        last_date = datetime.datetime.now() - datetime.timedelta(1)
        return last_date.strftime("%Y-%m-%d 23:59:59")
