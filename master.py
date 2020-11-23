#!/usr/bin/python
# -*- coding:utf-8 -*-
# 定时任务调度器
import argparse

from gevent import monkey
monkey.patch_all()

import threading
import time
import logging
from bin import app
from bin.task import Handler
from src import ApiTaskSetup, words
from src.dms.task import Task

logging.basicConfig(filename="%s.log" % __file__, level=logging.INFO,
                    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

# 处理任务的线程
# @param ApiTaskSetup one_task 一个任务设置
# @param bool time_check 是否检查时间
def do(one_task: ApiTaskSetup, time_check=False):
    app.app_context().push()
    handler = Handler(one_task)

    if time_check and not handler.check_task():
        print(words.RunResult.task_not_reach_time(one_task.Company_Code, one_task.API_Code))
        logging.getLogger(__name__).info(words.RunResult.task_not_reach_time(one_task.Company_Code, one_task.API_Code))
    else:
        print(words.RunResult.task_start(one_task.Company_Code, one_task.API_Code))
        logging.getLogger(__name__).info(words.RunResult.task_start(one_task.Company_Code, one_task.API_Code))
        res = handler.run_task()
        if not res and handler.notify:
            handler.send_notification()


if __name__ == '__main__':
    # 参数处理
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--time_check', dest='time_check', type=bool, nargs="?", default=False, const=True,
                        help="是否检查时间")
    # print(parser.parse_args())  ## 字典的方式接收参数
    # exit(1)
    args = parser.parse_args()

    task_list = Task.load_tasks()
    for one_task in task_list:
        threading_name = "%s-%s(%s)" % (one_task.Company_Code, one_task.API_Code, one_task.Sequence)
        sub = threading.Thread(target=do, name=threading_name, kwargs={"one_task": one_task, "time_check": args.time_check})
        sub.start()
        time.sleep(0.1)
