import os
import pytest
from sqlalchemy import and_

from src import Company
from src.dms.base import WebServiceHandler
from src.dms.invoice import InvoiceHeader, InvoiceLine
from src.models import nav
from src.dms.setup import Setup

company_code = "K302ZH"
api_code = "Invoice-xml-correct"
check_repeat = False
global_vars = {}
invoiceHeader_obj = None
invoiceLine_obj = None


# 根据公司列表和接口设置确定数据源
def test_1_dms_source(init_app):
    print("test_1_dms_source")
    app, db = init_app
    company_info = db.session.query(Company).filter(Company.Code == company_code).first()
    assert company_info is not None
    globals()["invoiceHeader_obj"] = InvoiceHeader(company_info.NAV_Company_Code, check_repeat=check_repeat)
    globals()["invoiceLine_obj"] = InvoiceLine(company_info.NAV_Company_Code, check_repeat=check_repeat)

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

    count = invoiceHeader_obj.get_count_from_data(data["Transaction"], "Invoice")
    global_vars["count"] = count
    entry_no = invoiceHeader_obj.save_data_to_interfaceinfo(
        general_data=general_dict, Type=2, Count=count,
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
    assert len(ih_dict) == global_vars["count"]

    if global_vars["count"] > 0:
        assert "InvoiceType" in ih_dict[0]
        assert "InvoiceNo" in ih_dict[0]
        print(invoiceHeader_obj.TABLE_CLASS)
        invoiceHeader_obj.save_data_to_nav(nav_data=ih_dict, entry_no=entry_no, TABLE_CLASS=invoiceHeader_obj.TABLE_CLASS)
        global_vars["invoice_no"] = [ih["InvoiceNo"] for ih in ih_dict]


# 根据API_P_Out写入Other库
# @pytest.mark.skip("先跑通app上下文")
def test_5_save_InvoiceLine(init_app):
    data = global_vars["data"]
    entry_no = global_vars["entry_no"]

    # FA节点配置
    il_node_dict = invoiceLine_obj.load_api_p_out_nodes(company_code, api_code, node_type=invoiceLine_obj.BIZ_NODE_LV1)
    # 拼接fa数据
    il_dict = invoiceLine_obj.splice_data_info(data, node_dict=il_node_dict)
    if len(il_dict) > 0:
        assert "InvoiceType" in il_dict[0]
        assert "InvoiceNo" in il_dict[0]
        # with pytest.raises():
        invoiceLine_obj.save_data_to_nav(nav_data=il_dict, entry_no=entry_no, TABLE_CLASS=invoiceLine_obj.TABLE_CLASS)
    # 读取文件，文件归档
    # 环境不同，归档路径不同
    app, db = init_app
    if app.config["ENV"] == "Development":
        global_vars["api_setup"].Archived_Path = "/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
    invoiceLine_obj.archive_xml(global_vars["path"], global_vars["api_setup"].Archived_Path)
    assert os.path.exists(global_vars["path"]) == False
    assert os.path.exists(global_vars["api_setup"].Archived_Path) == True


# 检查数据正确性
# @pytest.mark.skip(reason="数据文件变更导致具体判断不适用")
def test_6_valid_data(init_app):
    app, db = init_app
    entry_no = global_vars["entry_no"]

    interfaceInfoClass = invoiceHeader_obj.GENERAL_CLASS
    interfaceInfo = db.session.query(interfaceInfoClass).filter(interfaceInfoClass.Entry_No_ == entry_no).first()
    headerList = db.session.query(invoiceHeader_obj.TABLE_CLASS).filter(invoiceHeader_obj.TABLE_CLASS.Entry_No_ == entry_no).all()

    # 检查数据正确性
    assert interfaceInfo.Invoice_Total_Count == len(headerList)

    for h in headerList:
        lineList = db.session.query(invoiceLine_obj.TABLE_CLASS).filter(
            and_(invoiceLine_obj.TABLE_CLASS.Entry_No_ == entry_no, invoiceLine_obj.TABLE_CLASS.InvoiceNo == h.InvoiceNo)).all()

        # 检查发票数据正确性
        assert h.Line_Total_Count == len(lineList)


# 将entry_no作为参数写入指定的ws
# @pytest.mark.skip("等刘总提供ws再测试")
def test_7_invoke_ws(init_app):
    entry_no = global_vars["entry_no"]
    company_info = invoiceHeader_obj.get_company(company_code)
    assert company_info is not None
    api_setup = Setup.load_api_setup(company_code, api_code)
    assert api_setup is not None

    wsh = WebServiceHandler(api_setup, soap_username=company_info.NAV_WEB_UserID,
                            soap_password=company_info.NAV_WEB_Password)
    ws_url = wsh.soapAddress(company_info.NAV_Company_Code)
    ws_env = WebServiceHandler.soapEnvelope(method_name=invoiceHeader_obj.WS_METHOD, entry_no=entry_no, command_code=api_setup.CallBack_Command_Code)
    result = wsh.call_web_service(ws_url, ws_env, direction=invoiceHeader_obj.DIRECT_NAV, soap_action=api_setup.CallBack_SoapAction)
    print(result)
    assert result is not None


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

