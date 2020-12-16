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


# 按公司进行线程任务
def companyThread(company_tasks: list):
    if len(company_tasks) == 0:
        return
    for task in company_tasks:
        if task.API_Command_Code == "01":
            # CustVend必须单线程运行
            do(task.api_task_setup)
        else:
            # 其他任务根据配置选择是否多线程
            if app.config["THREADING"] == 1:
                threading_name = "thread-%s-%s-%s" % (task.Company_Code, task.API_Code, task.API_Command_Code)
                sub = threading.Thread(target=do, name=threading_name, kwargs={"one_task": task.api_task_setup})
                sub.start()
                time.sleep(0.5)
            else:
                do(task.api_task_setup)


# 单任务的执行
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
    companies_tasks = {}

    # 先判断时间，再执行任务分发
    for one_task in task_list:
        task = Task(one_task)
        if args.time_check and not task.is_valid():
            print(words.RunResult.task_not_reach_time(task.Company_Code, task.API_Code))
            logging.getLogger("master").info(words.RunResult.task_not_reach_time(task.Company_Code, task.API_Code))
        else:
            if task.Company_Code not in companies_tasks:
                companies_tasks[task.Company_Code] = []
            companies_tasks[task.Company_Code].append(task)

    # 启用多线程做任务分发
    for company_code, one_company_tasks in companies_tasks.items():
        # threading_name = "thread-%s" % company_code
        # sub = threading.Thread(target=companyThread, name=threading_name, kwargs={"company_tasks": one_company_tasks})
        # sub.start()
        # time.sleep(0.1)
        companyThread(one_company_tasks)
