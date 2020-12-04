#!/usr/bin/python
# -*- coding:utf-8 -*-
# 定时任务调度器
from gevent import monkey
monkey.patch_all()
import argparse
import os
from logging import config
import threading
import time
import logging
from bin import app
from bin.task import Handler
from src import ApiTaskSetup, words
from src.dms.task import Task

config.fileConfig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logging.conf"))


# 处理任务的线程
# @param ApiTaskSetup one_task 一个任务设置
def do(one_task: ApiTaskSetup):
    app.app_context().push()
    handler = Handler(one_task)

    try:
        print(words.RunResult.task_start(one_task.Company_Code, one_task.API_Code))
        logging.getLogger("master").info(words.RunResult.task_start(one_task.Company_Code, one_task.API_Code))
        res = handler.run_task()
        if not res and handler.notify:
            handler.send_notification()
    except Exception as ex:
        logging.getLogger(__name__).critical(ex)


if __name__ == '__main__':
    # 参数处理
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time_check', dest='time_check', type=bool, nargs="?", default=False, const=True,
                        help="是否检查时间")

    args = parser.parse_args()

    # 读取任务列表
    task_list = Task.load_tasks()
    task_can_run_list = []

    # 先判断时间，再执行任务分发
    for one_task in task_list:
        task = Task(one_task)
        if args.time_check and not task.is_valid():
            print(words.RunResult.task_not_reach_time(one_task.Company_Code, one_task.API_Code))
            logging.getLogger("master").info(words.RunResult.task_not_reach_time(one_task.Company_Code, one_task.API_Code))
        else:
            task_can_run_list.append(one_task)

    # 启用多线程做任务分发
    for one_task in task_can_run_list:
        threading_name = "%s-%s(%s)" % (one_task.Company_Code, one_task.API_Code, one_task.Sequence)
        sub = threading.Thread(target=do, name=threading_name, kwargs={"one_task": one_task})
        sub.start()
        time.sleep(0.1)
