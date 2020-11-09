#!/usr/bin/python
# -*- coding:utf-8 -*-
# 提示话术定义


class Notice:
    pass


class DataImport:
    _some_field_is_empty = "{0}为空"
    _file_repeat = "请不要重复导入xml文件:{0}"
    _file_not_exist = "找不到目标xml文件：{0}"
    _load_timeout = "文件：{0} 读取超时"
    _content_is_too_big = "文件{0}的以下字段长度超过规定长度："
    _node_not_exists = "缺少必要的节点：{0}"

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
    def content_is_too_big(cls, path, keys):
        message = cls._content_is_too_big.format(path)
        for k, v in keys.items():
            message += "%s: %s, " % (k, v)
        return message

    @classmethod
    def node_not_exists(cls, nodes):
        message = cls._node_not_exists.format(','.join(nodes))
        return message


class RunResult:
    _sucess = "读取成功，Entry_No={0}"
    _fail = "任务执行失败，原因是 {0}"
    _retry = "根据设置，任务将重试"
    _send_notify = "根据设置，任务将发送提醒邮件"

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
