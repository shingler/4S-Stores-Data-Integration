#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import jsonify

from src import create_app
from bin import cust_vend
app = create_app()


@app.route('/cust_vend/<string:company_code>/<string:api_code>', methods=["GET", "POST"])
def cust_vend_info(company_code, api_code):
    try:
        entry_no = cust_vend.main(company_code=company_code, api_code=api_code)
        res = {"status": 1, "entry_no": entry_no}
    except Exception as ex:
        res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


@app.route('/fa/<string:company_code>/<string:api_code>', methods=["GET", "POST"])
def fa(company_code, api_code):
    try:
        entry_no = fa.main(company_code=company_code, api_code=api_code)
        res = {"status": 1, "entry_no": entry_no}
    except Exception as ex:
        res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


@app.route('/invoice/<string:company_code>/<string:api_code>', methods=["GET", "POST"])
def invoice(company_code, api_code):
    try:
        entry_no = invoice.main(company_code=company_code, api_code=api_code)
        res = {"status": 1, "entry_no": entry_no}
    except Exception as ex:
        res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


@app.route('/other/<string:company_code>/<string:api_code>', methods=["GET", "POST"])
def other(company_code, api_code):
    try:
        entry_no = other.main(company_code=company_code, api_code=api_code)
        res = {"status": 1, "entry_no": entry_no}
    except Exception as ex:
        res = {"status": 0, "error_message": str(ex)}
    return jsonify(res)


if __name__ == '__main__':
    app.run()
