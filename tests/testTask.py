import random

import pytest

import bin
from bin import cust_vend, fa, invoice, other
from src.dms.custVend import CustVend
from src.dms.notification import Notification
from src.error import DataFieldEmptyError
from src.models import nav
from src.models.dms import ApiTaskSetup
from src.models.log import NotificationLog, APILog


global_vars = {
    "retry": False, "notify": False, "entry_no": 0
}


# 从数据库随机读取一个任务
def test_1_load_task(init_app):
    app, db = init_app
    task_list = db.session.query(ApiTaskSetup).all()
    one_task = random.choice(task_list)
    # one_task = task_list[0]
    assert one_task.Company_Code != ""
    assert one_task.API_Code != ""
    assert type(one_task.Fail_Handle) == int
    print(one_task)
    global_vars["current_task"] = one_task


# 成功执行这个任务
@pytest.mark.skip("测试失败时先忽略")
def test_2_run_task_success(init_app):
    one_task = global_vars["current_task"]
    company_code = one_task.Company_Code
    api_code = one_task.API_Code
    entry_no = 0

    if one_task.API_Code == "CustVendInfo":
        entry_no = cust_vend.main(company_code=company_code, api_code=api_code, retry=True)
    elif one_task.API_Code == "FA":
        entry_no = fa.main(company_code=one_task.Company_Code, api_code=one_task.API_Code, retry=True)
    elif one_task.API_Code == "Invoice":
        entry_no = invoice.main(company_code=one_task.Company_Code, api_code=one_task.API_Code, retry=True)
    elif one_task.API_Code == "Other":
        entry_no = other.main(company_code=one_task.Company_Code, api_code=one_task.API_Code, retry=True)
    assert entry_no != 0
    print(entry_no)
    global_vars["entry_no"] = entry_no


# 让这个任务执行失败（根据失败处理，进行重试及发邮件功能的测试）
# @pytest.mark.skip("测试成功时忽略")
def test_3_run_task_fail(init_app):
    one_task = global_vars["current_task"]
    company_code = one_task.Company_Code
    api_code = one_task.API_Code
    entry_no = 0
    retry = False
    notify = False

    try:
        if one_task.API_Code == "CustVendInfo":
            entry_no = cust_vend.main(company_code=company_code, api_code=api_code)
        elif one_task.API_Code == "FA":
            entry_no = fa.main(company_code=one_task.Company_Code, api_code=one_task.API_Code)
        elif one_task.API_Code == "Invoice":
            entry_no = invoice.main(company_code=one_task.Company_Code, api_code=one_task.API_Code)
        elif one_task.API_Code == "Other":
            entry_no = other.main(company_code=one_task.Company_Code, api_code=one_task.API_Code)
        assert entry_no != 0
        print(entry_no)

    except FileNotFoundError as ex:
        # 失败处理，主要读取task里的Fail_Handle字段
        if one_task.Fail_Handle == 1:
            print("Fail Handle设置为1，不继续执行")
        elif one_task.Fail_Handle == 2:
            print("Fail Handle设置为2，将重试")
            retry = True
        elif one_task.Fail_Handle == 3:
            print("Fail Handle设置为3，将重试并发送邮件")
            retry = True
            notify = True

    global_vars["retry"] = retry
    global_vars["notify"] = notify

    assert entry_no == 0
    global_vars["entry_no"] = entry_no


# 重试
def test_4_retry_or_not(init_app):
    retry = global_vars["retry"]
    if retry:
        print("失败后重试")
        one_task = global_vars["current_task"]
        company_code = one_task.Company_Code
        api_code = one_task.API_Code
        entry_no = 0

        if one_task.API_Code == "CustVendInfo":
            entry_no = cust_vend.main(company_code=company_code, api_code=api_code, retry=retry)
        elif one_task.API_Code == "FA":
            entry_no = fa.main(company_code=company_code, api_code=api_code, retry=retry)
        elif one_task.API_Code == "Invoice":
            entry_no = invoice.main(company_code=company_code, api_code=api_code, retry=retry)
        elif one_task.API_Code == "Other":
            entry_no = other.main(company_code=company_code, api_code=api_code, retry=retry)
        assert entry_no != 0
        print(entry_no)
        global_vars["entry_no"] = entry_no
    else:
        print("失败后不重试")


