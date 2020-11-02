#!/usr/bin/python
# -*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()
import json
from flask import jsonify, request, Response
from src import create_app
from bin import cust_vend, fa, invoice, other
from src import error

app = create_app()


# 接口状态获取
@app.route("/")
def default():
    return Response("It Works!")


# cust vend 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param int api_type 接口类型：1=JSON API，2=XML
# @param string options 指定参数，格式为JSON，详见说明文档
@app.route('/cust_vend', methods=["POST"])
def cust_vend_api():
    res = {}

    if request.method != "POST":
        return jsonify({"status": 400, "error_message": "请求方式有误，请使用POST方法"})

    company_code = request.form.get("company_code", "")
    api_code = request.form.get("api_code", "")
    retry = request.form.get("retry", 0)
    api_type = request.form.get("api_type", 0)
    options = request.form.get("options", "")
    if len(options) > 0:
        options = json.loads(options, encoding="UTF-8")

    # 参数检查
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    elif api_type == "1":
        # 解析JSON API
        res = {"status": 10006, "error_message": "暂不支持JSON API方式"}
    elif api_type == "2":
        file_path = options["file_path"] if "file_path" in options else None
        try:
            entry_no = cust_vend.main(company_code=company_code, api_code=api_code, file_path=file_path, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except error.DataFieldEmptyError as ex:
            res = {"status": 10001, "error_message": str(ex)}
        except error.InvoiceEmptyError as ex:
            res = {"status": 10002, "error_message": str(ex)}
        except error.DataLoadError as ex:
            res = {"status": 10003, "error_message": str(ex)}
        except error.DataLoadTimeOutError as ex:
            res = {"status": 10004, "error_message": str(ex)}
        except error.DataImportRepeatError as ex:
            res = {"status": 10007, "error_message": str(ex)}
        except Exception as ex:
            res = {"status": 10000, "error_message": str(ex)}
    else:
        res = {"status": 10005, "error_message": "无效的参数"}
    return jsonify(res)


# fa 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param int api_type 接口类型：1=JSON API，2=XML
# @param string options 指定参数，格式为JSON，详见说明文档
@app.route('/fa', methods=["POST"])
def fa_api():
    res = {}

    if request.method != "POST":
        return jsonify({"status": 400, "error_message": "请求方式有误，请使用POST方法"})

    company_code = request.form.get("company_code", "")
    api_code = request.form.get("api_code", "")
    retry = request.form.get("retry", 0)
    api_type = request.form.get("api_type", 0)
    options = request.form.get("options", "")
    if len(options) > 0:
        options = json.loads(options, encoding="UTF-8")

    # 参数检查
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    elif api_type == "1":
        # 解析JSON API
        res = {"status": 20006, "error_message": "暂不支持JSON API方式"}
    elif api_type == "2":
        file_path = options["file_path"] if "file_path" in options else None
        try:
            entry_no = fa.main(company_code=company_code, api_code=api_code, file_path=file_path, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except error.DataFieldEmptyError as ex:
            res = {"status": 20001, "error_message": str(ex)}
        except error.InvoiceEmptyError as ex:
            res = {"status": 20002, "error_message": str(ex)}
        except error.DataLoadError as ex:
            res = {"status": 20003, "error_message": str(ex)}
        except error.DataLoadTimeOutError as ex:
            res = {"status": 20004, "error_message": str(ex)}
        except error.DataImportRepeatError as ex:
            res = {"status": 20007, "error_message": str(ex)}
        except Exception as ex:
            res = {"status": 20000, "error_message": str(ex)}
    else:
        res = {"status": 20005, "error_message": "无效的参数"}
    return jsonify(res)


# invoice 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param int api_type 接口类型：1=JSON API，2=XML
# @param string options 指定参数，格式为JSON，详见说明文档
@app.route('/invoice', methods=["POST"])
def invoice_api():
    res = {}

    if request.method != "POST":
        return jsonify({"status": 400, "error_message": "请求方式有误，请使用POST方法"})

    company_code = request.form.get("company_code", "")
    api_code = request.form.get("api_code", "")
    retry = request.form.get("retry", 0)
    api_type = request.form.get("api_type", 0)
    options = request.form.get("options", "")
    if len(options) > 0:
        options = json.loads(options, encoding="UTF-8")

    # 参数检查
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    elif api_type == "1":
        # 解析JSON API
        res = {"status": 30006, "error_message": "暂不支持JSON API方式"}
    elif api_type == "2":
        file_path = options["file_path"] if "file_path" in options else None
        try:
            entry_no = invoice.main(company_code=company_code, api_code=api_code, file_path=file_path, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except error.DataFieldEmptyError as ex:
            res = {"status": 30001, "error_message": str(ex)}
        except error.InvoiceEmptyError as ex:
            res = {"status": 30002, "error_message": str(ex)}
        except error.DataLoadError as ex:
            res = {"status": 30003, "error_message": str(ex)}
        except error.DataLoadTimeOutError as ex:
            res = {"status": 30004, "error_message": str(ex)}
        except error.DataImportRepeatError as ex:
            res = {"status": 30007, "error_message": str(ex)}
        except Exception as ex:
            res = {"status": 30000, "error_message": str(ex)}
    else:
        res = {"status": 30005, "error_message": "无效的参数"}
    return jsonify(res)


# other 接口手动调用
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param int api_type 接口类型：1=JSON API，2=XML
# @param string options 指定参数，格式为JSON，详见说明文档
@app.route('/other', methods=["POST"])
def other_api():
    res = {}

    if request.method != "POST":
        return jsonify({"status": 400, "error_message": "请求方式有误，请使用POST方法"})

    company_code = request.form.get("company_code", "")
    api_code = request.form.get("api_code", "")
    retry = request.form.get("retry", 0)
    api_type = request.form.get("api_type", 0)
    options = request.form.get("options", "")
    if len(options) > 0:
        options = json.loads(options, encoding="UTF-8")

    # 参数检查
    if company_code == "" or api_code == "":
        res = {"status": 0, "error_message": "company_code或api_code不能为空"}
    elif api_type == "1":
        # 解析JSON API
        res = {"status": 40006, "error_message": "暂不支持JSON API方式"}
    elif api_type == "2":
        file_path = options["file_path"] if "file_path" in options else None
        try:
            entry_no = other.main(company_code=company_code, api_code=api_code, file_path=file_path, retry=True if retry else False)
            res = {"status": 1, "entry_no": entry_no}
        except error.DataFieldEmptyError as ex:
            res = {"status": 40001, "error_message": str(ex)}
        except error.InvoiceEmptyError as ex:
            res = {"status": 40002, "error_message": str(ex)}
        except error.DataLoadError as ex:
            res = {"status": 40003, "error_message": str(ex)}
        except error.DataLoadTimeOutError as ex:
            res = {"status": 40004, "error_message": str(ex)}
        except error.DataImportRepeatError as ex:
            res = {"status": 40007, "error_message": str(ex)}
        except Exception as ex:
            res = {"status": 40000, "error_message": str(ex)}
    else:
        res = {"status": 40005, "error_message": "无效的参数"}
    return jsonify(res)


if __name__ == '__main__':
    app.run(threaded=True)
