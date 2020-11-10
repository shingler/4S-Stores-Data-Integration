#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用拼接sql的方式写入nav库
import datetime
import random
import threading
import time

from src import db, ApiPOutSetup
from src import to_local_time


def _getTableName(company_nav_code: str, data_name) -> str:
    return "[{0}${1}]".format(company_nav_code, data_name)


# 获取最大id然后+1
def getLatestEntryNo(table_name):
    sql = "SELECT count(*) FROM {0}".format(table_name)
    print(sql)
    max_entry_id = db.session.execute(sql).fetchone()[0]
    print(max_entry_id)
    # max_entry_id = 0
    return max_entry_id + 1 if max_entry_id is not None else 1


def writeInterfaceInfo(company_nav_code: str, data_dict: dict, api_p_out: ApiPOutSetup, Type: int = 0, Count: int = 0, XMLFile: str = "", **kwargs) -> int:
    # 需要转换中文编码的字段
    convert_chn_fields = ["DMSTitle", "CompanyTitle", "Creator"]
    # 非xml的数据
    other_data = {"Type": str(Type), "[Customer_Vendor Total Count]": "0",
                  "[FA Total Count]": "0", "[Invoice Total Count]": "0",
                  "[Other Transaction Total Count]": "0", "XMLFileName": "'%s'" % XMLFile,
                  "[DateTime Handled]": "'1753-01-01 00:00:00.000'",
                  "[Handled by]": "''", "Status": "'INIT'", "[Error Message]": "''"}
    if Type == 0:
        other_data["[Customer_Vendor Total Count]"] = str(Count)
    elif Type == 1:
        other_data["[FA Total Count]"] = str(Count)
    elif Type == 2:
        other_data["[Invoice Total Count]"] = str(Count)
    else:
        other_data["[Other Transaction Total Count]"] = str(Count)
    other_data["[DateTime Imported]"] = "'%s'" % datetime.datetime.utcnow().isoformat(timespec="seconds")
    # 对xml的数据做处理
    data_dict["CreateDateTime"] = to_local_time(data_dict["CreateDateTime"])
    # 合并数据
    data_dict = {**data_dict, **other_data}

    print(type(api_p_out))
    table_name = _getTableName(company_nav_code, "DMSInterfaceInfo")

    db.session.execute("USE Nav")

    # 获取entry_no
    # 加线程锁
    lock = threading.Lock()
    lock.acquire()
    time.sleep(0.5)
    # print("%s已上锁" % threading.current_thread().name)
    data_dict["[Entry No_]"] = getLatestEntryNo(table_name)
    lock.release()

    # 拼接sql
    sql = "INSERT INTO {0} ({1}) VALUES ({2})"
    values = []
    i = 0
    # print(fields, data_dict)
    for f in data_dict.keys():
        v = str(data_dict[f])
        if f in api_p_out:
            f = api_p_out[f].Column_Name
            # 数据处理
            if api_p_out[f].Value_Type == 1:
                v = "'{0}'".format(v)
                # 转换中文
                if f in convert_chn_fields:
                    v = "cast(cast(%s collate Chinese_PRC_CI_AS as varchar(250)) as varbinary(max))" % v
            elif api_p_out[f].Value_Type in [2, 3]:
                v = str(v)
            elif api_p_out[f].Value_Type == 5:
                v = to_local_time(v)
        values.append(v)
        if i == 0:
            table_name = _getTableName(company_nav_code, api_p_out[f].Table_Name)
        i += 1
    print(table_name)
    print(",".join(data_dict.keys()))
    print(values)
    sql = sql.format(table_name, ",".join(data_dict.keys()), ','.join(values))
    print(sql)

    return 1


def writeCV():
    pass


def writeFA():
    pass


def writeInv():
    pass


def writeOther():
    pass