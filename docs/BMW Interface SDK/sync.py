# -*- coding: utf-8 -*-
import datetime
import logging
import json
import requests
from django.db import connection
from sco_request_sdk.sign.security_util import get_signature_dict
from app.models import custvendinfo
from app.models import invoice
from app.models import others
logger = logging.getLogger('log')

#初始化接口
ACCESS_KEY_SECRET ="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk6oiR0kV/4tSwQZBnTAEN4teEdy+NyGpoOmNkN6puE0qPLaCcPfzt5lLdXn3QtOPtBeE56ZJCGC4ZIvspPZQWuHOJOrIbU9n1OpfuBeE3+iTvYYznmMTNgrwifbS75S+IefMGUx6hPF0lsDW5Cnz+8JTwcmj9h5zvnhsv1QSp5QBo+n1zjW1vXOUnYcaHE8J2JifCkcDqqBHsHUz49uyCVBT4zB8fhKP8FJLPoC4rxPENydlp3IVCD6gTrxSr5s5hwXOcxbvFfEqLft6xwjSb14pm9qQG1Vp4vQMmFaPTtdAD8yk+MqgEJvVxCGL/wtBxsxoCGIF71nXTOKW2rlNAgMBAAECggEATrkqig0IF9W8MK3BnmxvjYBfHD8zB+D2ximCpaqPTAPP257ae38xlSJQHT3WmCq+EYcvdiIF3PmI/tGynxh8LecG9J7tVOQKq+XkdINd8e9LeOZsFRV9QWVabjVXbqUKq42vqQseEfee5MxcA/eqwSqDjKUuyIYEgHYpVYc6s9byS+YiQq2uWhuu9Zjsu40PdVu9LhyuOS4oexJCxaOFs42mUYXtlysHL/6kvU3E94kJOC8Ki1mHIOnWgyBWgw36EzUOLovCSR1gx0kM65zUPFcGXPbJMtHHiFSSbmzDSr2bSoqKLoEdKLmSM7lBJusaWqI/0U4nO8x4LnUsE9W/SQKBgQDzx473wlj75NG6YjiWXO5Xss1W6F9XOjuFfs2G1vWOMgsBCPZup1QEKq9m6vaKwtBbalI9ehCFY7eBKCH5ai2mVwink61/sLvF3pjyzs65oCvNU2LgtlKsa5m+RVkvZoK4+dSb2hk033xlfzyDtklCeg5H18udUSZUInElBM1TcwKBgQCWxjJsvsdU6v65HdINRmgmMyh56PrIMRLgpIicqemepqASdUiNIm27u8ya35J6Si1sL2ASPYRbB1cKvt57yOpjjrSPE2PMaYNKZQfqs+h3XkvsroS7t2ySESLDOpB0vsE30hDPlTRzVFQ+raXjVkVmBtnTxezjaWY9GPF+cXQQPwKBgB1vJfMCU04uxaf0fhKhq+GI5EQvEHvuuwsWUWiLgeCmaC+6zk50A6/xG3aYviXo+dFf2Ag2OdJxRNHib5+200Y3UgMx0IwPYcy1YNBIait9jGxhOhoZyYeqAkk4BFm1zejZuXML9Wkt5s42e68HjnbpV9oS0zHuf2s/MVwf5U7DAoGAJgpVeJhdxHAR2nTKpWzJJDIuGSwN8epnv+PjT9uSxON3aZDLwEgadY45Xi3gUBhdA3mkfJWmyiy86koj6glUEdBUf/C9cjqA1IlPCQlhMpTJBSs29AGgU+4c3jLtdXcXWtUWRrl3ZU22f6XiP8xpcAd0d/js/qd+ExYy/9ryFJMCgYA04TrRNNFc4AQHrzX7R8c0VpAAFYZA3IhQZeLyOF3WwnHpEFZwz4T3ktQSmDNFRab4G2md8md4Ww88T1ASC4ASLWvPAXu9lU8gmvLrUFREmw4hmeFGPAKZP8OrS6KJu1aMFBNEPgqiS6T8Ie/eGMy97e8PPUWlGO9L544Seoh1UQ=="
REQUEST_URL = "https://spark-dms-i.bmwgroup.com.cn/ddsp-api/api/g000035/adapterInterface"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}


