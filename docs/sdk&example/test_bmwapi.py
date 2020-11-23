# -*- coding: utf-8 -*-
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import logging
import json
import requests
from sco_request_sdk.sign.security_util import get_signature_dict
logger = logging.getLogger('log')

#初始化接口
ACCESS_KEY_SECRET ="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ=="
REQUEST_URL = "https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}


class Interface:
    SIGNATURE_VERSION = "1.0"
    FORMAT = "json"
    VERSION = "v1"
    SIGNATURE_METHOD = "SHA256withRSA"

    def __init__(self, dealer_entity_code , dealer_group_code, action):
        self.dealer_entity_code = dealer_entity_code
        self.dealer_group_code = dealer_group_code
        self.action = action

    def get_interface_params(self, data):
        return {
            'SignatureVersion': self.SIGNATURE_VERSION,
            'Action': self.action,
            'Format': self.FORMAT,
            'Version': self.VERSION,
            'DealerGroupCode': self.dealer_group_code,
            'DealerEntityCode': self.dealer_entity_code,
            'SignatureMethod': self.SIGNATURE_METHOD,
            'Data': json.dumps(data),
            'AccessKeySecret': ACCESS_KEY_SECRET
        }

#调用接口，请求宝马接口发送调用信息
def send_data(data, interface_instance: Interface) -> requests.Response:
    # 原始请求数据
    params = interface_instance.get_interface_params(data)
    #print(params)
    # 用于签名后的data
    url = REQUEST_URL.format(interface_instance.action.lower())
    sign_dict = get_signature_dict(params)
    return requests.post(url=url, data=json.dumps(sign_dict), headers=HEADERS)


if (__name__ == "__main__"):
    apiname = 'custvendinfo'
    dealer_group_code = 'G000035'  # 经销商集团代码
    action = 'G102010000'  # CustVendInfo接口代码
    entitycode = "28976"

    # 创建
    interface_instance = Interface(
        dealer_entity_code=entitycode,
        dealer_group_code=dealer_group_code,
        action=action
    )
    starttime = '2020-11-16 00:00:00'
    endtime = '2020-11-16 23:59:59'
    data = {"apiQueryDateBegin": starttime, "apiQueryDateEnd": endtime}
    resp = send_data(data, interface_instance)  # 调用接口
    print(resp.json())