from sco_request_sdk.utils.parameter_helper import get_iso_8061_date, get_uuid4
from sco_request_sdk.sdk_exception.exceptions import VerifyError

from urllib import parse as url_parse


class SignObjectBase:
    pass


class SignObject(SignObjectBase):
    VERSION = "v1"
    METHOD_ARGS_SEPARATOR = "%2F"
    FIELD = (
        'DealerGroupCode',
        'DealerEntityCode',
        'AccessKeySecret',
        'Action',
        'SignatureMethod',
        'Format',
        'Data'
    )

    def __init__(self, **kwargs):
        # 集团经销商编号
        self.dealer_group_code = kwargs.get('DealerGroupCode')
        # 店号
        self.dealer_entity_code = kwargs.get('DealerEntityCode')
        # 私钥
        self.access_key_secret = kwargs.pop('AccessKeySecret')
        # 接口编号
        self.action = kwargs.get('Action')
        # 加密方式
        self.signature_method = kwargs.get('SignatureMethod')
        # 数据返回格式
        self.format = kwargs.get('Format')
        # 请求data JSON串
        self.data = kwargs.get('Data')

        self.__dict = kwargs

    @classmethod
    def verify(cls, o):
        keys = o.keys()
        error = None
        for k in cls.FIELD:
            if k not in keys:
                error = '需要字段 %s' % k

        if error is not None:
            raise VerifyError(error)
        return True

    def get_dict(self):
        return self.__dict

    def get_sign_dict(self):
        sign_dict = {
            'Version': self.VERSION,
            'Timestamp': get_iso_8061_date(),
            'SignatureNonce': get_uuid4()
        }

        sign_dict.update(**self.__dict)

        return sign_dict

    def get_sign_str(self, sign_dict, method='GET'):
        url_args = url_parse.quote(url_parse.urlencode(sign_dict, quote_via=url_parse.quote))
        return '&'.join([method, self.METHOD_ARGS_SEPARATOR, url_args])

