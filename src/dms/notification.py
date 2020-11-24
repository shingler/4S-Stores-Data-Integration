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
    # smtp设置，读取自SystemSetup
    smtp_config = None
    # 收件人列表
    receivers = []

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

    # 增加收件人
    def add_receiver(self, email_address):
        if email_address not in self.receivers:
            self.receivers.append(email_address)

    # 获取提醒邮件内容
    # @param string data_type 报错的数据类型
    # @param string company_code
    # @param string api_code
    # @param string error_message
    # @return email_title, email_content
    def get_notification_content(self, data_type, company_code, api_code, error_message="") -> (str, str):
        title = words.Notice.title
        content = words.Notice.content
        return title.format(company_code, data_type), content.format(data_type, company_code, api_code, error_message, self.smtp_config.System_URL)

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
    def send_mail(self, email_title, email_content):
        smtp_conf = {
            "smtp_host": self.smtp_config.Email_SMTP,
            "smtp_port": self.smtp_config.SMTP_Port,
            "sender": self.smtp_config.Email_UserID,
            "sender_name": self.smtp_config.Email_SenderName,
            "user_pwd": self.smtp_config.Email_Password,
            "use_ssl": self.smtp_config.Use_SSL
        }
        ret = mail(smtp_config=smtp_conf, to_addr=self.receivers, email_title=email_title, email_body=email_content)
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