# 发送提醒邮件
def test_5_send_notification(init_app):
    notify = global_vars["notify"]
    if not notify:
        print("不发送提醒邮件")
    else:
        print("发送提醒邮件")
        one_task = global_vars["current_task"]
        # 读取邮件列表
        notify_obj = Notification(one_task.Company_Code, one_task.API_Code)
        receivers = notify_obj.get_receiver_email()
        assert type(receivers) == list
        assert len(receivers) != 0
        assert receivers[0].Activated == True
        # 发送邮件
        smtp_config = notify_obj.smtp_config
        assert smtp_config is not None
        assert smtp_config.Email_SMTP is not None
        assert smtp_config.Email_SMTP != ""

        nids = []
        for r in receivers:
            if r.Activated:
                email_title, email_content = notify_obj.get_notification_content()
                assert email_content != ""
                result = notify_obj.send_mail(r.Email_Address, email_title, email_content)
                assert result
                # 写入提醒日志
                if result:
                    nid = notify_obj.save_notification_log(r.Email_Address, email_title, email_content)
                    assert nid is not None
                    nids.append(nid)
        # 验证日志有记录
        app, db = init_app
        logs = db.session.query(NotificationLog).filter(NotificationLog.ID.in_(nids)).all()
        assert len(logs) > 0
        one_log = random.choice(logs)
        assert one_log.Company_Code != ""
        assert one_log.Recipients == "shingler@gf-app.cn"


# 验证写入的数据是否符合预期
def test_6_valid_data(init_app):
    entry_no = global_vars["entry_no"]
    if entry_no == 0:
        # 执行失败用例，不用验证
        print("接口读取失败，无数据写入")
        return True

    # 验证数据
    app, db = init_app
    db.session.expire_all()
    interface_data = db.session.query(nav.InterfaceInfo).filter(nav.InterfaceInfo.Entry_No_ == entry_no).first()
    assert interface_data is not None
    assert type(interface_data.Type) == int
    print(interface_data.Type)
    # 根据type，验证对应数据
    if interface_data.Type == 0:
        data_list = db.session.query(nav.CustVendBuffer).filter(nav.CustVendBuffer.Entry_No_ == entry_no).all()
        # 检查数据正确性
        assert interface_data.DMSCode == "7000320"
        assert interface_data.Customer_Vendor_Total_Count == 2
        assert len(data_list) > 0
        assert data_list[0].No_ == "835194"
        assert data_list[0].Type == 0
        assert data_list[1].No_ == "V00000002"
        assert data_list[1].Type == 1
    elif interface_data.Type == 1:
        data_list = db.session.query(nav.FABuffer).filter(nav.FABuffer.Entry_No_ == entry_no).all()
        # 检查数据正确性
        assert interface_data.DMSCode == "28976"
        assert interface_data.FA_Total_Count == 1
        assert len(data_list) > 0
        assert data_list[0].FANo_ == "FA0001"
    elif interface_data.Type == 2:
        headerInfo = db.session.query(nav.InvoiceHeaderBuffer).filter(nav.InvoiceHeaderBuffer.Entry_No_ == entry_no).first()
        lineList = db.session.query(nav.InvoiceLineBuffer).filter(nav.InvoiceLineBuffer.Entry_No_ == entry_no).all()

        print(headerInfo)
        # 检查数据正确性
        assert interface_data.DMSCode == "7000320"
        assert interface_data.Invoice_Total_Count == 1
        assert headerInfo.InvoiceNo == "1183569670"
        assert len(lineList) > 0
        assert lineList[0].GLAccount == "6001040101"
        assert lineList[0].VIN == "WP1AB2920FLA58047"
        assert lineList[0].InvoiceNo == headerInfo.InvoiceNo
        assert lineList[1].GLAccount == "6001030104"
        assert lineList[1].VIN == "WP1AB2920FLA58047"
        assert lineList[1].InvoiceNo == headerInfo.InvoiceNo
    elif interface_data.Type == 3:
        # 检查数据正确性
        assert interface_data.DMSCode == "7000320"
        assert interface_data.Other_Transaction_Total_Count == 1
        data_list = db.session.query(nav.OtherBuffer).filter(nav.OtherBuffer.Entry_No_ == entry_no).all()
        assert len(data_list) > 0
        assert data_list[0].DocumentNo_ == "XXXXX"
        assert data_list[0].SourceNo == "C0000001"
        assert data_list[1].SourceNo == "BNK_320_11_00003"
    # 验证api日志是否写入
