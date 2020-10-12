import pytest
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.dms.setup import Setup
from src.dms.custVend import CustVend
from src.models import nav
from src.error import DataFieldEmptyError

company_code = "K302ZH"
api_code = "CustVendInfo"
global_vars = {}
cv_obj = CustVend(force_secondary=True)


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    print("test_1_dms_source")
    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None
    assert api_setup.API_Address1 != ""
    print(api_setup)
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
    cv_obj.save_data_to_nav(custVend_dict, entry_no=entry_no, TABLE_CLASS=nav.CustVendBuffer)


# 检查数据正确性
def test_5_valid_data(init_app):
    app, db = init_app
    entry_no = global_vars["entry_no"]
    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    custVendList = db.session.query(nav.CustVendBuffer).filter(nav.CustVendBuffer.Entry_No_ == entry_no).all()

    # 检查数据正确性
    assert interfaceInfo.DMSCode == "7000320"
    assert interfaceInfo.Customer_Vendor_Total_Count == 2
    assert len(custVendList) > 0
    assert custVendList[0].No_ == "835194"
    assert custVendList[0].Type == 0
    assert custVendList[1].No_ == "V00000002"
    assert custVendList[1].Type == 1


# 将entry_no作为参数写入指定的ws
@pytest.mark.skip("先跑通app上下文")
def test_6_invoke_ws(init_app):
    cv_obj.call_web_service()


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

