#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime


# 将iso标准格式时间字符串（含时区）转换成当前iso标准时间字符串
from sqlalchemy import collate, VARCHAR, cast
from sqlalchemy.dialects.mssql import VARBINARY


def to_local_time(dt_str):
    # 时间字符串是否以Z结尾
    if dt_str.endswith("Z"):
        dt_str = dt_str[:dt_str.index("Z")]
        dt = datetime.datetime.fromisoformat(dt_str) + datetime.timedelta(hours=8)
    else:
        dt = datetime.datetime.fromisoformat(dt_str)
    if dt.tzinfo:
        dt = dt.astimezone()
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


# 将字符串true或false转成1或0
def true_or_false_to_tinyint(bool_str):
    if bool_str.lower() == 'true':
        return 1
    elif bool_str.lower() == 'false':
        return 0
    else:
        return -1


# 用cast函数进行中文的编码和解码
def cast_chinese_encode(some_str):
    exp = collate(some_str.encode("utf-8").decode("gbk"), "Chinese_PRC_CI_AS")
    # exp = collate(some_str.encode("mbcs").decode("mbcs"), "Chinese_PRC_CI_AS")
    exp = cast(exp, VARCHAR(250))
    exp = cast(exp, VARBINARY())
    return exp
    # return collate(some_str, "Chinese_PRC_CI_AS").cast(VARCHAR(250)).cast(VARBINARY())


def cast_chinese_decode(some_str):
    return cast(some_str, VARBINARY()).cast(VARCHAR(250)).collate("Chinese_PRC_CI_AS")


if __name__ == '__main__':
    print(cast_chinese_encode("测试"))
    print(cast_chinese_decode("t2"))
