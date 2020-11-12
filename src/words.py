#!/usr/bin/python
# -*- coding:utf-8 -*-
# 提示话术定义


# 提醒邮件话术模板
class Notice:
    # 提醒邮件标题模板
    title = 'DMS Interface Error (Data Type: {0} )'
    # 提醒邮件内容模板
    content = '''Dear User,
<p>There are some errors occurred during system import DMS <strong>{0}</strong> Interface Data, please check error log in NAV interface platform (URL:{1}).</p>
<p>If you have any questions, please contact NAV support team with Email:<a href="mailto:phnav.support@hytci.com!">phnav.support@hytci.com!</a></p>
<p>Navision system</p>'''


# 数据导入错误消息模板
class DataImport:
    _some_field_is_empty = "{0} can not be null!"
    _file_repeat = "XML file:{0} is already existing in system, can not import again! "
    _file_not_exist = "There is no XML file:{0}!"
    _load_timeout = "Timeout for reading file:{0}"
    _content_is_too_big = "The length of content (field:{0} \"{3}\" ) exceeds the max length {1} in file: {2}"
    _node_not_exists = "Node:{0} is missing!"

    @classmethod
    def field_is_empty(cls, field):
        return cls._some_field_is_empty.format(field)

    @classmethod
    def file_is_repeat(cls, file_path):
        return cls._file_repeat.format(file_path)

    @classmethod
    def file_not_exist(cls, file_path):
        return cls._file_not_exist.format(file_path)

    @classmethod
    def load_timeout(cls, file_path):
        return cls._load_timeout.format(file_path)

    @classmethod
    # @param str path 文件路径
    # @param dict cnt 内容超长的具体信息，{key=节点名, expect=预期长度, content=内容}
    def content_is_too_big(cls, path, cnt):
        return cls._content_is_too_big.format(cnt["key"], cnt["expect"], path, cnt["content"])

    @classmethod
    def node_not_exists(cls, nodes):
        message = cls._node_not_exists.format(','.join(nodes))
        return message


# 程序运行时报错消息模板
class RunResult:
    _sucess = "Operation successful, Entry No:{0}"
    _fail = "Task failed, reason is {0}"
    _retry = "According to system setting, the task will be tried again"
    _send_notify = "According to system setting, the task will send notification email"
    _task_start = "Task<%s, %s> is running"
    _task_not_reach_time = "The Time for Task<%s, %s> is not arrived"

    @classmethod
    def success(cls, entry_no):
        return cls._sucess.format(entry_no)

    @classmethod
    def fail(cls, reason):
        return cls._fail.format(reason)

    @classmethod
    def retry(cls):
        return cls._retry

    @classmethod
    def send_notify(cls):
        return cls._send_notify

    @classmethod
    def task_start(cls, company_code, api_code):
        return cls._task_start.format(company_code, api_code)

    @classmethod
    def task_not_reach_time(cls, company_code, api_code):
        return cls._task_not_reach_time.format(company_code, api_code)


# API错误提示模板
class WebApi:
    _field_empty = "{0} can not be empty!"
    _invalid_value = "the field {0} has an invalid value: {1}"
    _api_type_not_support = "the {0} is not supported"
    _other_error = "there's something wrong, please contact us."
    _method_error = "Request method is incorrect, please retry with POST"

    @classmethod
    def filed_empty(cls, field):
        return cls._field_empty.format(field)

    @classmethod
    def invalid_value(cls, key, value):
        return cls._invalid_value.format(key, value)

    @classmethod
    def api_type_not_support(cls, api_name):
        return cls._api_type_not_support.format(api_name)

    @classmethod
    def internal_error(cls):
        return cls._other_error

    @classmethod
    def method_error(cls):
        return cls._method_error
