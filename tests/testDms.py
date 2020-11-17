#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试dms的json接口
import json

import pytest
import requests
from sco_request_sdk.sign.security_util import get_signature_dict

from src.dms import interface
from src import Company
from src.dms.setup import Setup

company_code = "K302ZS"
api_code = "CustVendInfo"


def test_api_cv(init_app):
    # 读取签名配置
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    assert company_info.DMS_Company_Code is not None
    assert company_info.DMS_Group_Code is not None

    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None
    assert api_setup.Secret_Key is not None
    assert api_setup.Signature_Method is not None
    assert api_setup.Command_Code is not None

    p_in_list = Setup.load_api_p_in(company_code, api_code)
    assert type(p_in_list) == list
    assert len(p_in_list) > 0

    code, res = interface.api_dms(company_info, api_setup, p_in_list)
    assert res is not None
    print(res)


def test_ori():
    data = {"apiQueryDateBegin": '2020-11-01 00:00:00', "apiQueryDateEnd": '2020-11-02 00:00:00'}

    accessKeySecretA = "MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ=="

    ori_data = {
        "DealerGroupCode": 'G000035',
        "DealerEntityCode": '28976',
        'AccessKeySecret': accessKeySecretA,
        'Action': 'G102010000',
        'SignatureMethod': 'SHA256withRSA',
        'Format': 'json',
        'Data': json.dumps(data),
    }

    sign_dict = get_signature_dict(ori_data)

    print(json.dumps(sign_dict))
    print(type(sign_dict))
    headers = {'Content-Type': 'application/json;charset=UTF-8'}
    url="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface"
    res = requests.post(url=url, data=json.dumps(sign_dict), headers=headers)
    print(res.json())