class Interface:
    SIGNATURE_VERSION = "1.0"
    FORMAT = "json"
    VERSION = "v1"
    SIGNATURE_METHOD = "SHA256withRSA"

    def __init__(self, dealer_entity_code , dealer_group_code, action):
        self.dealer_entity_code = dealer_entity_code
        self.dealer_group_code = dealer_group_code
        self.action = action

    def get_interface_params(self, data):
        return {
            'SignatureVersion': self.SIGNATURE_VERSION,
            'Action': self.action,
            'Format': self.FORMAT,
            'Version': self.VERSION,
            'DealerGroupCode': self.dealer_group_code,
            'DealerEntityCode': self.dealer_entity_code,
            'SignatureMethod': self.SIGNATURE_METHOD,
            'Data': json.dumps(data),
            'AccessKeySecret': ACCESS_KEY_SECRET
        }

#调用接口，请求宝马接口发送调用信息
def send_data(data, interface_instance: Interface) -> requests.Response:
    # 原始请求数据
    params = interface_instance.get_interface_params(data)
    #print(params)
    # 用于签名后的data
    url = REQUEST_URL.format(interface_instance.action.lower())
    sign_dict = get_signature_dict(params)
    return requests.post(url=url, data=json.dumps(sign_dict), headers=HEADERS)

    # Custvendinfo接口调用，同步后返回对象
def api_custvendinfo(starttime, endtime, dealer_entity_code, operator):
    apiname='custvendinfo'
    dealer_group_code = 'G000035'  # 经销商集团代码
    action = 'G102010000'  # CustVendInfo接口代码
    entitycode = dealer_entity_code
    recordtotal = 0  # 总计
    recordupdate = 0  # 更新数
    recordinsert = 0  # 插入数
    recordsuccess = 0  # 成功数
    recordfail = 0  # 失败数
    # 创建
    interface_instance = Interface(
        dealer_entity_code=dealer_entity_code,
        dealer_group_code=dealer_group_code,
        action=action
    )


    data = {"apiQueryDateBegin": starttime, "apiQueryDateEnd": endtime}
    logger.info(data)
    resp = send_data(data, interface_instance)  #调用接口
    code=resp.json()["Code"]
    logger.info(resp.json()) #将返回写入日志

    #开始取数并解析数据
    if code!= '200' or 'no' not in json.dumps(resp.json()["Data"]): #原则上只需要判单code=200即可，但是由于当返回为空的时候无法判断code，需要判单Data中是否有数据
        retmsg= '0'
    else:
        jsonresp = resp.json()["Data"]
        for re in jsonresp:# 插入一条操作日志完成本次更新
            no = re["no"]
            name = re["name"]
            dmstitle = re["dmstitle"]
            template = re["template"]
            country = re["country"]
            creator = re["creator"]
            pricesincludingvat = re["pricesincludingvat"]
            costcentercode = re["costcentercode"]
            address = re["address"]
            dmscode = re["dmscode"]
            city = re["city"]
            paymentmethodcode = re["paymentmethodcode"]
            address2 = re["address2"]
            postcode = re["postcode"]
            arapaccountno = re["arapaccountno"]
            type = re["type"]
            phoneno = re["phoneno"]
            companycode = re["companycode"]
            blocked = re["blocked"]
            faxno = re["faxno"]
            applicationmethod = re["applicationmethod"]
            paymenttermscode = re["paymenttermscode"]
            currency = re["currency"]
            companytitle = re["companytitle"]
            createdatetime = re["createdatetime"]
            email = re["email"]
            lastupdatetime = datetime.datetime.now()


            recordtotal = recordtotal + 1  # 总数
            recordsuccess=recordsuccess+1 #成功记录数，默认都是成功的
            # 判断是否存在
            ls = custvendinfo.objects.filter(no=no)
            if ls:# 存在插入更新
                recordupdate=recordupdate+1 #更新成功记录数
                with connection.cursor() as cursor:
                    cursor.execute(
                        'UPDATE app_custvendinfo SET name=%s, dmstitle=%s, template=%s, country=%s, creator=%s, pricesincludingvat=%s, costcentercode=%s, address=%s, dmscode=%s, city=%s, paymentmethodcode=%s, address2=%s, postcode=%s, arapaccountno=%s, type=%s, phoneno=%s, companycode=%s, blocked=%s, faxno=%s, applicationmethod=%s, paymenttermscode=%s, currency=%s, companytitle=%s, createdatetime=%s, email=%s,lastupdatetime=%s WHERE no=%s', [name, dmstitle, template, country, creator, pricesincludingvat, costcentercode, address, dmscode, city, paymentmethodcode, address2, postcode, arapaccountno, type, phoneno, companycode, blocked, faxno, applicationmethod, paymenttermscode, currency, companytitle, createdatetime, email,lastupdatetime, no]
                    )
                logger.info('updata:' + no)
            else:# 不存在插入
                recordinsert=recordinsert+1 #插入成功记录数
                with connection.cursor() as cursor: #将解析明细插入数据库
                    cursor.execute(
                        'INSERT INTO app_custvendinfo (no, name, dmstitle, template, country, creator, pricesincludingvat, costcentercode, address, dmscode, city, paymentmethodcode, address2, postcode, arapaccountno, type, phoneno, companycode, blocked, faxno, applicationmethod, paymenttermscode, currency, companytitle, createdatetime, email,lastupdatetime) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        [no, name, dmstitle, template, country, creator, pricesincludingvat, costcentercode, address,
                         dmscode, city, paymentmethodcode, address2, postcode, arapaccountno, type, phoneno,
                         companycode, blocked, faxno,
                         applicationmethod, paymenttermscode, currency, companytitle, createdatetime, email,
                         lastupdatetime])
                logger.info('insert:' + no)
            retmsg = '1'
    # 结束取数


    #插入一条操作日志记录
    operationtime = datetime.datetime.now()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO app_apisynclog (apiname,entitycode,starttime,endtime,recordtotal,recordupdate,recordinsert,recordsuccess,recordfail,operator,operationtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            [apiname, entitycode, starttime, endtime, recordtotal, recordupdate, recordinsert, recordsuccess,recordfail, operator, operationtime])
    return retmsg

