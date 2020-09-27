#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, make_response
import xmltodict, json

app = Flask(__name__)


@app.route("/dms/api/cust_vend_info", methods=["GET"])
def custVendInfo():
    # 模拟接口，读取xml文件并以json格式输出
    with open("docs/CustVendInfo.xml", "rb") as xml_src:
        dict = xmltodict.parse(xml_src.read())
        response = make_response(json.dumps(dict))
        return response


@app.route("/dms/api/fa", methods=["GET"])
def fa():
    # 模拟接口，读取xml文件并以json格式输出
    with open("docs/FA.xml", "rb") as xml_src:
        dict = xmltodict.parse(xml_src.read())
        response = make_response(json.dumps(dict))
        return response


@app.route("/dms/api/invoice", methods=["GET"])
def invoice():
    # 模拟接口，读取xml文件并以json格式输出
    with open("docs/Invoice.xml", "rb") as xml_src:
        dict = xmltodict.parse(xml_src.read())
        response = make_response(json.dumps(dict))
        return response


@app.route("/dms/api/other", methods=["GET"])
def other():
    # 模拟接口，读取xml文件并以json格式输出
    with open("docs/Other.xml", "rb") as xml_src:
        dict = xmltodict.parse(xml_src.read())
        response = make_response(json.dumps(dict))
        return response


if __name__ == '__main__':
    app.run()
