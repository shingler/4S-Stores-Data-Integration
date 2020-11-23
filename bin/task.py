import argparse
import os
import sys
import logging
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from bin import cust_vend, fa, invoice, other
from src import UserList, words
from src.dms.notification import Notification
from src.dms.task import Task
from src.models.dms import ApiTaskSetup, NotificationUser


class Handler:
    runner = None
    current_task = None
    load_error = None
    retry = False
    notify = False
    entry_no = 0

    def __init__(self, task: ApiTaskSetup):
        self.current_task = Task(task)
        self.logger = logging.getLogger(__name__)

    # 检查这个任务是否可用
    def check_task(self) -> bool:
        if self.current_task.is_valid():
            return True
        else:
            return False

    def run_task(self):
        company_code = self.current_task.Company_Code
        api_code = self.current_task.API_Code
        try:
            if self.current_task.API_Command_Code == "01":
                self.runner = cust_vend
            elif self.current_task.API_Command_Code == "02":
                self.runner = fa
            elif self.current_task.API_Command_Code == "03":
                self.runner = invoice
            elif self.current_task.API_Command_Code == "04":
                self.runner = other

            self.entry_no = self.runner.main(company_code=company_code, api_code=api_code)
            print(words.RunResult.success(self.entry_no))
            self.logger.info(words.RunResult.success(self.entry_no))
            # 更新成功执行时间
            self.current_task.update_execute_time()

            # 执行成功
            return True

        except Exception as ex:
            # 失败处理，主要读取task里的Fail_Handle字段
            if not self.retry and self.current_task.api_task_setup.Fail_Handle == 1:
                # 第一次执行失败了，且不重试
                print(words.RunResult.fail(ex))
                self.logger.error(words.RunResult.fail(ex))
                self.retry = False
                self.notify = False
                return False
            elif not self.retry and self.current_task.api_task_setup.Fail_Handle == 4:
                # 第一次执行失败了，且不重试
                print(words.RunResult.fail(ex))
                print(words.RunResult.send_notify())
                self.logger.error(words.RunResult.fail(ex))
                self.logger.info(words.RunResult.send_notify())
                self.notify = True
                self.retry = False
                self.load_error = ex
                return False
            elif not self.retry:
                # 仍然是第一次执行，失败将重试
                print(words.RunResult.fail(ex))
                print(words.RunResult.retry())
                self.logger.error(words.RunResult.fail(ex))
                self.logger.warning(words.RunResult.retry())
                self.retry = True
                self.notify = False
                self.run_task()

            # retry=True，表示这是第二次执行了
            if self.retry and self.current_task.api_task_setup.Fail_Handle == 3:
                # 重试后依然失败，如果Fail_Handle=3则发送提醒邮件
                print(words.RunResult.fail(ex))
                print(words.RunResult.send_notify())
                self.logger.error(words.RunResult.fail(ex))
                self.logger.info(words.RunResult.send_notify())
                self.notify = True
                self.load_error = ex
                return False

    # 发送提醒邮件
    def send_notification(self):
        if self.notify:
            # print("发送提醒邮件")
            # 读取邮件列表
            notify_obj = Notification(self.current_task.Company_Code, self.current_task.API_Code)
            receivers = notify_obj.get_receiver_email()

            for r in receivers:
                if (isinstance(r, NotificationUser) and r.Activated) \
                        or (isinstance(r, UserList) and r.Receive_Notification):
                    notify_obj.add_receiver(r.Email_Address)

            email_title, email_content = notify_obj.get_notification_content(self.current_task.Task_Name,
                                                                             self.current_task.Company_Code,
                                                                             self.current_task.API_Code,
                                                                             error_message=self.load_error)

            result = notify_obj.send_mail(email_title, email_content)
            # print(result)
            # 写入提醒日志
            if result:
                notify_obj.save_notification_log(",".join(notify_obj.receivers), email_title, email_content)


if __name__ == '__main__':
    # 参数处理
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--company_code', dest='company_code', type=str, required=True, help='公司代码')
    parser.add_argument('-s', '--sequence', dest='sequence', type=str, required=True, help='任务的序号')
    parser.add_argument('-t', '--time_check', dest='time_check', type=bool, nargs="?", default=False, const=True, help="是否检查时间")
    # print(parser.parse_args())  ## 字典的方式接收参数
    # exit(1)
    
    args = parser.parse_args()
    if args.company_code is None or args.sequence is None:
        print("Command Line Error，Please add Option -h for help")
        exit(1)

    # 业务调用
    one_task = Task.get_task(args.company_code, args.sequence)
    logger = logging.getLogger(__name__)
    
    if one_task is None:
        print("there is no such a task.")
        logger.error("there is no such a task.")
        exit(1)

    handler = Handler(one_task)
    time_check = args.time_check
    if time_check and not handler.check_task():  # 检查任务的开始时间是否符合
        print(words.RunResult.task_not_reach_time(one_task.Company_Code, one_task.API_Code))
        logger.info(words.RunResult.task_not_reach_time(one_task.Company_Code, one_task.API_Code))
    else:
        print(words.RunResult.task_start(one_task.Company_Code, one_task.API_Code))
        logger.info(words.RunResult.task_start(one_task.Company_Code, one_task.API_Code))
        res = handler.run_task()
        if not res and handler.notify:
            handler.send_notification()
