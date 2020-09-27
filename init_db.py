#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime

from src import db, Company, ApiSetup, ApiPOutSetup
from src import create_app

app = create_app()
with app.app_context():
    db.create_all()
    # 测试数据
    db.session.add(Company(
        Code="K302ZH",
        Name="K302 Zhuhai JJ",
        Brand="Porsche",
        DMS_Interface_Activated=1,
        DMS_Company_Code="K302ZH",
        DMS_Company_Name="K302 Zhuhai JJ",
        DMS_Group_Code="",
        NAV_DB_Name="NAV",
        NAV_DB_Address="192.168.1.10",
        NAV_DB_UserID="NavDBUser",
        NAV_DB_Password="XXXXX",
        NAV_Company_Code="K302 Zhuhai JJ",
        NAV_Company_Name="K302 Zhuhai JJ",
        Last_Modified_DT=str(datetime.datetime.now()),
        Last_Modified_By="",
        NAV_WEB_UserID="",
        NAV_WEB_Password=""
    ))
    db.session.add(ApiSetup(
        Company_Code="K302ZH",
        API_Code="CustVendInfo",
        API_Name="Customer/Vendor Interface",
        API_Type=2,
        API_Address1="X:\DMS_Interface\K302ZH",
        API_Address2="Y:\DMS_Interface2\K302ZH",
        Command_Code="",
        Data_Format=2,
        Signature_Verision="",
        Signature_Method="",
        Signature="",
        Activated=True,
        File_Name_Format="YYYYMMDD_CustVendInfo.XML",
        Notification_Activated=True,
        CallBack_Address="http://192.168.1.5/XXXXX",
        Time_out=10,
        File_Max_Size=10,
        Last_Modified_DT=str(datetime.datetime.now()),
        Last_Modified_By="",
        Archived_Path=""
    ))
    db.session.add_all([
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=1, P_Code="Transaction",
            P_Name="Transaction", Level=0,
            Parent_Node_Name="", Value_Type=6,
            Table_Name="", Column_Name="",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=2, P_Code="General",
            P_Name="General", Level=1,
            Parent_Node_Name="Transaction", Value_Type=6,
            Table_Name="", Column_Name="",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=3, P_Code="DMSCode",
            P_Name="DMSCode", Level=2,
            Parent_Node_Name="General", Value_Type=1,
            Table_Name="DMSInterfaceInfo", Column_Name="DMSCode",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=4, P_Code="DMSTitle",
            P_Name="DMSTitle", Level=2,
            Parent_Node_Name="General", Value_Type=1,
            Table_Name="DMSInterfaceInfo", Column_Name="DMSTitle",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=5, P_Code="CompanyCode",
            P_Name="CompanyCode", Level=2,
            Parent_Node_Name="General", Value_Type=1,
            Table_Name="DMSInterfaceInfo", Column_Name="CompanyCode",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=6, P_Code="CompanyTitle",
            P_Name="CompanyTitle", Level=2,
            Parent_Node_Name="General", Value_Type=1,
            Table_Name="DMSInterfaceInfo", Column_Name="CompanyTitle",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=7, P_Code="CreateDateTime",
            P_Name="CreateDateTime", Level=2,
            Parent_Node_Name="General", Value_Type=1,
            Table_Name="DMSInterfaceInfo", Column_Name="CreateDateTime",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=8, P_Code="Creator",
            P_Name="Creator", Level=2,
            Parent_Node_Name="General", Value_Type=1,
            Table_Name="DMSInterfaceInfo", Column_Name="Creator",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=9, P_Code="CustVendInfo",
            P_Name="CustVendInfo", Level=2,
            Parent_Node_Name="Transaction", Value_Type=6,
            Table_Name="", Column_Name="",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=10, P_Code="Type",
            P_Name="Type", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Type",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=11, P_Code="No",
            P_Name="No", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="No_",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=12, P_Code="Name",
            P_Name="Name", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Name",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=13, P_Code="Address",
            P_Name="Address", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Address",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=14, P_Code="Address2",
            P_Name="Address2", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="[Address 2]",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=15, P_Code="PhoneNo",
            P_Name="PhoneNo", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="PhoneNo",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=16, P_Code="FaxNo",
            P_Name="FaxNo", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="FaxNo",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=17, P_Code="Blocked",
            P_Name="Blocked", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Blocked",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=18, P_Code="Email",
            P_Name="Email", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Email",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=19, P_Code="Postcode",
            P_Name="Postcode", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="[Post Code]",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=20, P_Code="City",
            P_Name="City", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="City",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=21, P_Code="Country",
            P_Name="Country", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Country",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=22, P_Code="Currency",
            P_Name="Currency", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Currency",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=23, P_Code="ARAPAccountNo",
            P_Name="ARAPAccountNo", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="ARAPAccountNo",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=24, P_Code="PricesIncludingVAT",
            P_Name="PricesIncludingVAT", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="PricesIncludingVAT",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=25, P_Code="ApplicationMethod",
            P_Name="ApplicationMethod", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="[Application Method]",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=26, P_Code="PaymentTermsCode",
            P_Name="PaymentTermsCode", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="PaymentTermsCode",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=27, P_Code="PaymentMethodCode",
            P_Name="PaymentMethodCode", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="PaymentMethodCode",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=28, P_Code="CostCenterCode",
            P_Name="CostCenterCode", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="[Cost Center Code]",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=29, P_Code="Template",
            P_Name="Template", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Template",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=30, P_Code="ICPartnerCode",
            P_Name="ICPartnerCode", Level=3,
            Parent_Node_Name="CustVendInfo", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="ICPartnerCode",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=31, P_Code="",
            P_Name="", Level="",
            Parent_Node_Name="", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="[Gen_ Bus_ Posting Group]",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=32, P_Code="",
            P_Name="", Level="",
            Parent_Node_Name="", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="[VAT Bus_ Posting Group]",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        ),
        ApiPOutSetup(
            Company_Code="K302ZH", API_Code="CustVendInfo",
            Sequence=33, P_Code="",
            P_Name="", Level="",
            Parent_Node_Name="", Value_Type=1,
            Table_Name="CustVendBuffer", Column_Name="Cust_VendPostingGroup",
            Last_Modified_DT=str(datetime.datetime.now()), Last_Modified_By=""
        )
    ])
    db.session.commit()
