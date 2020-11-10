#!/usr/bin/python
# -*- coding:utf-8 -*-
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.sql.elements import and_
from src import db, words
from src.models.dms import NotificationUser
from src.models.log import NotificationLog
from src.models.system import SystemSetup, UserList
from src.smtp import mail


class Notification:
    company_code = ""
    api_code = ""
    smtp_config = None

    TYPE_ERROR = 1
    TYPE_TIMEOUT = 2
    TYPE_REPEAT = 3
    TYPE_DATA_TOO_BIG = 4
    TYPE_NODE_NOT_EXISTS = 5
    TYPE_OTHER = 9

    def __init__(self, company_code, api_code):
        self.company_code = company_code
        self.api_code = api_code
        self.smtp_config = self._get_smtp_setup()

    # 获取收件人（NotificationUser和接收邮件的User）
    def get_receiver_email(self):
        receivers = db.session.query(NotificationUser).filter(
            and_(NotificationUser.Company_Code == self.company_code, NotificationUser.Activated == True)).all()
        users = db.session.query(UserList).filter(
            and_(UserList.Receive_Notification == True, not UserList.Blocked == False)).all()
        return receivers + users

    # 获取提醒邮件内容
    # @param string type 报错的数据类型
    # @param string url 报错参考访问地址
    # @return email_title, email_content
    def get_notification_content(self, type, ref_url="") -> (str, str):
        title = words.Notice.title
        content = words.Notice.content
        return title.format(type), content.format(type, ref_url)

    # 获取smtp设置
    def _get_smtp_setup(self):
        conf = None
        try:
            conf = db.session.query(SystemSetup).first()
            db.session.commit()
        except InvalidRequestError:
            db.session.rollback()
        return conf

    # 发送邮件
    def send_mail(self, to_address, email_title, email_content):
        smtp_conf = {
            "smtp_host": self.smtp_config.Email_SMTP,
            "smtp_port": self.smtp_config.SMTP_Port,
            "sender": self.smtp_config.Email_UserID,
            "user_pwd": self.smtp_config.Email_Password
        }
        ret = mail(smtp_config=smtp_conf, to_addr=to_address, email_title=email_title, email_body=email_content)
        # ret = True
        return ret

    # 写入发送日志
    def save_notification_log(self, to_address, email_title, email_content):
        log_id = 0
        try:
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
            log_id = log.ID
        except InvalidRequestError:
            db.session.rollback()
        return log_id
