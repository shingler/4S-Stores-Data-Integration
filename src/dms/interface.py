#!/usr/bin/python
# -*- coding:utf-8 -*-
# DMS json接口
import json
import requests
from sco_request_sdk.sign.security_util import get_signature_dict
from src.dms.setup import ParamConvert
from src.models import dms


class Interface:
    SIGNATURE_VERSION = "1.0"
    FORMAT = "json"
    VERSION = "v1"
    SIGNATURE_METHOD = "SHA256withRSA"

    def __init__(self, dealer_entity_code: str, dealer_group_code: str, api_setup: dms.ApiSetup):
        self.dealer_group_code = dealer_group_code
        self.dealer_entity_code = dealer_entity_code
        self.action = api_setup.Command_Code
        # self.action = "G100910000"
        self.access_key_secret = api_setup.Secret_Key
        self.signature_version = api_setup.Signature_Verision
        self.version = api_setup.API_Version
        self.signature_method = api_setup.Signature_Method

    def get_interface_params(self, data):
        return {
            'SignatureVersion': self.signature_version,
            'Action': self.action,
            'Format': self.FORMAT,
            'Version': self.version,
            'DealerGroupCode': self.dealer_group_code,
            'DealerEntityCode': self.dealer_entity_code,
            'SignatureMethod': self.signature_method,
            'Data': json.dumps(data, separators=(',', ':')),
            'AccessKeySecret': self.access_key_secret
        }


# 调用接口，请求宝马接口发送调用信息
def send_data(url, data, interface_instance: Interface) -> requests.Response:
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    # 原始请求数据
    params = interface_instance.get_interface_params(data)
    # 用于签名后的data
    # url = url.format(interface_instance.action.lower())
    sign_dict = get_signature_dict(params)
    # print(url, params)
    print("=======")
    print(sign_dict)
    return requests.post(url=url, data=json.dumps(sign_dict), headers=headers)


# DMS接口调用，同步后返回对象
def api_dms(company_info: dms.Company, api_setup: dms.ApiSetup, p_in_list: list):
    dealer_group_code = company_info.DMS_Group_Code  # 经销商集团代码
    dealer_entity_code = company_info.DMS_Company_Code  # 4S店编号

    # 创建
    interface_instance = Interface(
        dealer_entity_code=dealer_entity_code,
        dealer_group_code=dealer_group_code,
        api_setup=api_setup
    )

    data = {}
    pc = ParamConvert()
    # 对日期公式做转换
    for p in p_in_list:
        if p.Value_Type in [4, 5] and p.Value_Source == 2:
            if hasattr(pc, p.Value.upper()):
                data[p.P_Code] = pc.__getattribute__(p.Value.upper())
        else:
            data[p.P_Code] = p.Value

    url = api_setup.API_Address1.format(dealer_group_code.lower())

    resp = send_data(url, data=data, interface_instance=interface_instance).json()
    print(data, resp)
    code = resp["Code"] if "Code" in resp else resp["status"]

    # 开始取数并解析数据
    if code != '200':
        jsonresp = resp['Message']
    else:
        jsonresp = resp["Data"]
        if len(jsonresp) > 0:
            # 为兼容XML格式，增加Transaction根节点
            if "Transaction" not in jsonresp:
                jsonresp = {"Transaction": jsonresp}

    return code, jsonresp
