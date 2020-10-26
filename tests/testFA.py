import os

import pytest
import requests

import src.dms
from src import Company
from src.dms.fa import FA
from src.models import nav
from src.dms.setup import Setup

company_code = "K302ZH"
api_code = "FA-xml-correct"
global_vars = {}
fa_obj = None


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    print("test_1_dms_source")
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    # 将公司名给与全局变量fa_obj
    globals()["fa_obj"] = FA(company_info.NAV_Company_Code)

    # 修改bind
    conn_str = company_info.get_nav_connection_string(app.config)
    assert conn_str.startswith(app.config["DATABASE_ENGINE"])
    app.config["SQLALCHEMY_BINDS"][
        "%s-nav" % company_info.NAV_Company_Code] = conn_str

    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None
    assert api_setup.API_Address1 != ""
    print(api_setup)
    global_vars["api_setup"] = api_setup


# 读取接口或xml
# @pytest.mark.skip("先跑通app上下文")
def test_2_load_from_dms(init_app):
    api_setup = global_vars["api_setup"]
    path, data = fa_obj.load_data(api_setup)
    assert path != ""
    assert data is not None
    assert len(data) > 0
    global_vars["data"] = data
    global_vars["path"] = path


# 写入interfaceinfo获得entry_no
# @pytest.mark.skip("先跑通app上下文")
def test_3_save_interface(init_app):
    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    assert len(general_node_dict) > 0
    assert "DMSCode" in general_node_dict

    data = global_vars["data"]
    general_dict = fa_obj.splice_general_info(data, node_dict=general_node_dict)
    assert len(general_dict) > 0
    assert "DMSCode" in general_dict

    entry_no = fa_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=1,
        Count=fa_obj.get_count_from_data(data["Transaction"], "FA"),
        XMLFile=global_vars["path"] if global_vars["path"] else "")
    assert entry_no != 0

    global_vars["entry_no"] = entry_no


# 根据API_P_Out写入FA库
# @pytest.mark.skip("先跑通app上下文")
def test_4_save_FA(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]

    # FA节点配置
    fa_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="FA")
    # 拼接fa数据
    fa_dict = fa_obj.splice_data_info(data, node_dict=fa_node_dict)
    assert len(fa_dict) > 0
    assert "FANo" in fa_dict[0]
    fa_obj.save_data_to_nav(nav_data=fa_dict, entry_no=entry_no, TABLE_CLASS=fa_obj.TABLE_CLASS)
    # 读取文件，文件归档
    fa_obj.archive_xml(global_vars["path"], global_vars["api_setup"].Archived_Path)
    assert os.path.exists(global_vars["path"]) == False
    assert os.path.exists(global_vars["api_setup"].Archived_Path) == True


# 检查数据正确性
# @pytest.mark.skip(reason="调通了上一步再说")
def test_5_valid_data(init_app):
    app, db = init_app
    entry_no = global_vars["entry_no"]

    interfaceInfoClass = fa_obj.GENERAL_CLASS
    interfaceInfo = db.session.query(interfaceInfoClass).filter(interfaceInfoClass.Entry_No_ == entry_no).first()
    faList = db.session.query(fa_obj.TABLE_CLASS).filter(fa_obj.TABLE_CLASS.Entry_No_ == entry_no).all()

    # 检查数据正确性
    assert interfaceInfo.DMSCode == "28976"
    assert interfaceInfo.FA_Total_Count == 1
    assert len(faList) > 0
    assert faList[0].FANo_ == "FA0001"


# 将entry_no作为参数写入指定的ws
# @pytest.mark.skip("等刘总提供ws再测试")
def test_6_invoke_ws(init_app):
    entry_no = global_vars["entry_no"]
    company_info = fa_obj.get_company(company_code)
    assert company_info is not None
    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None

    # result = await cv_obj.call_web_service(entry_no, url=api_setup.CallBack_Address, user_id=company_info.NAV_WEB_UserID, password=company_info.NAV_WEB_Password)
    result = fa_obj.call_web_service(entry_no, api_setup=api_setup, user_id=company_info.NAV_WEB_UserID,
                                     password=company_info.NAV_WEB_Password)
    assert result is not None


# 清理测试数据
@pytest.mark.skip(reason="都调通再说")
def test_7_cleanup(init_app):
    (app, db) = init_app
    entry_no = global_vars["entry_no"]

    print("清理entry_no=%d的数据..." % entry_no)

    cust_list = db.session.query(nav.FABuffer).filter(nav.FABuffer.Entry_No_ == entry_no).all()
    for cust in cust_list:
        db.session.delete(cust)
    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    db.session.delete(interfaceInfo)

    db.session.commit()

