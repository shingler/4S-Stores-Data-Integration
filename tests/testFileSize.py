#!/usr/bin/python
# -*- coding:utf-8 -*-
import pytest
import os

from src import words
from src.dms.setup import Setup

filename = "/Users/shingler/PycharmProjects/platform20200916/DMS_Interface/K302ZH/20201215_Other.xml"
company_code = "K302ZH"
api_code = "Other"


def test_filesize(init_app):
    filesize = 0
    try:
        filesize = os.path.getsize(filename)
    except OSError as ex:
        print("exception:", ex)
    filesize = filesize/1024/1024
    print(round(filesize, 2))
    api_setup = Setup.load_api_setup(company_code, api_code)
    if filesize > api_setup.File_Max_Size:
        print(words.DataImport.file_too_big(api_setup.File_Max_Size, round(filesize, 2)))
