import os
import pytest
from src import Company
from src.dms.setup import Setup
from src.dms.custVend import CustVend
from src.models import nav
from src.dms.base import WebServiceHandler

company_code = "K302ZH"
api_code = "CustVendInfo-xml-correct"
check_repeat = False
global_vars = {}
cv_obj = None


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    print("test_1_dms_source")
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    assert company_info.NAV_Company_Code != ""
    globals()["cv_obj"] = CustVend(company_info.NAV_Company_Code, check_repeat=check_repeat)

    # 修改bind
    conn_str = company_info.get_nav_connection_string(app.config)
    assert conn_str.startswith(app.config["DATABASE_ENGINE"])
    app.config["SQLALCHEMY_BINDS"]["%s-nav" % company_info.NAV_Company_Code] = conn_str

    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None
    assert api_setup.API_Address1 != ""
    global_vars["api_setup"] = api_setup


# 读取接口或xml
# @pytest.mark.skip("先跑通app上下文")
def test_2_load_from_dms(init_app):
    api_setup = global_vars["api_setup"]
    path, data = cv_obj.load_data(api_setup)
    assert path != ""
    assert data is not None
    assert len(data) > 0
    global_vars["path"] = path
    global_vars["data"] = data


# 写入interfaceinfo获得entry_no
# @pytest.mark.skip("先跑通app上下文")
def test_3_save_interface(init_app):
    general_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="General")
    assert len(general_node_dict) > 0
    assert "DMSCode" in general_node_dict

    data = global_vars["data"]
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)
    assert len(general_dict) > 0
    assert "DMSCode" in general_dict

    entry_no = cv_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=0,
        Count=cv_obj.get_count_from_data(data["Transaction"], "CustVendInfo"),
        XMLFile=global_vars["path"] if global_vars["path"] else "")
    assert entry_no != 0

    global_vars["entry_no"] = entry_no


# 根据API_P_Out写入CustVendInfo库
# @pytest.mark.skip("先跑通app上下文")
def test_4_save_custVendInfo(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]

    # custVend节点配置
    custVend_node_dict = Setup.load_api_p_out_nodes(company_code, api_code, node_type="CustVendInfo")
    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)
    assert len(custVend_dict) > 0
    assert "No" in custVend_dict[0]
    cv_obj.save_data_to_nav(custVend_dict, entry_no=entry_no, TABLE_CLASS=cv_obj.TABLE_CLASS)
    # 读取文件，文件归档
    # 环境不同，归档路径不同
    app, db = init_app
    if app.config["ENV"] == "Development":
        global_vars["api_setup"].Archived_Path = "/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
    cv_obj.archive_xml(global_vars["path"], global_vars["api_setup"].Archived_Path)
    assert os.path.exists(global_vars["path"]) == False
    assert os.path.exists(global_vars["api_setup"].Archived_Path) == True


# 检查数据正确性
def test_5_valid_data(init_app):
    app, db = init_app
    entry_no = global_vars["entry_no"]

    interfaceInfoClass = cv_obj.GENERAL_CLASS
    interfaceInfo = db.session.query(interfaceInfoClass).filter(interfaceInfoClass.Entry_No_ == entry_no).first()
    custVendClass = cv_obj.TABLE_CLASS
    custVendList = db.session.query(custVendClass).filter(custVendClass.Entry_No_ == entry_no).all()

    # 检查数据正确性
    assert interfaceInfo.DMSCode == "7000320"
    assert interfaceInfo.Customer_Vendor_Total_Count > 0
    assert len(custVendList) > 0
    assert custVendList[0].No_ == "835194"
    assert custVendList[0].Type == 0
    assert custVendList[1].No_ == "V00000002"
    assert custVendList[1].Type == 1


# 将entry_no作为参数写入指定的ws
# @pytest.mark.skip("先跑通app上下文")
def test_6_invoke_ws(init_app):
    entry_no = global_vars["entry_no"]
    company_info = cv_obj.get_company(company_code)
    assert company_info is not None
    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None

    # result = cv_obj.call_web_service(entry_no, api_setup=api_setup, user_id=company_info.NAV_WEB_UserID, password=company_info.NAV_WEB_Password)
    wsh = WebServiceHandler(api_setup, soap_username=company_info.NAV_WEB_UserID, soap_password=company_info.NAV_WEB_Password)
    ws_url = wsh.soapAddress(company_info.NAV_Company_Code)
    ws_env = WebServiceHandler.soapEnvelope(method_name=cv_obj.WS_METHOD, entry_no=entry_no)
    result = wsh.call_web_service(ws_url, ws_env, direction=cv_obj.DIRECT_NAV, soap_action=cv_obj.WS_ACTION)
    assert result is not None


# 清理测试数据
@pytest.mark.skip("先确定数据编码")
def test_7_cleanup(init_app):
    (app, db) = init_app
    entry_no = global_vars["entry_no"]

    print("清理entry_no=%d的数据..." % entry_no)

    cust_list = db.session.query(nav.CustVendBuffer).filter(nav.CustVendBuffer.Entry_No_ == entry_no).all()
    for cust in cust_list:
        db.session.delete(cust)
    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    db.session.delete(interfaceInfo)

    db.session.commit()

