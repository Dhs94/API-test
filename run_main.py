import unittest
import HTMLTestRunner
from common.send_mail import sendMail
from config.read_config import *


def all_case():
    """
    加载所有用例
    """
    discover = unittest.defaultTestLoader.discover(case_path, pattern='test*.py', top_level_dir=None)
    return discover

if __name__ == '__main__':
    # 报告路径
    case_path = os.path.join(os.getcwd(), 'case')
    report_path = os.path.join(os.getcwd(), 'report\\report.html')

    with open(report_path, 'wb') as fp:
        runner = HTMLTestRunner.HTMLTestRunner(fp, title=u'WDMS接口测试报告', description=u'用例执行情况')
        runner.run(all_case())
    # 发送测试报告
    send_reports = sendMail()
    send_reports.send_report(sender, password, host, receiver, report_path, subject, content)