def api_invoice(starttime, endtime, dealer_entity_code, operator):
    apiname='invoice'
    dealer_group_code = 'G000035'  # 经销商集团代码
    action = 'G102010002'  # invoice接口代码
    entitycode = dealer_entity_code
    recordtotal = 0  # 总计
    recordupdate = 0  # 更新数
    recordinsert = 0  # 插入数
    recordsuccess = 0  # 成功数
    recordfail = 0  # 失败数
    # 创建
    interface_instance = Interface(
        dealer_entity_code=dealer_entity_code,
        dealer_group_code=dealer_group_code,
        action=action
    )
    data = {"apiQueryDateBegin": starttime, "apiQueryDateEnd": endtime}
    logger.info(data)
    resp = send_data(data, interface_instance)
    code=resp.json()["Code"]
    logger.info(resp.json())

    #开始取数并解析数据
    if code!= '200' or 'invoiceno' not in json.dumps(resp.json()["Data"]):
        retmsg= '0'
    else:
        jsonresp = resp.json()["Data"]
        for re in jsonresp:# 插入一条操作日志完成本次更新
            dmstitle = re["dmstitle"]
            dmsitemtype = re["dmsitemtype"]
            linevatamount = re["linevatamount"]
            costcentercode = re["costcentercode"]
            dmscode = re["dmscode"]
            description = re["description"]
            invoicetype = re["invoicetype"]
            priceincludevat = re["priceincludevat"]
            linediscountamount = re["linediscountamount"]
            transactiontype = re["transactiontype"]
            tocompanyname = re["tocompanyname"]
            lineamount = re["lineamount"]
            companycode = re["companycode"]
            postingdate = re["postingdate"]
            companytitle = re["companytitle"]
            oemcode = re["oemcode"]
            linecost = re["linecost"]
            wipno = re["wipno"]
            creator = re["creator"]
            paytobilltono = re["paytobilltono"]
            vinno = re["vinno"]
            vehicleseriesdetail = re["vehicleseriesdetail"]
            costcentercodedetail = re["costcentercodedetail"]
            vehicleseries = re["vehicleseries"]
            linenos = re["lineno"]
            glaccount = re["glaccount"]
            duedate = re["duedate"]
            qty = re["qty"]
            extdocumentno = re["extdocumentno"]
            createdatetime = re["createdatetime"]
            invoiceno = re["invoiceno"]
            selltobuyfromno = re["selltobuyfromno"]
            documentdate = re["documentdate"]
            fromcompanyname = re["fromcompanyname"]
            lastupdatetime = datetime.datetime.now()

            recordtotal = recordtotal + 1  # 总数
            recordsuccess=recordsuccess+1 #成功记录数，默认都是成功的
            # 判断是否存在
            ls = invoice.objects.filter(invoiceno=invoiceno, linenos=linenos)
            if ls:# 存在插入更新
                recordupdate=recordupdate+1 #更新成功记录数
                with connection.cursor() as cursor:
                    cursor.execute(
                        'UPDATE app_invoice SET dmstitle=%s,dmsitemtype=%s, linevatamount=%s, costcentercode=%s, dmscode=%s, description=%s, invoicetype=%s, priceincludevat=%s, linediscountamount=%s, transactiontype=%s, tocompanyname=%s, lineamount=%s, companycode=%s, postingdate=%s, companytitle=%s, oemcode=%s, linecost=%s, wipno=%s, creator=%s, paytobilltono=%s, vinno=%s, vehicleseriesdetail=%s, costcentercodedetail=%s, vehicleseries=%s, glaccount=%s, duedate=%s, qty=%s, extdocumentno=%s, createdatetime=%s, invoiceno=%s, selltobuyfromno=%s, documentdate=%s, fromcompanyname=%s, lastupdatetime=%s WHERE invoiceno=%s and linenos=%s ', [dmstitle, dmsitemtype, linevatamount, costcentercode, dmscode, description, invoicetype, priceincludevat, linediscountamount, transactiontype, tocompanyname, lineamount, companycode, postingdate, companytitle, oemcode, linecost, wipno, creator, paytobilltono, vinno, vehicleseriesdetail, costcentercodedetail, vehicleseries, glaccount, duedate, qty, extdocumentno, createdatetime, invoiceno, selltobuyfromno, documentdate, fromcompanyname, lastupdatetime,invoiceno,linenos])
                logger.info('updata:' + invoiceno +'-'+ linenos)
            else:# 不存在插入
                logger.info('linenos:' +linenos)
                recordinsert=recordinsert+1 #插入成功记录数
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO app_invoice (dmstitle,dmsitemtype, linevatamount, costcentercode, dmscode, description, invoicetype, priceincludevat, linediscountamount, transactiontype, tocompanyname, lineamount, companycode, postingdate, companytitle, oemcode, linecost, wipno, creator, paytobilltono, vinno, vehicleseriesdetail, costcentercodedetail, vehicleseries, linenos, glaccount, duedate, qty, extdocumentno, createdatetime, invoiceno, selltobuyfromno, documentdate, fromcompanyname, lastupdatetime) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [dmstitle,dmsitemtype, linevatamount, costcentercode, dmscode, description, invoicetype, priceincludevat, linediscountamount, transactiontype, tocompanyname, lineamount, companycode, postingdate, companytitle, oemcode, linecost, wipno, creator, paytobilltono, vinno, vehicleseriesdetail, costcentercodedetail, vehicleseries, linenos, glaccount, duedate, qty, extdocumentno, createdatetime, invoiceno, selltobuyfromno, documentdate, fromcompanyname, lastupdatetime])
                logger.info('insert:' + invoiceno +'-'+ linenos)
            retmsg = '1'
    # 结束取数


    #插入一条操作日志记录
    operationtime = datetime.datetime.now()
    with connection.cursor() as cursor:
        cursor.execute(
            'INSERT INTO app_apisynclog (apiname,entitycode,starttime,endtime,recordtotal,recordupdate,recordinsert,recordsuccess,recordfail,operator,operationtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            [apiname, entitycode, starttime, endtime, recordtotal, recordupdate, recordinsert, recordsuccess,recordfail, operator, operationtime])
    return retmsg

def api_other(starttime, endtime, dealer_entity_code, operator):
    apiname='other'
    dealer_group_code = 'G000035'  # 经销商集团代码
    action = 'G102010003'  # invoice接口代码
    entitycode = dealer_entity_code
    recordtotal = 0  # 总计
    recordupdate = 0  # 更新数
    recordinsert = 0  # 插入数
    recordsuccess = 0  # 成功数
    recordfail = 0  # 失败数
    # 创建
    interface_instance = Interface(
        dealer_entity_code=dealer_entity_code,
        dealer_group_code=dealer_group_code,
        action=action
    )
    data = {"apiQueryDateBegin": starttime, "apiQueryDateEnd": endtime}
    logger.info(data)
    resp = send_data(data, interface_instance)
    code=resp.json()["Code"]
    logger.info(resp.json())

    #开始取数并解析数据
    if code!= '200' or 'no' not in json.dumps(resp.json()["Data"]):
        retmsg= '0'
    else:
        jsonresp = resp.json()["Data"]
        for re in jsonresp:# 插入一条操作日志完成本次更新
            dmstitle = re["dmstitle"]
            costcentercode = re["costcentercode"]
            dmscode = re["dmscode"]
            accounttype = re["accounttype"]
            description = re["description"]
            sourceno = re["sourceno"]
            transactiontype = re["transactiontype"]
            tocompanyname = re["tocompanyname"]
            daydookno = re["daydookno"]
            entrytype = re["entrytype"]
            companycode = re["companycode"]
            fapostingtype = re["fapostingtype"]
            postingdate = re["postingdate"]
            sourcetype = re["sourcetype"]
            companytitle = re["companytitle"]
            wipno = re["wipno"]
            creator = re["creator"]
            vinno = re["vinno"]
            linenos = re["lineno"]
            vehicleseries = re["vehicleseries"]
            debitvalue = re["debitvalue"]
            accountno = re["accountno"]
            extdocumentno = re["extdocumentno"]
            createdatetime = re["createdatetime"]
            documentdate = re["documentdate"]
            creditvalue = re["creditvalue"]
            fromcompanyname = re["fromcompanyname"]
            lastupdatetime = datetime.datetime.now()


            recordtotal = recordtotal + 1  # 总数
            recordsuccess=recordsuccess+1 #成功记录数，默认都是成功的
            # 判断是否存在
            ls = others.objects.filter(daydookno=daydookno, linenos=linenos)
            if ls:# 存在插入更新
                recordupdate=recordupdate+1 #更新成功记录数
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE app_others SET dmstitle = %s,costcentercode = %s,dmscode = %s,accounttype = %s,description = %s,sourceno = %s,transactiontype = %s,tocompanyname = %s,entrytype = %s,companycode = %s,fapostingtype = %s,postingdate = %s,sourcetype = %s,companytitle = %s,wipno = %s,creator = %s,vinno = %s,vehicleseries = %s,debitvalue = %s,accountno = %s,extdocumentno = %s,createdatetime = %s,documentdate = %s,creditvalue = %s,fromcompanyname = %s,lastupdatetime = %s  WHERE daydookno=%s and linenos=%s', [dmstitle,costcentercode,dmscode,accounttype,description,sourceno,transactiontype,tocompanyname,entrytype,companycode,fapostingtype,postingdate,sourcetype,companytitle,wipno,creator,vinno,vehicleseries,debitvalue,accountno,extdocumentno,createdatetime,documentdate,creditvalue,fromcompanyname,lastupdatetime, daydookno, linenos])
                logger.info('updata:' + daydookno+'-'+linenos)
            else:# 不存在插入
                recordinsert=recordinsert+1 #插入成功记录数
                logger.info(lastupdatetime)

                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO app_others (dmstitle,costcentercode,dmscode,accounttype,description,sourceno,transactiontype,tocompanyname,daydookno,entrytype,companycode,fapostingtype,postingdate,sourcetype,companytitle,wipno,creator,vinno,linenos,vehicleseries,debitvalue,accountno,extdocumentno,createdatetime,documentdate,creditvalue,fromcompanyname,lastupdatetime) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',[dmstitle,costcentercode,dmscode,accounttype,description,sourceno,transactiontype,tocompanyname,daydookno,entrytype,companycode,fapostingtype,postingdate,sourcetype,companytitle,wipno,creator,vinno,linenos,vehicleseries,debitvalue,accountno,extdocumentno,createdatetime,documentdate,creditvalue,fromcompanyname,lastupdatetime])
                logger.info('insert:' + daydookno+'-'+linenos)
            retmsg = '1'
    # 结束取数


    #插入一条操作日志记录
    operationtime = datetime.datetime.now()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO app_apisynclog (apiname,entitycode,starttime,endtime,recordtotal,recordupdate,recordinsert,recordsuccess,recordfail,operator,operationtime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',[apiname, entitycode, starttime, endtime, recordtotal, recordupdate, recordinsert, recordsuccess,recordfail, operator, operationtime])
    return retmsg