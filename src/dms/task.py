#!/usr/bin/python
# -*- coding:utf-8 -*-
# 任务相关类
import datetime
import math

from sqlalchemy.sql.elements import and_

from src import ApiTaskSetup, db


class Task:
    api_task_setup = None

    def __init__(self, task):
        self.api_task_setup = task

    # 返回内嵌对象的属性
    @property
    def Company_Code(self):
        return self.api_task_setup.Company_Code

    @property
    def API_Code(self):
        return self.api_task_setup.API_Code

    @property
    def Task_Name(self):
        return self.api_task_setup.Task_Name

    # 读取任务配置, 返回任务列表
    @staticmethod
    def load_tasks() -> list:
        return db.session.query(ApiTaskSetup).all()

    # 获取特定任务
    @staticmethod
    def get_task(company_code, sequence) -> ApiTaskSetup:
        return db.session.query(ApiTaskSetup).filter(
            and_(ApiTaskSetup.Company_Code == company_code, ApiTaskSetup.Sequence == sequence)).first()

    # 根据间隔天数和开始时间，判断内嵌的任务是否该被执行
    def is_valid(self):
        date_is_valid = True
        # 先验证日期是否正确
        last_run_dt_str = self.api_task_setup.Last_Executed_Time

        if type(last_run_dt_str) == datetime.datetime:
            last_run_dt_str = last_run_dt_str.isoformat()
        if last_run_dt_str != "0000-00-00 00:00:00":
            # 把之前的执行时间的时分秒部分省略，只比较日期部分
            last_run_dt = datetime.datetime.fromisoformat(last_run_dt_str).strftime("%Y-%m-%d 00:00:00")
            interval_days = datetime.datetime.now() - datetime.datetime.fromisoformat(last_run_dt)
            # print(interval_days.days)
            if interval_days.days != self.api_task_setup.Recurrence_Day:
                return False

        # 日期正确的前提下验证开始时间和当前的时间间隔小于5分钟
        if date_is_valid:
            execute_time_obj = self.api_task_setup.Execute_Time
            if type(self.api_task_setup.Execute_Time) == str:
                execute_time_obj = datetime.time.fromisoformat(self.api_task_setup.Execute_Time)
            execute_dt = datetime.datetime(
                year=datetime.datetime.now().year,
                month=datetime.datetime.now().month,
                day=datetime.datetime.now().day,
                hour=execute_time_obj.hour,
                minute=execute_time_obj.minute,
                second=execute_time_obj.second
            )
            delta = datetime.datetime.now() - execute_dt
            interval_seconds = math.fabs(delta.seconds)
            # print(execute_dt, datetime.datetime.now())
            # print(delta.seconds, interval_seconds)
            if interval_seconds/60 > 5:
                return False

        return True

    # 更新成功执行时间
    def update_execute_time(self):
        now_time = datetime.datetime.now().isoformat(timespec="milliseconds")
        db.session.query(ApiTaskSetup).filter(
            and_(ApiTaskSetup.Company_Code == self.api_task_setup.Company_Code,
                 ApiTaskSetup.Sequence == self.api_task_setup.Sequence)) \
            .update({"Last_Executed_Time": now_time})
