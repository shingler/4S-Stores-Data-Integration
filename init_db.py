#!/usr/bin/python
# -*- coding:utf-8 -*-
import datetime

from src import db, Company, ApiSetup, ApiPOutSetup, ApiTaskSetup, NotificationUser, SystemSetup, UserList, ApiPInSetup
from src import create_app


def test_data_for_company():
    companies = [
        Company(
            Code="K302ZH",
            Name="K302 Zhuhai JJ",
            Brand="Porsche",
            DMS_Interface_Activated=1,
            DMS_Company_Code="K302ZH",
            DMS_Company_Name="K302 Zhuhai JJ",
            DMS_Group_Code="",
            NAV_DB_Name="NAV",
            NAV_DB_Address="127.0.0.1",
            NAV_DB_UserID="sa",
            NAV_DB_Password="msSqlServer2020",
            NAV_Company_Code="K302 Zhuhai JJ",
            NAV_Company_Name="K302 Zhuhai JJ",
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            NAV_WEB_UserID="NAVWebUser",
            NAV_WEB_Password="Hytc_1qaz@WSX"
        ),
        Company(
            Code="K302ZS",
            Name="K302 Zhongshan JJ",
            Brand="BMW",
            DMS_Interface_Activated=1,
            DMS_Company_Code="K302ZS",
            DMS_Company_Name="K302 Zhongshan JJ",
            DMS_Group_Code="G000035",
            NAV_DB_Name="NAV",
            NAV_DB_Address="127.0.0.1",
            NAV_DB_UserID="sa",
            NAV_DB_Password="msSqlServer2020",
            NAV_Company_Code="K302 Zhongshan JJ",
            NAV_Company_Name="K302 Zhongshan JJ",
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            NAV_WEB_UserID="NAVWebUser",
            NAV_WEB_Password="Hytc_1qaz@WSX"
        )
    ]
    return companies


