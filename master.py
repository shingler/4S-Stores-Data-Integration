#!/usr/bin/python
# -*- coding:utf-8 -*-
# 定时任务调度器
import argparse

from gevent import monkey
monkey.patch_all()

import threading
import time

from bin import app
from bin.task import Handler
from src import ApiTaskSetup
from src.dms.task import Task


# 处理任务的线程
# @param ApiTaskSetup one_task 一个任务设置
# @param bool time_check 是否检查时间
def do(one_task: ApiTaskSetup, time_check=False):
    app.app_context().push()
    handler = Handler(one_task)

    if time_check and not handler.check_task():
        print("任务<%s, %s>还没到执行时间" % (one_task.Company_Code, one_task.API_Code))
    else:
        print("任务<%s, %s>开始执行" % (one_task.Company_Code, one_task.API_Code))
        res = handler.run_task()
        if not res and handler.notify:
            print("任务执行失败，根据设置将发送电子邮件")
            handler.send_notification()
        elif not res and handler.retry:
            print("任务执行失败，重试后依然失败")
        elif not res:
            print("任务执行失败")
        else:
            print("任务执行成功")


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
