#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试时间公式：CD:当天日期,CDT:当前日期时间, TDTB:当天0点,TDTE:当天24点,PDTB:前一天0点,PDTE:前一天24点
import pytest
from src.dms.setup import ParamConvert
pc = ParamConvert()


def test_CD():
    res = pc.CD
    print(res)


def test_CDT():
    res = pc.CDT
    print(res)


def test_TDTB():
    if hasattr(pc, "TDTB"):
        res = pc.__getattribute__("TDTB")
        print(res)


def test_TDTE():
    res = pc.__getattribute__("TDTE")
    print(res)


def test_PDTB():
    res = pc.__getattribute__("PDTB")
    print(res)


def test_PDTE():
    res = pc.__getattribute__("PDTE")
    print(res)
