import argparse
import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from bin import cust_vend, fa, invoice, other
from src import UserList
from src.dms.notification import Notification
from src.dms.task import Task
from src.error import DataLoadError, DataLoadTimeOutError, DataImportRepeatError
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
            if self.current_task.API_Code.startswith("CustVendInfo"):
                self.runner = cust_vend
            elif self.current_task.API_Code.startswith("FA"):
                self.runner = fa
            elif self.current_task.API_Code.startswith("Invoice"):
                self.runner = invoice
            elif self.current_task.API_Code.startswith("Other"):
                self.runner = other

            self.entry_no = self.runner.main(company_code=company_code, api_code=api_code)
            print("读取成功，Entry_No=%d" % self.entry_no)
            # 更新成功执行时间
            self.current_task.update_execute_time()

            # 执行成功
            return True

        except Exception as ex:
            print(ex)
            # 失败处理，主要读取task里的Fail_Handle字段
            if not self.retry and self.current_task.api_task_setup.Fail_Handle == 1:
                # 第一次执行失败了，且不重试
                print("任务执行失败，原因是 %s, \nFail Handle设置为1，不继续执行" % ex)
                self.retry = False
                self.notify = False
                return False
            elif not self.retry and self.current_task.api_task_setup.Fail_Handle == 4:
                # 第一次执行失败了，且不重试
                print("任务执行失败，原因是 %s, \nFail Handle设置为4，将发送提醒但不继续执行" % ex)
                self.notify = True
                self.retry = False
                self.load_error = ex
                return False
            elif not self.retry:
                # 仍然是第一次执行，失败将重试
                print("任务执行失败，原因是 %s, \nFail Handle设置不为1，将重试" % ex)
                self.retry = True
                self.notify = False
                self.run_task()

            # retry=True，表示这是第二次执行了
            if self.retry and self.current_task.api_task_setup.Fail_Handle == 3:
                # 重试后依然失败，如果Fail_Handle=3则发送提醒邮件
                self.notify = True
                self.load_error = ex
                return False

    # 发送提醒邮件
    def send_notification(self):
        if self.notify:
            print("发送提醒邮件")
            # 读取邮件列表
            notify_obj = Notification(self.current_task.Company_Code, self.current_task.API_Code)
            receivers = notify_obj.get_receiver_email()

            nids = []
            for r in receivers:
                if (isinstance(r, NotificationUser) and r.Activated) \
                        or (isinstance(r, UserList) and r.Receive_Notification):
                    email_title = ""
                    email_content = ""

                    if isinstance(self.load_error, DataLoadError):
                        email_title, email_content = notify_obj.get_notification_content(
                            type=notify_obj.TYPE_ERROR, error_msg=str(self.load_error)
                        )
                    elif isinstance(self.load_error, DataLoadTimeOutError):
                        email_title, email_content = notify_obj.get_notification_content(
                            type=notify_obj.TYPE_TIMEOUT, error_msg=str(self.load_error)
                        )
                    elif isinstance(self.load_error, DataImportRepeatError):
                        email_title, email_content = notify_obj.get_notification_content(
                            type=notify_obj.TYPE_REPEAT, error_msg=str(self.load_error)
                        )
                    elif isinstance(self.load_error, Exception):
                        email_title, email_content = notify_obj.get_notification_content(
                            type=notify_obj.TYPE_OTHER, error_msg=str(self.load_error)
                        )
                    assert email_content != ""
                    result = notify_obj.send_mail(r.Email_Address, email_title, email_content)
                    assert result
                    # 写入提醒日志
                    if result:
                        nid = notify_obj.save_notification_log(r.Email_Address, email_title, email_content)
                        assert nid is not None
                        nids.append(nid)


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
        print("命令行参数错误，请输入-h 查看帮助")
        exit(1)

    # 业务调用
    # task_list = Task.load_tasks()
    # # one_task = random.choice(task_list)
    # one_task = task_list[9]
    one_task = Task.get_task(args.company_code, args.sequence)
    handler = Handler(one_task)
    time_check = args.time_check
    if time_check and not handler.check_task():  # 检查任务的开始时间是否符合
        print("任务<%s, %s>还没到执行时间" % (one_task.Company_Code, one_task.API_Code))
    else:
        print("任务<%s, %s>开始执行" % (one_task.Company_Code, one_task.API_Code))
        res = handler.run_task()
        if not res and handler.notify:
            print("任务重试后依然失败，根据设置将发送电子邮件")
            handler.send_notification()
        elif not res and handler.retry:
            print("任务执行失败，重试后依然失败")
        elif not res:
            print("任务执行失败")
        else:
            print("任务执行成功")