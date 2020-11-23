from sco_request_sdk.utils.parameter_helper import ensure_string, ensure_bytes


from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

from base64 import encodebytes as b64_encode_bytes
from base64 import decodebytes as b64_decode_bytes


class SignatureBase:
    pass


class SHA256WithRSASignature(SignatureBase):
    SIGNATURE_VERSION = 1.0

    def get_sign_string(self, source, access_secret):
        key = RSA.importKey(b64_decode_bytes(ensure_bytes(access_secret)))
        h = SHA256.new(ensure_bytes(source))
        signer = PKCS1_v1_5.new(key)
        signed_bytes = signer.sign(h)
        signed_base64 = b64_encode_bytes(signed_bytes)
        signature = ensure_string(signed_base64).replace('\n', '')
        return signature

    def get_signer_name(self):
        return "SHA256withRSA"

    def get_signer_version(self):
        return "1.0"

    def get_signer_type(self):
        return "PRIVATEKEY"