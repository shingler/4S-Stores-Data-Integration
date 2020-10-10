#!/usr/bin/python
# -*- coding:utf-8 -*-
from src import db
from src.models.dms import NotificationUser
from src.models.log import NotificationLog
from src.models.system import SystemSetup
from src.smtp import mail


class Notification:
    company_code = ""
    api_code = ""
    smtp_config = None

    def __init__(self, company_code, api_code):
        self.company_code = company_code
        self.api_code = api_code
        self.smtp_config = self._get_smtp_setup()

    # 获取收件人
    def get_receiver_email(self):
        receivers = db.session.query(NotificationUser).filter(NotificationUser.Company_Code == self.company_code) \
            .filter(NotificationUser.Activated == True).all()
        return receivers

    # 获取提醒邮件内容
    def get_notification_content(self):
        return "测试邮件标题", "这是一封测试邮件"

    # 获取smtp设置
    def _get_smtp_setup(self):
        conf = db.session.query(SystemSetup).first()
        return conf

    # 发送邮件
    def send_mail(self, to_address, email_title, email_content):
        ret = mail(smtp_config=self.smtp_config, to_addr=to_address, email_title=email_title, email_body=email_content)
        ret = True
        return ret

    # 写入发送日志
    def save_notification_log(self, to_address, email_title, email_content):
        log = NotificationLog(
            Company_Code=self.company_code,
            API_Code=self.api_code,
            Recipients=to_address,
            Email_Title=email_title,
            Email_Content=email_content
        )
        db.session.add(log)
        db.session.flush()
        db.session.commit()
        return log.ID
