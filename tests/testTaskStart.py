#!/usr/bin/python
# -*- coding:utf-8 -*-
# 测试任务开始
import datetime

import pytest

from src import ApiTaskSetup
from src.dms.task import Task


def test_task_can_run():
    one_task = ApiTaskSetup()

    # # 上次执行时间为空，时间不满足
    # one_task.Execute_Time = "17:00:00"
    # one_task.Recurrence_Day = 1
    # one_task.Last_Executed_Time = "0000-00-00 00:00:00"
    # task = Task(one_task)
    # assert task.is_valid() == False
    #
    # # 上次执行时间为空，时间满足
    # one_task.Execute_Time = "14:04:00"
    # one_task.Recurrence_Day = 1
    # one_task.Last_Executed_Time = "0000-00-00 00:00:00"
    # task = Task(one_task)
    # assert task.is_valid() == True
    #
    # # 上次执行时间为当天
    # one_task.Execute_Time = "17:00:00"
    # one_task.Recurrence_Day = 1
    # one_task.Last_Executed_Time = "2020-10-16 14:45:42"
    # task = Task(one_task)
    # assert task.is_valid() == False
    #
    # # 上次执行时间为前一天，时间不满足
    # one_task.Execute_Time = "18:00:00"
    # one_task.Recurrence_Day = 1
    # one_task.Last_Executed_Time = "2020-10-15 14:45:42"
    # task = Task(one_task)
    # assert task.is_valid() == False

    # 上次执行时间为前一天，时间满足
    one_task.Execute_Time = "14:21:00"
    one_task.Recurrence_Day = 1
    one_task.Last_Executed_Time = "2020-10-21 14:45:42"
    task = Task(one_task)
    assert task.is_valid() == True




