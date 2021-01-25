#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import os
import logging
from logging import config
from flask import jsonify, request, Response
from src import create_app, words
from bin import cust_vend, fa, invoice, other
from src import error
from src.error import NodeNotExistError

app = create_app()
config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.conf"))

# 接口状态获取
@app.route("/")
def default():
    return Response("It Works!")


# dms接口统一入口
# @param string company_code 公司代码
# @param string api_code 执行代码
# @param string command_code 01=cust_vend, 02=fa, 03=invoice, 04=other
# @param int retry 是否重试。retry=0将按照地址1执行；为1则按照地址2执行。
# @param int api_type 接口类型：1=JSON API，2=XML
# @param string options 指定参数，格式为JSON
@app.route("/dms_interface", methods=["POST"])
def dms_interface_api():
    logger = logging.getLogger("dms_interface_api")
    if request.method != "POST":
        return jsonify({"status": 40000, "error_message": words.WebApi.method_error()})

    company_code = request.form.get("company_code", "")
    api_code = request.form.get("api_code", "")
    command_code = request.form.get("command_code", "01")
    retry = request.form.get("retry", 0)
    api_type = request.form.get("api_type", 0)
    option_str = request.form.get("options", "")
    userID = None

    logger.info("company_code=%s, api_code=%s" % (company_code, api_code))

    try:
        options = json.loads(option_str, encoding="UTF-8") if len(option_str) > 0 else None
    except json.decoder.JSONDecodeError:
        # json格式不正确
        return jsonify({"status": 40002, "error_message": words.WebApi.invalid_value("options", option_str)})

    # 参数检查
    if company_code == "":
        return jsonify({"status": 40001, "error_message": words.WebApi.filed_empty("company_code")})
    if api_code == "":
        return jsonify({"status": 40001, "error_message": words.WebApi.filed_empty("api_code")})
    if command_code not in ["01", "02", "03", "04"]:
        return jsonify({"status": 40002, "error_message": words.WebApi.invalid_value("command_code", command_code)})
    if api_type not in ["1", "2"]:
        return jsonify({"status": 40003, "error_message": words.WebApi.api_type_not_support(api_type)})
    if api_type == "2" and (options is None or "file_path" not in options):
        # xml模式下没提供file_path
        return jsonify({"status": 40002, "error_message": words.WebApi.filed_empty("file_path in options")})
    if "user_id" in options:
        userID = options["user_id"]
        del options["user_id"]

    file_path = None
    if api_type == "2":
        # 解析XML文件
        file_path = options["file_path"] if "file_path" in options else None

    if command_code == "01":
        runner = cust_vend
    elif command_code == "02":
        runner = fa
    elif command_code == "03":
        runner = invoice
    else:
        runner = other
    try:
        entry_no = runner.main(company_code=company_code, api_code=api_code, file_path=file_path,
                               p_in=options, retry=True if retry else False, userID=userID)
        res = {"status": 0, "entry_no": entry_no}
    except error.DataFieldEmptyError as ex:
        res = {"status": 50001, "error_message": str(ex)}
    except error.InvoiceEmptyError as ex:
        res = {"status": 50002, "error_message": str(ex)}
    except (error.DataLoadError, NodeNotExistError) as ex:
        res = {"status": 50003, "error_message": str(ex)}
    except error.DataLoadTimeOutError as ex:
        res = {"status": 50004, "error_message": str(ex)}
    except error.DataImportRepeatError as ex:
        res = {"status": 50005, "error_message": str(ex)}
    except Exception as ex:
        res = {"status": 50000, "error_message": str(ex)}

    return jsonify(res)


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
            entry_no = cust_vend.main(company_code=company_code, api_code=api_code, file_path=file_path,
                                      retry=True if retry else False)
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
            entry_no = fa.main(company_code=company_code, api_code=api_code, file_path=file_path,
                               retry=True if retry else False)
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
            entry_no = invoice.main(company_code=company_code, api_code=api_code, file_path=file_path,
                                    retry=True if retry else False)
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
            entry_no = other.main(company_code=company_code, api_code=api_code, file_path=file_path,
                                  retry=True if retry else False)
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
    app.run(host='0.0.0.0', threaded=True)
