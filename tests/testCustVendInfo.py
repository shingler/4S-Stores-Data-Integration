import os
import pytest
from src import Company
from src.dms.setup import Setup
from src.dms.custVend import CustVend
from src.models import navdb
from src.dms.base import WebServiceHandler

company_code = "K302ZH"
api_code = "CustVendInfo"
check_repeat = False
global_vars = {}
cv_obj = None
nav = None


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    assert company_info.NAV_Company_Code != ""
    global_vars["company_info"] = company_info
    globals()["cv_obj"] = CustVend(company_code, api_code, check_repeat=check_repeat)

    # 连接nav库
    globals()["nav"] = navdb.NavDB(db_host=company_info.NAV_DB_Address, db_user=company_info.NAV_DB_UserID,
                                   db_password=company_info.NAV_DB_Password, db_name=company_info.NAV_DB_Name,
                                   company_nav_code=company_info.NAV_Company_Code)
    globals()["nav"].prepare()

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
    # custVend节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    assert node_dict is not None
    general_node_dict = node_dict["General"]
    assert len(general_node_dict) > 0
    assert "DMSCode" in general_node_dict

    data = global_vars["data"]
    general_dict = cv_obj.splice_general_info(data, node_dict=general_node_dict)
    assert len(general_dict) > 0
    assert "DMSCode" in general_dict

    count = cv_obj.get_count_from_data(data["Transaction"], "CustVendInfo")
    global_vars["count"] = count
    entry_no = nav.insertGeneral(api_p_out=general_node_dict, data_dict=general_dict,
                                 Type=nav.DATA_TYPE_CV, Count=count, XMLFile=global_vars["path"])
    assert entry_no != 0

    global_vars["entry_no"] = entry_no


# 根据API_P_Out写入CustVendInfo库
# @pytest.mark.skip("先跑通app上下文")
def test_4_save_custVendInfo(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]

    # custVend节点配置
    node_dict = Setup.load_api_p_out(company_code, api_code)
    assert node_dict is not None
    assert cv_obj.BIZ_NODE_LV1 in node_dict
    custVend_node_dict = node_dict[cv_obj.BIZ_NODE_LV1]

    # 拼接custVend数据
    custVend_dict = cv_obj.splice_data_info(data, node_dict=custVend_node_dict)
    assert len(custVend_dict) == global_vars["count"]
    if global_vars["count"] > 0:
        assert "No" in custVend_dict[0]
        nav.insertCV(api_p_out=custVend_node_dict, data_dict=custVend_dict, entry_no=entry_no)
        # 读取文件，文件归档
    # 环境不同，归档路径不同
    api_setup = global_vars["api_setup"]
    if api_setup.API_Type == cv_obj.TYPE_FILE and api_setup.Archived_Path != "":
        app, db = init_app
        if app.config["ENV"] == "Development":
            global_vars["api_setup"].Archived_Path = "/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        cv_obj.archive_xml(global_vars["path"], global_vars["api_setup"].Archived_Path)
        assert os.path.exists(global_vars["path"]) == False
        assert os.path.exists(global_vars["api_setup"].Archived_Path) == True


# 检查数据正确性
# @pytest.mark.skip("数据导入前校验测试")
def test_5_valid_data(init_app):
    entry_no = global_vars["entry_no"]

    interfaceInfo = nav.getNavDataByEntryNo(entry_no, table_name="DMSInterfaceInfo", return_list=False)
    custVendList = nav.getNavDataByEntryNo(entry_no, table_name="CustVendBuffer", return_list=True)

    # 检查数据正确性
    assert interfaceInfo is not None
    assert custVendList is not None
    assert interfaceInfo["Customer_Vendor Total Count"] == global_vars["count"]
    assert len(custVendList) == global_vars["count"]


# 将entry_no作为参数写入指定的ws
# @pytest.mark.skip("先跑通app上下文")
def test_6_invoke_ws(init_app):
    entry_no = global_vars["entry_no"]
    company_info = cv_obj.get_company(company_code)
    assert company_info is not None
    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None

    wsh = WebServiceHandler(api_setup, soap_username=company_info.NAV_WEB_UserID,
                            soap_password=company_info.NAV_WEB_Password)
    ws_url = wsh.soapAddress(company_info.NAV_Company_Code)
    ws_env = WebServiceHandler.soapEnvelope(entry_no=entry_no, command_code=api_setup.CallBack_Command_Code)
    result = wsh.call_web_service(ws_url, ws_env, direction=cv_obj.DIRECT_NAV,
                                  soap_action=api_setup.CallBack_SoapAction)
    assert result == True


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
