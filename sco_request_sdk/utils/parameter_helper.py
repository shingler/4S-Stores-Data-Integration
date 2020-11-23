import time
import uuid


TIME_ZONE = "GMT"
FORMAT_ISO_8601 = "%Y-%m-%dT%H:%M:%SZ"


def get_uuid4():
    return str(uuid.uuid4())


def get_iso_8061_date():
    return time.strftime(FORMAT_ISO_8601, time.localtime())


def ensure_bytes(s, encoding='utf-8', errors='strict'):
    if isinstance(s, str):
        return bytes(s, encoding=encoding)
    if isinstance(s, bytes):
        return s
    if isinstance(s, bytearray):
        return bytes(s)
    raise ValueError(
        "Expected str or bytes or bytearray, received %s." %
        type(s))


def ensure_string(s, encoding='utf-8', errors='strict'):
    if isinstance(s, str):
        return s
    if isinstance(s, (bytes, bytearray)):
        return str(s, encoding='utf-8')
    raise ValueError(
        "Expected str or bytes or bytearray, received %s." %
        type(s))