# test data for task
def test_data_for_task():
    # xml的任务（mac）
    task_xml = [
        ApiTaskSetup(
            Company_Code="K302ZH",
            Sequence=1,
            Task_Name="CustVendInfo",
            API_Code="CustVendInfo",
            Execute_Time=datetime.time.fromisoformat("11:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        ),
        ApiTaskSetup(
            Company_Code="K302ZH",
            Sequence=2,
            Task_Name="FA-xml",
            API_Code="FA-xml",
            Execute_Time=datetime.time.fromisoformat("11:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        ),
        ApiTaskSetup(
            Company_Code="K302ZH",
            Sequence=3,
            Task_Name="Invoice",
            API_Code="Invoice",
            Execute_Time=datetime.time.fromisoformat("11:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        ),
        ApiTaskSetup(
            Company_Code="K302ZH",
            Sequence=4,
            Task_Name="Other",
            API_Code="Other",
            Execute_Time=datetime.time.fromisoformat("11:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        )
    ]
    # dms api的任务
    task_api = [
        ApiTaskSetup(
            Company_Code="K302ZS",
            Sequence=1,
            Task_Name="CustVendInfo",
            API_Code="CustVendInfo",
            Execute_Time=datetime.time.fromisoformat("16:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        ),
        ApiTaskSetup(
            Company_Code="K302ZS",
            Sequence=2,
            Task_Name="FA",
            API_Code="FA",
            Execute_Time=datetime.time.fromisoformat("16:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        ),
        ApiTaskSetup(
            Company_Code="K302ZS",
            Sequence=3,
            Task_Name="Invoice",
            API_Code="Invoice",
            Execute_Time=datetime.time.fromisoformat("16:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        ),
        ApiTaskSetup(
            Company_Code="K302ZS",
            Sequence=4,
            Task_Name="Other",
            API_Code="Other",
            Execute_Time=datetime.time.fromisoformat("16:00:00.000"),
            Fail_Handle=4,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"),
            Last_Modified_By="",
            Recurrence_Day=1,
            Last_Executed_Time=""
        )
    ]

    return task_xml, task_api


# test data for api_setup
def test_data_for_setup():
    setup_for_api = [
        ApiSetup(
            Company_Code="K302ZS",
            API_Code="CustVendInfo",
            API_Name="Customer/Vendor Interface",
            API_Type=2,
            API_Address2="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            API_Address1="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            Command_Code="G102010000",
            Data_Format=1,
            Signature_Verision="1.0",
            Signature_Method="SHA256withRSA",
            Signature="",
            Secret_Key="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ==",
            Activated=True,
            File_Name_Format="",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="01",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="seconds"),
            Last_Modified_By="",
            Archived_Path=""
        ),
        ApiSetup(
            Company_Code="K302ZS",
            API_Code="FA",
            API_Name="Customer/FA Interface",
            API_Type=1,
            API_Address2="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            API_Address1="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            Command_Code="G102010001",
            Data_Format=1,
            Signature_Verision="1.0",
            Signature_Method="SHA256withRSA",
            Signature="",
            Secret_Key="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ==",
            Activated=True,
            File_Name_Format="",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="02",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path=""
        ),
        ApiSetup(
            Company_Code="K302ZS",
            API_Code="Invoice",
            API_Name="Customer/Invoice Interface",
            API_Type=1,
            API_Address2="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            API_Address1="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            Command_Code="G102010002",
            Data_Format=1,
            Signature_Verision="1.0",
            Signature_Method="SHA256withRSA",
            Signature="",
            Secret_Key="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ==",
            Activated=True,
            File_Name_Format="",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="03",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path=""
        ),
        ApiSetup(
            Company_Code="K302ZS",
            API_Code="Other",
            API_Name="Customer/Other Interface",
            API_Type=1,
            API_Address2="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            API_Address1="https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface",
            Command_Code="G102010003",
            Data_Format=1,
            Signature_Verision="1.0",
            Signature_Method="SHA256withRSA",
            Signature="",
            Secret_Key="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ==",
            Activated=True,
            File_Name_Format="",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="04",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
    ]
    setup_for_xml = [
        ApiSetup(
            Company_Code="K302ZH",
            API_Code="CustVendInfo",
            API_Name="Customer/Vendor Interface",
            API_Type=2,
            API_Address1="D:\DMS_Interface\K302ZH",
            API_Address2="/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH",
            Command_Code="",
            Data_Format=2,
            Signature_Verision="",
            Signature_Method="",
            Signature="",
            Secret_Key="",
            Activated=True,
            File_Name_Format="YYYYMMDD_CustVendInfo.XML",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="01",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="seconds"),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
        ApiSetup(
            Company_Code="K302ZH",
            API_Code="FA-xml-incorrect",
            API_Name="Customer/FA Interface",
            API_Type=2,
            API_Address1="D:\DMS_Interface\K302ZH",
            API_Address2="/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH",
            Command_Code="",
            Data_Format=2,
            Signature_Verision="",
            Signature_Method="",
            Signature="",
            Secret_Key="",
            Activated=True,
            File_Name_Format="YYYYMMDD_FA.XML",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="02",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
        ApiSetup(
            Company_Code="K302ZH",
            API_Code="Invoice-xml-incorrect",
            API_Name="Customer/Invoice Interface",
            API_Type=2,
            API_Address1="D:\DMS_Interface\K302ZH",
            API_Address2="/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH",
            Command_Code="",
            Data_Format=2,
            Signature_Verision="",
            Signature_Method="",
            Signature="",
            Secret_Key="",
            Activated=True,
            File_Name_Format="YYYYMMDD_Invoice.XML",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="03",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
        ApiSetup(
            Company_Code="K302ZH",
            API_Code="Other-xml-incorrect",
            API_Name="Customer/Other Interface",
            API_Type=2,
            API_Address1="D:\DMS_Interface\K302ZH",
            API_Address2="/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH",
            Command_Code="",
            Data_Format=2,
            Signature_Verision="",
            Signature_Method="",
            Signature="",
            Secret_Key="",
            Activated=True,
            File_Name_Format="YYYYMMDD_Other.XML",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="04",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
    ]
    setup_will_error = [
        ApiSetup(
            Company_Code="K302ZH",
            API_Code="FA-xml-error",
            API_Name="xxx",
            API_Type=1,
            API_Address2="yyy",
            API_Address1="xxx",
            Command_Code="",
            Data_Format=2,
            Signature_Verision="",
            Signature_Method="",
            Signature="",
            Secret_Key="",
            Activated=True,
            File_Name_Format="YYYYMMDD_CustVendInfo.XML",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="02",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="seconds"),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
        ApiSetup(
            Company_Code="K302ZH",
            API_Code="Other-xml-error",
            API_Name="yyy",
            API_Type=2,
            API_Address2="bbb",
            API_Address1="aaa",
            Command_Code="",
            Data_Format=2,
            Signature_Verision="",
            Signature_Method="",
            Signature="",
            Secret_Key="",
            Activated=True,
            File_Name_Format="YYYYMMDD_FA.XML",
            Notification_Activated=True,
            CallBack_Address="http://62.234.26.35:7047/DynamicsNAV/WS/%s/Codeunit/DMSWebAPI",
            CallBack_SoapAction="DMSDataInterfaceIn",
            CallBack_Command_Code="04",
            Time_out=1,
            File_Max_Size=10,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'),
            Last_Modified_By="",
            Archived_Path="/Users/shingler/PycharmProjects/platform20200916/archive/K302ZH"
        ),
    ]
    return setup_for_xml, setup_for_api, setup_will_error


# test data fro setup_p_in
def test_data_for_in_param(company_code):
    p_in = [
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="CustVendInfo",
            P_Code="queryBeginDate",
            P_Name="queryBeginDate",
            Sequence=1,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="CustVendInfo",
            P_Code="queryEndDate",
            P_Name="queryEndDate",
            Sequence=2,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="FA",
            P_Code="queryBeginDate",
            P_Name="queryBeginDate",
            Sequence=1,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="FA",
            P_Code="queryEndDate",
            P_Name="queryEndDate",
            Sequence=2,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="Invoice",
            P_Code="queryBeginDate",
            P_Name="queryBeginDate",
            Sequence=1,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="Invoice",
            P_Code="queryEndDate",
            P_Name="queryEndDate",
            Sequence=2,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="Other",
            P_Code="queryBeginDate",
            P_Name="queryBeginDate",
            Sequence=1,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        ),
        ApiPInSetup(
            Company_Code=company_code,
            API_Code="Other",
            P_Code="queryEndDate",
            P_Name="queryEndDate",
            Sequence=2,
            Value_Type=5,
            Value_Source=1,
            Value="2020-11-01 00:00:00",
            Last_Modified_DT=datetime.datetime.utcnow().isoformat(timespec="seconds"),
            Last_Modified_By=""
        )
    ]
    return p_in

# test data for setup_p_out
# format=json,xml
# version=success, retry, error
def test_data_for_out_param(company_code):
    cust_vend_p = [
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=1, P_Code="Transaction",
                P_Name="Transaction", Level=0,
                Parent_Node_Name="", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=2, P_Code="General",
                P_Name="General", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=3, P_Code="DMSCode",
                P_Name="DMSCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=4, P_Code="DMSTitle",
                P_Name="DMSTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=5, P_Code="CompanyCode",
                P_Name="CompanyCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=6, P_Code="CompanyTitle",
                P_Name="CompanyTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=7, P_Code="CreateDateTime",
                P_Name="CreateDateTime", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CreateDateTime",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=8, P_Code="Creator",
                P_Name="Creator", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="Creator",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=9, P_Code="CustVendInfo",
                P_Name="CustVendInfo", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=10, P_Code="Type",
                P_Name="Type", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Type",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=11, P_Code="No",
                P_Name="No", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="No_",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=12, P_Code="Name",
                P_Name="Name", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Name",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=13, P_Code="Address",
                P_Name="Address", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Address",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=14, P_Code="Address2",
                P_Name="Address2", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="[Address 2]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=15, P_Code="PhoneNo",
                P_Name="PhoneNo", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="PhoneNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=16, P_Code="FaxNo",
                P_Name="FaxNo", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="FaxNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=17, P_Code="Blocked",
                P_Name="Blocked", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Blocked",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=18, P_Code="Email",
                P_Name="Email", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Email",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=19, P_Code="Postcode",
                P_Name="Postcode", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="[Post Code]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=20, P_Code="City",
                P_Name="City", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="City",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=21, P_Code="Country",
                P_Name="Country", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Country",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=22, P_Code="Currency",
                P_Name="Currency", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Currency",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=23, P_Code="ARAPAccountNo",
                P_Name="ARAPAccountNo", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="ARAPAccountNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=24, P_Code="PricesIncludingVAT",
                P_Name="PricesIncludingVAT", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="PricesIncludingVAT",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=25, P_Code="ApplicationMethod",
                P_Name="ApplicationMethod", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="[Application Method]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=26, P_Code="PaymentTermsCode",
                P_Name="PaymentTermsCode", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="PaymentTermsCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=27, P_Code="PaymentMethodCode",
                P_Name="PaymentMethodCode", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="PaymentMethodCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=28, P_Code="CostCenterCode",
                P_Name="CostCenterCode", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="[Cost Center Code]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=29, P_Code="Template",
                P_Name="Template", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Template",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=30, P_Code="ICPartnerCode",
                P_Name="ICPartnerCode", Level=2,
                Parent_Node_Name="CustVendInfo", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="ICPartnerCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=31, P_Code="",
                P_Name="", Level=0,
                Parent_Node_Name="", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="[Gen_ Bus_ Posting Group]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=32, P_Code="",
                P_Name="", Level=0,
                Parent_Node_Name="", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="[VAT Bus_ Posting Group]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="CustVendInfo",
                Sequence=33, P_Code="",
                P_Name="", Level=0,
                Parent_Node_Name="", Value_Type=1,
                Table_Name="CustVendBuffer", Column_Name="Cust_VendPostingGroup",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            )
        ]
    fa_p = [
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=1, P_Code="Transaction",
                P_Name="Transaction", Level=0,
                Parent_Node_Name="", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=2, P_Code="General",
                P_Name="General", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=3, P_Code="DMSCode",
                P_Name="DMSCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=4, P_Code="DMSTitle",
                P_Name="DMSTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=5, P_Code="CompanyCode",
                P_Name="CompanyCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=6, P_Code="CompanyTitle",
                P_Name="CompanyTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=7, P_Code="CreateDateTime",
                P_Name="CreateDateTime", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CreateDateTime",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=8, P_Code="Creator",
                P_Name="Creator", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="Creator",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=9, P_Code="FA",
                P_Name="FA", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=10, P_Code="FANo",
                P_Name="FANo", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="FANo_",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=11, P_Code="Description",
                P_Name="Description", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="Description",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=12, P_Code="SerialNo",
                P_Name="SerialNo", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="SerialNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=13, P_Code="Inactive",
                P_Name="Inactive", Level=2,
                Parent_Node_Name="FA", Value_Type=2,
                Table_Name="FABuffer", Column_Name="Inactive",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=14, P_Code="Blocked",
                P_Name="Blocked", Level=2,
                Parent_Node_Name="FA", Value_Type=2,
                Table_Name="FABuffer", Column_Name="Blocked",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=16, P_Code="FAClassCode",
                P_Name="FAClassCode", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="FAClassCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=17, P_Code="FASubclassCode",
                P_Name="FASubclassCode", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="FASubclassCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=18, P_Code="FALocationCode",
                P_Name="FALocationCode", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="FALocationCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=19, P_Code="BudgetedAsset",
                P_Name="BudgetedAsset", Level=2,
                Parent_Node_Name="FA", Value_Type=2,
                Table_Name="FABuffer", Column_Name="BudgetedAsset",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=20, P_Code="VendorNo",
                P_Name="VendorNo", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="VendorNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=21, P_Code="MaintenanceVendorNo",
                P_Name="MaintenanceVendorNo", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="MaintenanceVendorNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=22, P_Code="UnderMaintenance",
                P_Name="UnderMaintenance", Level=2,
                Parent_Node_Name="FA", Value_Type=2,
                Table_Name="FABuffer", Column_Name="UnderMaintenance",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=23, P_Code="NextServiceDate",
                P_Name="NextServiceDate", Level=2,
                Parent_Node_Name="FA", Value_Type=5,
                Table_Name="FABuffer", Column_Name="NextServiceDate",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=24, P_Code="WarrantyDate",
                P_Name="WarrantyDate", Level=2,
                Parent_Node_Name="FA", Value_Type=5,
                Table_Name="FABuffer", Column_Name="WarrantyDate",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=25, P_Code="DepreciationPeriod",
                P_Name="DepreciationPeriod", Level=2,
                Parent_Node_Name="FA", Value_Type=2,
                Table_Name="FABuffer", Column_Name="DepreciationPeriod",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=26, P_Code="DepreciationStartingDate",
                P_Name="DepreciationStartingDate", Level=2,
                Parent_Node_Name="FA", Value_Type=5,
                Table_Name="FABuffer", Column_Name="DepreciationStartingDate",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="FA",
                Sequence=27, P_Code="CostCenterCode",
                P_Name="CostCenterCode", Level=2,
                Parent_Node_Name="FA", Value_Type=1,
                Table_Name="FABuffer", Column_Name="CostCenterCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            )
        ]
    inv_p = [
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=1, P_Code="Transaction",
                P_Name="Transaction", Level=0,
                Parent_Node_Name="", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=2, P_Code="General",
                P_Name="General", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=3, P_Code="DMSCode",
                P_Name="DMSCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=4, P_Code="DMSTitle",
                P_Name="DMSTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=5, P_Code="CompanyCode",
                P_Name="CompanyCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=6, P_Code="CompanyTitle",
                P_Name="CompanyTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=7, P_Code="CreateDateTime",
                P_Name="CreateDateTime", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CreateDateTime",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=8, P_Code="Creator",
                P_Name="Creator", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="Creator",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=9, P_Code="Invoice",
                P_Name="Invoice", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=10, P_Code="InvoiceType",
                P_Name="InvoiceType", Level=2,
                Parent_Node_Name="Invoice", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="InvoiceType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=11, P_Code="INVHeader",
                P_Name="INVHeader", Level=2,
                Parent_Node_Name="Invoice", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=12, P_Code="InvoiceNo",
                P_Name="InvoiceNo", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="InvoiceNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=13, P_Code="PostingDate",
                P_Name="PostingDate", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=5,
                Table_Name="InvoiceHeaderBuffer", Column_Name="[Posting Date]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=14, P_Code="DocumentDate",
                P_Name="DocumentDate", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=5,
                Table_Name="InvoiceHeaderBuffer", Column_Name="[Document Date]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=15, P_Code="DueDate",
                P_Name="DueDate", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=5,
                Table_Name="InvoiceHeaderBuffer", Column_Name="[Due Date]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=16, P_Code="PayToBillToNo",
                P_Name="PayToBillToNo", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=5,
                Table_Name="InvoiceHeaderBuffer", Column_Name="PayToBillToNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=17, P_Code="SellToBuyFromNo",
                P_Name="SellToBuyFromNo", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="SellToBuyFromNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=18, P_Code="CostCenterCode",
                P_Name="CostCenterCode", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="CostCenterCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=19, P_Code="VehicleSeries",
                P_Name="VehicleSeries", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="VehicleSeries",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=20, P_Code="ExtDocumentNo",
                P_Name="ExtDocumentNo", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="ExtDocumentNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=21, P_Code="PriceIncludeVAT",
                P_Name="PriceIncludeVAT", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=2,
                Table_Name="InvoiceHeaderBuffer", Column_Name="PriceIncludeVAT",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=22, P_Code="Description",
                P_Name="Description", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="Description",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=23, P_Code="Location",
                P_Name="Location", Level=3,
                Parent_Node_Name="INVHeader", Value_Type=1,
                Table_Name="InvoiceHeaderBuffer", Column_Name="Location",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=24, P_Code="INVLine",
                P_Name="INVLine", Level=2,
                Parent_Node_Name="Invoice", Value_Type=1,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=25, P_Code="LineNo",
                P_Name="LineNo", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="[Line No_]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=26, P_Code="DMSItemType",
                P_Name="DMSItemType", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="DMSItemType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=27, P_Code="GLAccount",
                P_Name="GLAccount", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="GLAccount",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=28, P_Code="Description",
                P_Name="Description", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="Description",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=29, P_Code="CostCenterCode",
                P_Name="CostCenterCode", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="CostCenterCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=30, P_Code="VehicleSeries",
                P_Name="VehicleSeries", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="VehicleSeries",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=31, P_Code="VINNo",
                P_Name="VINNo", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="VIN",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=32, P_Code="QTY",
                P_Name="QTY", Level=3,
                Parent_Node_Name="INVLine", Value_Type=3,
                Table_Name="InvoiceLineBuffer", Column_Name="Quantity",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=33, P_Code="LineAmount",
                P_Name="LineAmount", Level=3,
                Parent_Node_Name="INVLine", Value_Type=3,
                Table_Name="InvoiceLineBuffer", Column_Name="[Line Amount]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=34, P_Code="LineCost",
                P_Name="LineCost", Level=3,
                Parent_Node_Name="INVLine", Value_Type=3,
                Table_Name="InvoiceLineBuffer", Column_Name="LineCost",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=35, P_Code="LineDiscountAmount",
                P_Name="LineDiscountAmount", Level=3,
                Parent_Node_Name="INVLine", Value_Type=3,
                Table_Name="InvoiceLineBuffer", Column_Name="[Line Discount Amount]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=36, P_Code="LineVATAmount",
                P_Name="LineVATAmount", Level=3,
                Parent_Node_Name="INVLine", Value_Type=3,
                Table_Name="InvoiceLineBuffer", Column_Name="[Line VAT Amount]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=37, P_Code="LineVATRate",
                P_Name="LineVATRate", Level=3,
                Parent_Node_Name="INVLine", Value_Type=3,
                Table_Name="InvoiceLineBuffer", Column_Name="[Line VAT Rate]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=38, P_Code="TransactionType",
                P_Name="TransactionType", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="TransactionType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=39, P_Code="WIPNo",
                P_Name="WIPNo", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="[WIP No_]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=40, P_Code="FromCompanyName",
                P_Name="FromCompanyName", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="FromCompanyName",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=41, P_Code="ToCompanyName",
                P_Name="ToCompanyName", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="ToCompanyName",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=42, P_Code="Location",
                P_Name="Location", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="Location",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Invoice",
                Sequence=43, P_Code="MovementType",
                P_Name="MovementType", Level=3,
                Parent_Node_Name="INVLine", Value_Type=1,
                Table_Name="InvoiceLineBuffer", Column_Name="MovementType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
        ]
    other_p = [
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=1, P_Code="Transaction",
                P_Name="Transaction", Level=0,
                Parent_Node_Name="", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=2, P_Code="General",
                P_Name="General", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=3, P_Code="DMSCode",
                P_Name="DMSCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=4, P_Code="DMSTitle",
                P_Name="DMSTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="DMSTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=5, P_Code="CompanyCode",
                P_Name="CompanyCode", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=6, P_Code="CompanyTitle",
                P_Name="CompanyTitle", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CompanyTitle",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=7, P_Code="CreateDateTime",
                P_Name="CreateDateTime", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="CreateDateTime",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=8, P_Code="Creator",
                P_Name="Creator", Level=2,
                Parent_Node_Name="General", Value_Type=1,
                Table_Name="DMSInterfaceInfo", Column_Name="Creator",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=9, P_Code="Daydook",
                P_Name="Daydook", Level=1,
                Parent_Node_Name="Transaction", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=10, P_Code="DaydookNo",
                P_Name="DaydookNo", Level=2,
                Parent_Node_Name="Daydook", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="DocumentNo_",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=11, P_Code="Line",
                P_Name="Line", Level=2,
                Parent_Node_Name="Daydook", Value_Type=6,
                Table_Name="", Column_Name="",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=12, P_Code="TransactionType",
                P_Name="TransactionType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="TransactionType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=13, P_Code="LineNo",
                P_Name="LineNo", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[Line No_]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=14, P_Code="PostingDate",
                P_Name="PostingDate", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[Posting Date]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=15, P_Code="DocumentDate",
                P_Name="DocumentDate", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[Document Date]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=16, P_Code="ExtDocumentNo",
                P_Name="ExtDocumentNo", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="ExtDocumentNo_",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=17, P_Code="AccountType",
                P_Name="AccountType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="AccountType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=18, P_Code="AccountNo",
                P_Name="AccountNo", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[Account No_]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=19, P_Code="Description",
                P_Name="Description", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="Description",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=20, P_Code="DebitValue",
                P_Name="DebitValue", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[Debit Value]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=21, P_Code="CreditValue",
                P_Name="CreditValue", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[Credit Value]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=22, P_Code="CostCenterCode",
                P_Name="CostCenterCode", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="CostCenterCode",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=23, P_Code="VehicleSeries",
                P_Name="VehicleSeries", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="VehicleSeries",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=24, P_Code="VINNo",
                P_Name="VINNo", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="VIN",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=25, P_Code="WIPNo",
                P_Name="WIPNo", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[WIP No_]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=26, P_Code="FAPostingType",
                P_Name="FAPostingType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="[FA Posting Type]",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=27, P_Code="EntryType",
                P_Name="EntryType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="EntryType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=28, P_Code="FromCompanyName",
                P_Name="FromCompanyName", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="FromCompanyName",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=29, P_Code="ToCompanyName",
                P_Name="ToCompanyName", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="ToCompanyName",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=30, P_Code="SourceType",
                P_Name="SourceType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="SourceType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=31, P_Code="SourceNo",
                P_Name="SourceNo", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="SourceNo",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=32, P_Code="DMSItemType",
                P_Name="DMSItemType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="DMSItemType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=33, P_Code="DMSItemTransType",
                P_Name="DMSItemTransType", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="DMSItemTransType",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            ),
            ApiPOutSetup(
                Company_Code=company_code, API_Code="Other",
                Sequence=34, P_Code="Location",
                P_Name="Location", Level=3,
                Parent_Node_Name="Line", Value_Type=1,
                Table_Name="OtherBuffer", Column_Name="Location",
                Last_Modified_DT=datetime.datetime.now().isoformat(timespec='seconds'), Last_Modified_By=""
            )
        ]
    return cust_vend_p, fa_p, inv_p, other_p


# test data for sending notification
def test_data_for_notification():
    notification_users = [
        NotificationUser(
            Company_Code="K302ZH", User_Name="shingler",
            Email_Address="shingler@gf-app.cn", Activated=True,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"), Last_Modified_By=""
        ),
        NotificationUser(
            Company_Code="K302ZH", User_Name="moore",
            Email_Address="moore0101@gf-app.cn", Activated=False,
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="milliseconds"), Last_Modified_By=""
        )
    ]
    user_it = [
        UserList(
            UserID="amanda",
            Password="123",
            Blocked=False,
            Receive_Notification=True,
            Email_Address="49273395@qq.com",
            Telephone="123456",
            Cell_Phone="",
            Last_Modified_DT="",
            Last_Modified_By=""
        ),
        UserList(
            UserID="bran",
            Password="123",
            Blocked=False,
            Receive_Notification=False,
            Email_Address="singlerwong@gmail.com",
            Telephone="123456",
            Cell_Phone="",
            Last_Modified_DT="",
            Last_Modified_By=""
        )
    ]
    setup = [
        SystemSetup(
            Email_SMTP="smtp.163.com",
            SMTP_Port="465",
            Email_UserID="singlerwong@163.com",
            Email_Password="XJZDDLHZYACGJVWM",
            Last_Modified_DT=datetime.datetime.now().isoformat(timespec="seconds"),
            Last_Modified_By=""
        )
    ]
    return notification_users, user_it, setup


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        if app.config["ENV"] == "production":
            print("Error! This init DB script cannot run on production environment")
            exit(0)
        print("Warning! You are running init DB script on %s environment. \n"
              "This will erase all the data. \nPlease make sure you want to do this!" % app.config["ENV"])
        answer = input("Please input Y to run or any key to cancel.")
        if answer.upper() != "Y":
            exit(0)
        db.drop_all(bind=None)
        db.create_all(bind=None)
        # 插入测试数据
        db.session.add_all(test_data_for_company())

        # test data for task
        task_xml, task_api = test_data_for_task()
        db.session.add_all(task_xml)
        db.session.add_all(task_api)

        # test data for api_setup
        setup_for_xml, setup_for_api, setup_will_error = test_data_for_setup()
        db.session.add_all(setup_for_xml)
        db.session.add_all(setup_for_api)
        db.session.add_all(setup_will_error)

        # test data for setup_p_in
        p_in_1 = test_data_for_in_param("K302ZH")
        db.session.add_all(p_in_1)
        p_in_2 = test_data_for_in_param("K302ZS")
        db.session.add_all(p_in_2)

        # test data for setup_p_out
        cust_vend_p_success, fa_p_success, inv_p_success, other_p_success = test_data_for_out_param("K302ZH")
        db.session.add_all(cust_vend_p_success)
        db.session.add_all(fa_p_success)
        db.session.add_all(inv_p_success)
        db.session.add_all(other_p_success)

        cust_vend_p_retry, fa_p_retry, inv_p_retry, other_p_retry = test_data_for_out_param("K302ZS")
        db.session.add_all(cust_vend_p_retry)
        db.session.add_all(fa_p_retry)
        db.session.add_all(inv_p_retry)
        db.session.add_all(other_p_retry)

        db.session.commit()
