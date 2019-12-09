# coding=utf-8
import smtplib
import os
import traceback
from email.mime.text import MIMEText


def get_msg(code, name):  # 获取发送内容，传入整型验证码
    msg = ''
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(base_dir+'/message.txt', 'r', encoding='UTF-8') as f:
        for line in f:
            msg += line
        msg = msg.replace('CODE', str(code))
        if len(name) == 0:
            msg = msg.replace('NAME，', '')
        else:
            msg = msg.replace('NAME','尊敬的'+name)
        f.close()
    return msg


def send_email(code, name,mailto):  # 发送邮件方法，传入验证码和要发送邮箱的地址
    msg = MIMEText(get_msg(code,name), 'plain', 'utf-8')
    sender = 'omnisci_001@sina.com'
    password = 'omnisci001'
    mailto_list = [mailto]  # 收件人
    smtp_server = 'smtp.sina.com'
    msg['From'] = sender
    msg['To'] = ';'.join(mailto_list)  # 发送多人邮件写法
    msg['Subject'] = 'OmniSci'
    server = smtplib.SMTP(smtp_server, 587)  # SMTP协议默认端口是25
    try:
        server.login(sender, password)  # ogin()方法用来登录SMTP服务器
        server.sendmail(sender, mailto_list, msg.as_string())
        server.quit()
    except Exception:
        traceback.print_exc()
        return False
    return True
