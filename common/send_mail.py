import yagmail
import os


class sendMail:
    # 发送测试报告

    def send_report(self, sender, pwd, host, receiver, attachment, sub=None, content=None):
        yag = yagmail.SMTP(user=sender, password=pwd, host=host)
        yag.send(receiver, sub, content, attachment)
