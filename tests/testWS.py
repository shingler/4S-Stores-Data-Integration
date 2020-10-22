#!/usr/bin/python
# -*- coding:utf-8 -*-
import base64

import pytest
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from suds.client import Client
from suds.sax.attribute import Attribute
from suds.sax.element import Element
from suds.transport.http import HttpAuthenticated
from suds.transport.https import WindowsHttpAuthenticated
from requests_ntlm import HttpNtlmAuth

@pytest.mark.skip("试试别的方法")
def test_ws_custvend():
    url = "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI"
    username = "NAVWebUser"
    password = "Hytc_1qaz@WSX"

    # t = HttpAuthenticated(username=username, password=password)
    # client = Client(url, transport=t)

    # usr = Element('USER').setText(username)
    # pwd = Element('PASSWORD').setText(password)
    # header_list = [usr, pwd]
    # reqsoap_attribute = Attribute('xsi:type', "xsd:string")
    # for param in header_list:
    #     param.append(reqsoap_attribute)
    # client = Client(url)
    # client.set_options(soapheaders=header_list)

    ntlm = WindowsHttpAuthenticated(username=username, password=password)
    client = Client(url, transport=ntlm)

    response = requests.post(url, auth=HttpNtlmAuth(username, password))
    print(response)
    print(response.headers)

    # str1 = '%s:%s' % (username, password)
    # be = base64.encodestring(str1.encode(encoding="utf-8"))
    # print(type(be))
    # base64string = be.replace(b'\n', b'')
    # authenticationHeader = {
    #     "SOAPAction": "HandleCVInfoWithEntryNo",
    #     "Authorization": "Basic %s" % base64string
    # }
    # client = Client(url, headers=authenticationHeader)

    res = client.service.HandleCVInfoWithEntryNo(6514, 0)
    print(res)


def test_InvokeWebservice():
    url = "http://62.234.26.35:7047/DynamicsNAV/WS/K302%20Zhuhai%20JJ/Codeunit/DMSWebAPI"
    username = "NAVWebUser"
    password = "Hytc_1qaz@WSX"

    postcontent='<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><HandleCVInfoWithEntryNo xmlns="urn:microsoft-dynamics-schemas/codeunit/DMSWebAPI"><entryNo>6514</entryNo><_CalledBy>0</_CalledBy></HandleCVInfoWithEntryNo></soap:Body></soap:Envelope>'
    req = requests.post(url, auth=HttpNtlmAuth(username, password), data=postcontent.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    print(req)


