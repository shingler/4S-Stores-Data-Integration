#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import jsonify, request
import datetime
from src import create_app
from bin import cust_vend, fa, invoice, other
app = create_app()


# cust vend 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param string curdate 日期：格式YYYYMMDD，默认为空则表示读取当天xml
@app.route('/cust_vend', methods=["POST"])
def cust_vend_api():
    company_code = ""
    api_code = ""
    cur_date = datetime.datetime.now().strftime('%Y%m%d')
    retry = 0
    if request.method == "POST":
        company_code = request.form.get("company_code")
        api_code = request.form.get("api_code")
        cur_date = request.form.get("cur_date", datetime.datetime.now().strftime('%Y%m%d'))
        retry = request.form.get("retry", 0)
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    else:
        try:
            entry_no = cust_vend.main(company_code=company_code, api_code=api_code, cur_date=cur_date, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except Exception as ex:
            res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


# fa 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param string curdate 日期：格式YYYYMMDD，默认为空则表示读取当天xml
@app.route('/fa', methods=["POST"])
def fa_api():
    company_code = ""
    api_code = ""
    cur_date = datetime.datetime.now().strftime('%Y%m%d')
    retry = 0
    if request.method == "POST":
        company_code = request.form.get("company_code")
        api_code = request.form.get("api_code")
        cur_date = request.form.get("cur_date", datetime.datetime.now().strftime('%Y%m%d'))
        retry = request.form.get("retry", 0)
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    else:
        try:
            entry_no = fa.main(company_code=company_code, api_code=api_code, cur_date=cur_date, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except Exception as ex:
            print(ex)
            res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


# invoice 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param string curdate 日期：格式YYYYMMDD，默认为空则表示读取当天xml
@app.route('/invoice', methods=["POST"])
def invoice_api():
    company_code = ""
    api_code = ""
    cur_date = datetime.datetime.now().strftime('%Y%m%d')
    retry = 0
    if request.method == "POST":
        company_code = request.form.get("company_code")
        api_code = request.form.get("api_code")
        cur_date = request.form.get("cur_date", datetime.datetime.now().strftime('%Y%m%d'))
        retry = request.form.get("retry", 0)
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    else:
        try:
            entry_no = invoice.main(company_code=company_code, api_code=api_code, cur_date=cur_date, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except Exception as ex:
            res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


# other 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param string curdate 日期：格式YYYYMMDD，默认为空则表示读取当天xml
@app.route('/other', methods=["GET", "POST"])
def other_api():
    company_code = ""
    api_code = ""
    cur_date = datetime.datetime.now().strftime('%Y%m%d')
    retry = 0
    if request.method == "POST":
        company_code = request.form.get("company_code")
        api_code = request.form.get("api_code")
        cur_date = request.form.get("cur_date", datetime.datetime.now().strftime('%Y%m%d'))
        retry = request.form.get("retry", 0)
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    else:
        try:
            entry_no = other.main(company_code=company_code, api_code=api_code, cur_date=cur_date, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except Exception as ex:
            res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


if __name__ == '__main__':
    app.run()
