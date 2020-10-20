import pytest
import requests

from src import Company
from src.dms.invoice import InvoiceHeader, InvoiceLine
from src.models import nav
from src.dms.setup import Setup

company_code = "K302ZH"
api_code = "Invoice-xml-correct"
global_vars = {}
invoiceHeader_obj = None
invoiceLine_obj = None


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    print("test_1_dms_source")
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    globals()["invoiceHeader_obj"] = InvoiceHeader(company_info.NAV_Company_Code)
    globals()["invoiceLine_obj"] = InvoiceLine(company_info.NAV_Company_Code)

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
    path, data = invoiceHeader_obj.load_data(api_setup)
    assert path != ""
    assert data is not None
    assert len(data) > 0
    global_vars["data"] = data
    global_vars["path"] = path


# 写入interfaceinfo获得entry_no
# @pytest.mark.skip("先跑通app上下文")
def test_3_save_interface(init_app):
    general_node_dict = invoiceHeader_obj.load_api_p_out_nodes(company_code, api_code, node_type="General")
    assert len(general_node_dict) > 0
    assert "DMSCode" in general_node_dict

    data = global_vars["data"]
    general_dict = invoiceHeader_obj.splice_general_info(data, node_dict=general_node_dict)
    assert len(general_dict) > 0
    assert "DMSCode" in general_dict

    entry_no = invoiceHeader_obj.save_data_to_interfaceinfo(
        general_data=general_dict,
        Type=2,
        Count=invoiceHeader_obj.get_count_from_data(data["Transaction"], "Invoice"),
        XMLFile=global_vars["path"] if global_vars["path"] else "")
    assert entry_no != 0

    global_vars["entry_no"] = entry_no


# 根据API_P_Out写入Other库
# @pytest.mark.skip("先跑通app上下文")
def test_4_save_InvoiceHeader(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]

    # 节点配置
    ih_node_dict = invoiceHeader_obj.load_api_p_out_nodes(company_code, api_code, node_type=invoiceHeader_obj.BIZ_NODE_LV1)
    # 拼接fa数据
    ih_dict = invoiceHeader_obj.splice_data_info(data, node_dict=ih_node_dict)
    assert len(ih_dict) > 0
    assert "InvoiceType" in ih_dict[0]
    assert "InvoiceNo" in ih_dict[0]
    print(invoiceHeader_obj.TABLE_CLASS)
    invoiceHeader_obj.save_data_to_nav(nav_data=ih_dict, entry_no=entry_no, TABLE_CLASS=invoiceHeader_obj.TABLE_CLASS)
    global_vars["invoice_no"] = ih_dict[0]["InvoiceNo"]


# 根据API_P_Out写入Other库
# @pytest.mark.skip("先跑通app上下文")
def test_5_save_InvoiceLine(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]
    invoice_no = global_vars["invoice_no"]

    # FA节点配置
    il_node_dict = invoiceLine_obj.load_api_p_out_nodes(company_code, api_code, node_type=invoiceLine_obj.BIZ_NODE_LV1)
    # 拼接fa数据
    il_dict = invoiceLine_obj.splice_data_info(data, node_dict=il_node_dict, invoice_no=invoice_no)
    assert len(il_dict) > 0
    assert "InvoiceType" in il_dict[0]
    assert "InvoiceNo" in il_dict[0]
    # with pytest.raises():
    invoiceLine_obj.save_data_to_nav(nav_data=il_dict, entry_no=entry_no, TABLE_CLASS=invoiceLine_obj.TABLE_CLASS)


# 检查数据正确性
# @pytest.mark.skip(reason="调通了上一步再说")
def test_6_valid_data(init_app):
    app, db = init_app
    entry_no = global_vars["entry_no"]
    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    headerInfo = db.session.query(invoiceHeader_obj.TABLE_CLASS).filter(invoiceHeader_obj.TABLE_CLASS.Entry_No_ == entry_no).first()
    lineList = db.session.query(invoiceLine_obj.TABLE_CLASS).filter(invoiceLine_obj.TABLE_CLASS.Entry_No_ == entry_no).all()

    # 检查数据正确性
    assert interfaceInfo.DMSCode == "7000320"
    assert interfaceInfo.Invoice_Total_Count == 1
    assert headerInfo.InvoiceNo == "1183569670"
    assert len(lineList) > 0
    assert lineList[0].GLAccount == "6001040101"
    assert lineList[0].VIN == "WP1AB2920FLA58047"
    assert lineList[0].InvoiceNo == headerInfo.InvoiceNo
    assert lineList[1].GLAccount == "6001030104"
    assert lineList[1].VIN == "WP1AB2920FLA58047"
    assert lineList[1].InvoiceNo == headerInfo.InvoiceNo


# 将entry_no作为参数写入指定的ws
@pytest.mark.skip("等刘总提供ws再测试")
def test_7_invoke_ws(init_app):
    invoiceHeader_obj.call_web_service()


# 清理测试数据
@pytest.mark.skip(reason="都调通再说")
def test_8_cleanup(init_app):
    (app, db) = init_app
    entry_no = global_vars["entry_no"]

    print("清理entry_no=%d的数据..." % entry_no)

    line_list = db.session.query(nav.InvoiceLineBuffer).filter(nav.InvoiceLineBuffer.Entry_No_ == entry_no).all()
    for cust in line_list:
        db.session.delete(cust)

    header_list = db.session.query(nav.InvoiceHeaderBuffer).filter(nav.InvoiceHeaderBuffer.Entry_No_ == entry_no).all()
    for one in header_list:
        db.session.delete(one)

    interfaceInfo = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    db.session.delete(interfaceInfo)

    db.session.commit()

