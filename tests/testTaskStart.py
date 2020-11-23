#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试任务开始
import pytest

from src import ApiTaskSetup
from src.dms.task import Task


def test_task_can_run(init_app):
    one_task = Task.get_task(company_code="K302ZH", sequence=1)
    task = Task(one_task)
    assert task.is_valid() == True


def test_task_list(init_app):
    tasks = Task.load_tasks()
    for t in tasks:
        task = Task(t)
        print(task.Company_Code, task.API_Code, task.API_Command_Code, task.api_task_setup.Execute_Time)
        print(task.is_valid())
