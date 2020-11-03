#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
# 将iso标准格式时间字符串（含时区）转换成当前iso标准时间字符串
from sqlalchemy import collate, VARCHAR, cast, func, literal_column
from sqlalchemy.dialects.mssql import VARBINARY


# 去掉时间字符串日期与时间中间的T后面可能带的空格，只取到秒
def to_local_time(dt_str):
    if dt_str.find("T ") != -1:
        dt_str = dt_str.replace("T ", "T")
    # # YYYY-mm-ddTHH:MM:SS
    dt_str = dt_str[:19]
    dt = datetime.datetime.fromisoformat(dt_str)
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
    exp = collate(some_str, "Chinese_PRC_CI_AS")
    exp = func.convert(literal_column('VARCHAR(500)'), exp)
    exp = cast(exp, VARBINARY())
    return exp


def cast_chinese_decode(some_str):
    return cast(some_str, VARBINARY()).cast(VARCHAR(250)).collate("Chinese_PRC_CI_AS")


# 拼接数据库连接字符串
def splice_db_connect_string(db_engine, db_user, db_pwd, db_host, db_port, db_name, db_suffix):
    return "{0}://{1}:{2}@{3}:{4}/{5}?{6}".format(db_engine, db_user, db_pwd, db_host, db_port, db_name, db_suffix)


if __name__ == '__main__':
    print(cast_chinese_encode("测试"))
    print(cast_chinese_decode("t2"))
