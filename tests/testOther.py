import pytest
import requests

from src.dms.other import Other
from src.models import nav
from src.dms.setup import Setup

company_code = "K302ZH"
api_code = "Other-xml-correct"
global_vars = {}
other_obj = Other(force_secondary=False)


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
    path, data = other_obj.load_data(api_setup)
    assert path != ""
    assert data is not None
    assert len(data) > 0
    global_vars["data"] = data
    global_vars["path"] = path


# 写入interfaceinfo获得entry_no
# @pytest.mark.skip("先跑通app上下文")
def test_3_save_interface(init_app):
    general_node_dict = other_obj.load_api_p_out_nodes(company_code, api_code, node_type="General")
    assert len(general_node_dict) > 0
    assert "DMSCode" in general_node_dict

    data = global_vars["data"]
    general_dict = other_obj.splice_general_info(data, node_dict=general_node_dict)
    assert len(general_dict) > 0
    assert "DMSCode" in general_dict

    entry_no = other_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=3,
        Count=other_obj.get_count_from_data(data["Transaction"], "Daydook"),
        XMLFile=global_vars["path"] if global_vars["path"] else "")
    assert entry_no != 0

    global_vars["entry_no"] = entry_no


# 根据API_P_Out写入Other库
# @pytest.mark.skip("先跑通app上下文")
def test_4_save_Other(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]

    # FA节点配置
    other_node_dict = other_obj.load_api_p_out_nodes(company_code, api_code, node_type="Daydook")
    # 拼接fa数据
    other_dict = other_obj.splice_data_info(data, node_dict=other_node_dict)
    assert len(other_dict) > 0
    assert "DaydookNo" in other_dict[0]
    assert "SourceNo" in other_dict[0]
    # with pytest.raises():
    other_obj.save_data_to_nav(nav_data=other_dict, entry_no=entry_no, TABLE_CLASS=nav.OtherBuffer)


# 检查数据正确性
# @pytest.mark.skip(reason="调通了上一步再说")
def test_5_valid_data(init_app):
    app, db = init_app
    entry_no = global_vars["entry_no"]
    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    lineList = db.session.query(nav.OtherBuffer).filter(nav.OtherBuffer.Entry_No_ == entry_no).all()

    # 检查数据正确性
    assert interfaceInfo.DMSCode == "7000320"
    assert interfaceInfo.Other_Transaction_Total_Count == 1
    assert len(lineList) > 0
    assert lineList[0].DocumentNo_ == "XXXXX"
    assert lineList[0].SourceNo == "C0000001"
    assert lineList[1].SourceNo == "BNK_320_11_00003"


# 将entry_no作为参数写入指定的ws
@pytest.mark.skip("等刘总提供ws再测试")
def test_6_invoke_ws(init_app):
    other_obj.call_web_service()


# 清理测试数据
@pytest.mark.skip(reason="都调通再说")
def test_7_cleanup(init_app):
    (app, db) = init_app
    entry_no = global_vars["entry_no"]

    print("清理entry_no=%d的数据..." % entry_no)

    cust_list = db.session.query(nav.OtherBuffer).filter(nav.OtherBuffer.Entry_No_ == entry_no).all()
    for cust in cust_list:
        db.session.delete(cust)
    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    db.session.delete(interfaceInfo)

    db.session.commit()

