#!/usr/bin/python
# -*- coding:utf-8 -*-
# 利用smtp服务发送电子邮件
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


# 发送邮件
# @param dict smtp_config {"smtp_host", "smtp_port", "sender", "user_pwd"}
#         smtp配置字典。smtp_host=smtp服务地址，smtp_port=smtp服务端口号，
#         sender=发件人邮箱地址，user_pwd=发件人邮箱密码
# @param str to_addr 收件人邮箱地址
# @param str email_title 邮件标题
# @param str email_body 邮件正文
def mail(smtp_config, to_addr, email_title, email_body):
    print(smtp_config, to_addr, email_title, email_body)
    ret = True
    try:
        # 构建邮件对象
        msg = MIMEText(email_body, 'plain', 'utf-8')
        msg['From'] = formataddr(["dms_develop", smtp_config["sender"]])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", to_addr])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = email_title

        server = smtplib.SMTP_SSL(smtp_config["smtp_host"], smtp_config["smtp_port"])
        server.login(smtp_config["sender"], smtp_config["user_pwd"])
        server.sendmail(smtp_config["sender"], [to_addr, ], msg.as_string())
        # 关闭连接
        server.quit()
    except Exception:
        ret = False
    return ret


if __name__ == '__main__':
    smtp_conf = {
        "smtp_host": "smtp.163.com",
        "smtp_port": 465,
        "sender": "singlerwong@163.com",
        "user_pwd": "XJZDDLHZYACGJVWM"
    }
    ret = mail(smtp_conf, "shingler@gf-app.cn", "测试邮件标题", "测试邮件内容")
    print(ret)
