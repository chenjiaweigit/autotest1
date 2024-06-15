#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import os
import smtplib
from common.set_title import getrootdirectory
from common.yaml_util1 import load_ini
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from common.tool import zip_file, locathost_ip

data_file_path = os.path.join(getrootdirectory(), 'config', 'setting.ini')
server_email = load_ini(data_file_path)["server_email"]
html_report_path = os.path.join(getrootdirectory(), 'html_report')
zip_file(html_report_path)
html_report = os.path.join(getrootdirectory(), 'html_report.zip')
locathost_ip = 'http://39.100.74.45:9090'


class Send_email:

    def __init__(self, result):
        self.sender = server_email['sender']  # 发件人邮箱账号
        self.password = server_email['password']  # 发件人邮箱密码
        self.addressee = server_email['addressee']  # 收件人邮箱账号，我这边发送给自己
        self.smtp_ssl = server_email['smtp_ssl']
        self.port = server_email['port']
        self.state = server_email['state']
        self.result = ('自动化测试报告 \n'
                       '用例总数：%d；\n'
                       '通过：%d;\n'
                       '失败：%d;\n'
                       '错误：%d;\n'
                       '跳过：%d;\n'
                       '省略：%d;\n'
                       '重试：%d;\n'
                       '总运行时间:%.3f second\n'
                       '项目报告地址：%s (该地址为局域网ip，需连接"NETGEAR"或"GAGO_IMPL"或者其他网络即可访问)'
                       % (result['用例总数'], result['通过'], result['失败'], result['错误'], result['跳过'], result['省略'],
                          result['重试'], result['总运行时间'], locathost_ip))

    def mail(self):
        ret = True
        try:
            if self.state == 'True':
                msg = MIMEMultipart()
                msg.attach(MIMEText(self.result, 'plain', 'utf-8'))
                # msg = MIMEText('自动化测试报告', 'plain', 'utf-8')
                msg['From'] = formataddr([self.sender, self.sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                msg['To'] = formataddr([self.addressee, self.addressee])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msg['Subject'] = "江苏植保自动化监控报告"  # 邮件的主题，也可以说是标题

                att1 = MIMEText(open(html_report, 'rb').read(), 'base64', 'utf-8')
                att1["Content-Type"] = 'application/octet-stream'
                # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                att1["Content-Disposition"] = 'attachment; filename="html_report.zip"'
                msg.attach(att1)

                server = smtplib.SMTP_SSL(self.smtp_ssl, self.port)  # 发件人邮箱中的SMTP服务器，端口是25
                server.login(self.sender, self.password)  # 括号中对应的是发件人邮箱账号、邮箱密码
                server.sendmail(self.sender, self.addressee.split(","), msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.quit()  # 关闭连接
                print("邮件发送成功")
            else:
                print("邮件未发送！")
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
            print("邮件发送失败，请检查配置")
        return ret


# if __name__ == '__main__':
#     Send_email(5).email_template()

    # a = 1647889583.735189 - 1647889579.7489228
    # print(a)
    # print(1647889583.735189 - 1647889579.7489228)

print(server_email['addressee'].split(","))
