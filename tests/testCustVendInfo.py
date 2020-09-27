import pytest
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


from src.dms.custVend import CustVend
from src.error import DataFieldEmptyError

global_vars = {}
cv_obj = CustVend()


@pytest.fixture(scope="module")
def create_app():
    app = Flask(__name__)
    app.config.from_object("settings.Development")
    db = SQLAlchemy()
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()

    return app


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    print("test_1_dms_source")

    company_code = "K302ZH"
    api_code = "CustVendInfo"
    api_setup = cv_obj.load_config_from_api_setup(company_code, api_code)
    assert api_setup is not None
    assert api_setup.API_Address1 != ""
    print(api_setup)
    global_vars["api_setup"] = api_setup


# 读取接口或xml
# @pytest.mark.skip("先跑通app上下文")
def test_2_load_from_dms():
    api_setup = global_vars["api_setup"]
    if api_setup.API_Type == 1:
        data = cv_obj.load_data_from_dms_interface()
    else:
        # with not pytest.raises(DataFieldEmptyError):
        xml_src_path = cv_obj.splice_xml_file_path(api_setup)
        assert xml_src_path != ""
        global_vars["xml_src_path"] = xml_src_path
        data = cv_obj.load_data_from_xml(xml_src_path)
    assert data is not None
    assert len(data) > 0
    global_vars["data"] = data


# 写入interfaceinfo获得entry_no
@pytest.mark.skip("先跑通app上下文")
def test_3_save_interface():
    data = global_vars["data"]
    entry_no = cv_obj.save_data_to_interfaceinfo(
        DMSCode=data["Transaction"]["General"]["DMSCode"],
        DMSTitle=data["Transaction"]["General"]["DMSTitle"],
        CompanyCode=data["Transaction"]["General"]["CompanyCode"],
        CompanyTitle=data["Transaction"]["General"]["CompanyTitle"],
        CreateDateTime=data["Transaction"]["General"]["CreateDateTime"],
        Creator=data["Transaction"]["General"]["Creator"],
        Type=0,
        Count=len(data["Transaction"]["CustVendInfo"]),
        XMLFile=global_vars["xml_src_path"] if global_vars["xml_src_path"] else "")
    assert entry_no != 0
    global_vars["entry_no"] = entry_no


# 根据API_P_Out写入CustVendInfo库
@pytest.mark.skip("先跑通app上下文")
def test_4_save_custVendInfo():
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]
    # with pytest.raises():
    cv_obj.save_data_to_custVendInfo()


# 将entry_no作为参数写入指定的ws
@pytest.mark.skip("先跑通app上下文")
def test_5_invoke_ws():
    cv_obj.call_web_service()
