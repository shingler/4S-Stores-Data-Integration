#!/usr/bin/python
# -*- coding:utf-8 -*-
# 操作日志的类
import datetime
import json

from src import APILog, db
from src.dms.setup import ParamConvert


class Logger:
    api_log = None

    def __init__(self, api_log):
        self.api_log = api_log

    @staticmethod
    def add_new_api_log(apiSetup, direction=1, p_in=None, userID=None):
        api_log = APILog(
            Company_Code=apiSetup.Company_Code,
            API_Code=apiSetup.API_Code,
            API_Direction=direction,
            API_P_In=json.dumps(p_in, ensure_ascii=False) if p_in is not None and len(p_in) > 0 else "",
            API_Content="",
            Content_Type=apiSetup.Data_Format,
            Status=1,
            Executed_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Finished_DT="",
            Error_Message="",
            Executed_By=1 if userID is None else 2,
            UserID="System" if userID is None else userID
        )
        db.session.add(api_log)
        db.session.commit()
        db.session.flush()
        me = __class__(api_log)
        return me

    # 读取接口/文件成功后，通过主键更新日志
    def update_api_log_when_finish(self, status, data=None, p_in=None, error_msg=""):
        pk = self.api_log.ID
        update_dict = {
            "Status": status,
            "API_Content": data,
            "Finished_DT": datetime.datetime.now().isoformat(timespec="milliseconds"),
            "Error_Message": error_msg
        }
        if p_in is not None and len(p_in) > 0:
            update_dict["API_P_In"] = json.dumps(p_in, ensure_ascii=False)
        db.session.query(APILog).filter(APILog.ID == pk).update(update_dict)

