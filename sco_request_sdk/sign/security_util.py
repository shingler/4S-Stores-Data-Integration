from sco_request_sdk.sign.sign_object import SignObject
from sco_request_sdk.auth.signature import SHA256WithRSASignature

from collections import OrderedDict


def get_signature_dict(sign_data, method='GET'):
    """
    :param sign_data: 一个字典，包含了要签名的字段
    :param method: 请求方法
    :return: 签名后的字典
    """

    # 校验sign_data，判断它是否包含SignObject需要的字段
    if SignObject.verify(sign_data):

        # 获取签名对象，添加额外的签名字段
        sign_obj = SignObject(**sign_data)
        sign_dict = sign_obj.get_sign_dict()

        # 使用SHA256WithRSA签名对象
        sec_util = SHA256WithRSASignature()
        # 添加签名版本字段
        sign_dict['SignatureVersion'] = sec_util.get_signer_version()

        # 使用排序后的字段获取签名
        # from urllib import parse as url_parse
        # sign_dict['Data'] = url_parse.quote(sign_dict['Data'])
        sign_str = sign_obj.get_sign_str(
            sorted(zip(sign_dict.keys(), sign_dict.values()), key=lambda x: x[0]),
            method
        )

        signature = sec_util.get_sign_string(sign_str, sign_obj.access_key_secret)
        #添加签名字段
        sign_dict['Signature'] = signature

        return sign_dict





