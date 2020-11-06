#!/usr/bin/python
# -*- coding:utf-8 -*-
# 错误类型及错误话术定义


class DataFieldEmptyError(Exception):
    pass


class InvoiceEmptyError(Exception):
    pass


class DataLoadError(Exception):
    pass


class DataLoadTimeOutError(Exception):
    pass


class DataImportRepeatError(Exception):
    pass


class DataContentTooBig(Exception):
    pass
