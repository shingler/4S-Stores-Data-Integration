#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用于测试给NAV用的接口
import datetime
import os

import pytest
import requests
import json
from sqlalchemy import and_

from src import ApiSetup


# 先确定服务有没有开
def test_server_is_run():
    url = "http://127.0.0.1:5000"
    res = requests.get(url)
    assert res.status_code == 200


@pytest.mark.skip("先跑通别的")
def test_custvend(init_app):
    url = "http://127.0.0.1:5000/cust_vend"
    param_correct = {
        "company_code": "K302ZH",
        "api_code": "CustVendInfo-xml-correct",
        "api_type": 2,
        "options": '{"file_path":"/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/20201028_CustVendInfo.XML"}'
    }

    # company_code或api_code不能为空检查
    param1 = {}
    res1 = requests.post(url, data=param1)
    result1 = res1.json()
    assert result1["status"] == 0

    # api_type为空检查
    param2 = {"company_code": "K302ZH", "api_code": "CustVendInfo-xml-correct"}
    res2 = requests.post(url, data=param2).json()
    assert res2["status"] == 10005

    # api_type不正确检查
    param3 = {"company_code": "K302ZH", "api_code": "CustVendInfo-xml-correct", "api_type": 4}
    res3 = requests.post(url, data=param3).json()
    assert res3["status"] == 10005

    # api_type=2,不提供file_path则默认解析当天的xml
    param4 = {"company_code": "K302ZH", "api_code": "CustVendInfo-xml-correct", "api_type": 2}
    # 获取文件路径，检查文件是否存在
    app, db = init_app
    api_setup = db.session.query(ApiSetup).filter(
        and_(ApiSetup.Company_Code == param4["company_code"], ApiSetup.API_Code == param4["api_code"])).first()
    curdate = datetime.datetime.now().strftime("%Y%m%d")
    file_name = api_setup.File_Name_Format.replace("YYYYMMDD", curdate)
    file_path = "%s/%s" % (api_setup.API_Address1, file_name)
    file_exist = os.path.exists(file_path)
    # print(file_path)
    res4 = requests.post(url, data=param4).json()
    # print(res4)
    if file_exist:
        # 文件存在，解析正常
        print("文件存在，解析正常")
        assert res4["status"] == 1
    else:
        # 文件不存在
        print("文件不存在")
        assert res4["status"] == 10003

    # api_type=2，提供了错误的file_path
    param_path = "D:/xxx/20201026_CustVendInfo.XML"
    param5 = {
        "company_code": "K302ZH",
        "api_code": "CustVendInfo-xml-correct",
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == False
    res5 = requests.post(url, data=param5).json()
    assert res5["status"] == 10003

    # api_type=2，提供了正确的file_path
    param_path = "/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/demo_CustVendInfo.XML"
    param6 = {
        "company_code": "K302ZH",
        "api_code": "CustVendInfo-xml-correct",
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == True
    res6 = requests.post(url, data=param6).json()
    assert res6["status"] == 1


@pytest.mark.skip("先跑通上一个")
def test_fa(init_app):
    url = "http://127.0.0.1:5000/fa"
    param_correct = {
        "company_code": "K302ZH",
        "api_code": "FA-xml-correct",
        "api_type": 2,
        "options": '{"file_path":"/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/20201028_FA.XML"}'
    }

    # company_code或api_code不能为空检查
    param1 = {}
    res1 = requests.post(url, data=param1)
    result1 = res1.json()
    assert result1["status"] == 0

    # api_type为空检查
    param2 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"]}
    res2 = requests.post(url, data=param2).json()
    assert res2["status"] == 20005

    # api_type不正确检查
    param3 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"], "api_type": 4}
    res3 = requests.post(url, data=param3).json()
    assert res3["status"] == 20005

    # api_type=2,不提供file_path则默认解析当天的xml
    param4 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"], "api_type": 2}
    # 获取文件路径，检查文件是否存在
    app, db = init_app
    api_setup = db.session.query(ApiSetup).filter(
        and_(ApiSetup.Company_Code == param4["company_code"], ApiSetup.API_Code == param4["api_code"])).first()
    curdate = datetime.datetime.now().strftime("%Y%m%d")
    file_name = api_setup.File_Name_Format.replace("YYYYMMDD", curdate)
    file_path = "%s/%s" % (api_setup.API_Address1, file_name)
    file_exist = os.path.exists(file_path)
    # print(file_path)
    res4 = requests.post(url, data=param4).json()
    # print(res4)
    if file_exist:
        # 文件存在，解析正常
        print("文件存在，解析正常")
        assert res4["status"] == 1
    else:
        # 文件不存在
        print("文件不存在")
        assert res4["status"] == 20003

    # api_type=2，提供了错误的file_path
    param_path = "D:/xxx/20201026_xxx.XML"
    param5 = {
        "company_code": param_correct["company_code"],
        "api_code": param_correct["api_code"],
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == False
    res5 = requests.post(url, data=param5).json()
    assert res5["status"] == 20003

    # api_type=2，提供了正确的file_path
    param_path = "/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/demo_FA.XML"
    param6 = {
        "company_code": param_correct["company_code"],
        "api_code": param_correct["api_code"],
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == True
    res6 = requests.post(url, data=param6).json()
    assert res6["status"] == 1


@pytest.mark.skip("先跑通上一个")
def test_invoice(init_app):
    url = "http://127.0.0.1:5000/invoice"
    param_correct = {
        "company_code": "K302ZH",
        "api_code": "Invoice-xml-correct",
        "api_type": 2,
        "options": '{"file_path":"/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/20201028_Invoice.XML"}'
    }

    # company_code或api_code不能为空检查
    param1 = {}
    res1 = requests.post(url, data=param1)
    result1 = res1.json()
    assert result1["status"] == 0

    # api_type为空检查
    param2 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"]}
    res2 = requests.post(url, data=param2).json()
    print(res2)
    assert res2["status"] == 30005

    # api_type不正确检查
    param3 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"], "api_type": 4}
    res3 = requests.post(url, data=param3).json()
    assert res3["status"] == 30005

    # api_type=2,不提供file_path则默认解析当天的xml
    param4 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"], "api_type": 2}
    # 获取文件路径，检查文件是否存在
    app, db = init_app
    api_setup = db.session.query(ApiSetup).filter(
        and_(ApiSetup.Company_Code == param4["company_code"], ApiSetup.API_Code == param4["api_code"])).first()
    curdate = datetime.datetime.now().strftime("%Y%m%d")
    file_name = api_setup.File_Name_Format.replace("YYYYMMDD", curdate)
    file_path = "%s/%s" % (api_setup.API_Address1, file_name)
    file_exist = os.path.exists(file_path)
    # print(file_path)
    res4 = requests.post(url, data=param4).json()
    # print(res4)
    if file_exist:
        # 文件存在，解析正常
        print("文件存在，解析正常")
        assert res4["status"] == 1
    else:
        # 文件不存在
        print("文件不存在")
        assert res4["status"] == 30003

    # api_type=2，提供了错误的file_path
    param_path = "D:/xxx/20201026_xxx.XML"
    param5 = {
        "company_code": param_correct["company_code"],
        "api_code": param_correct["api_code"],
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == False
    res5 = requests.post(url, data=param5).json()
    assert res5["status"] == 30003

    # api_type=2，提供了正确的file_path
    param_path = "/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/demo_Invoice.XML"
    param6 = {
        "company_code": param_correct["company_code"],
        "api_code": param_correct["api_code"],
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == True
    res6 = requests.post(url, data=param6).json()
    assert res6["status"] == 1


# @pytest.mark.skip("先跑通上一个")
def test_other(init_app):
    url = "http://127.0.0.1:5000/other"
    param_correct = {
        "company_code": "K302ZH",
        "api_code": "Other-xml-correct",
        "api_type": 2,
        "options": '{"file_path":"/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/20201028_Other.XML"}'
    }

    # company_code或api_code不能为空检查
    param1 = {}
    res1 = requests.post(url, data=param1)
    result1 = res1.json()
    assert result1["status"] == 0

    # api_type为空检查
    param2 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"]}
    res2 = requests.post(url, data=param2).json()
    # print(res2)
    assert res2["status"] == 40005

    # api_type不正确检查
    param3 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"], "api_type": 4}
    res3 = requests.post(url, data=param3).json()
    assert res3["status"] == 40005

    # api_type=2,不提供file_path则默认解析当天的xml
    param4 = {"company_code": param_correct["company_code"], "api_code": param_correct["api_code"], "api_type": 2}
    # 获取文件路径，检查文件是否存在
    app, db = init_app
    api_setup = db.session.query(ApiSetup).filter(
        and_(ApiSetup.Company_Code == param4["company_code"], ApiSetup.API_Code == param4["api_code"])).first()
    curdate = datetime.datetime.now().strftime("%Y%m%d")
    file_name = api_setup.File_Name_Format.replace("YYYYMMDD", curdate)
    file_path = "%s/%s" % (api_setup.API_Address1, file_name)
    file_exist = os.path.exists(file_path)
    # print(file_path)
    res4 = requests.post(url, data=param4).json()
    # print(res4)
    if file_exist:
        # 文件存在，解析正常
        print("文件存在，解析正常")
        assert res4["status"] == 1
    else:
        # 文件不存在
        print("文件不存在")
        assert res4["status"] == 40003

    # api_type=2，提供了错误的file_path
    param_path = "D:/xxx/20201026_xxx.XML"
    param5 = {
        "company_code": param_correct["company_code"],
        "api_code": param_correct["api_code"],
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == False
    res5 = requests.post(url, data=param5).json()
    assert res5["status"] == 40003

    # api_type=2，提供了正确的file_path
    param_path = "/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/demo_Other.XML"
    param6 = {
        "company_code": param_correct["company_code"],
        "api_code": param_correct["api_code"],
        "api_type": 2,
        "options": json.dumps({"file_path": param_path})
    }
    assert os.path.exists(param_path) == True
    res6 = requests.post(url, data=param6).json()
    assert res6["status"] == 1
