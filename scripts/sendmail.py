#!/usr/bin/python3
#
# 当服务器 IP 变更时，给用户发送邮件。
# NOTE：
# - 使用 SMTP 发送邮件，密码可能时邮件服务商的授权码。
# - 假设只有一个 IP。

from urllib import request
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import socket
import os

mail_host="smtp.qq.com"  #邮件发件服务器，建议 QQ 邮箱
mail_user="sender@qq.com"    #用户名(你的邮件地址）
mail_pass="password"   #邮箱密码（授权码）
sender = 'sender@qq.com'        #和上面的用户名一致
receivers = ['reveiver@outlook.com']  # 接收邮箱

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        return ip


def sendmail(host_ip):
    message = MIMEText('公网IP是: ' + host_ip, 'plain', 'utf-8') #正文
    message['From'] = Header('服务器邮件', 'utf-8') #发件人显示的名字
    message['To'] =  Header("Kong Jun", 'utf-8')        #接收人显示的名字
    message['Subject'] = Header('公网IP通知', 'utf-8') #标题
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")

host_ip=get_host_ip()
cache_dir=os.environ["HOME"] + "/.local/cache"
host_ip_file=cache_dir + "/host-ip"
old_host_ip=""

print("Host IP address: " + host_ip)

if not os.path.exists(host_ip_file):
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    f = open(host_ip_file, "w")
    f.close()

f = open(host_ip_file, "r+")
old_host_ip = f.read()
if host_ip != old_host_ip:
    print("IP address changes: sending email...")
    sendmail(host_ip)
    f.write(host_ip)
