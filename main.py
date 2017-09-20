#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
import time
import re
import requests

int_sd_updated_time = ''
dom_sd_updated_time = ''
news_updated_time = ''
ad_updated_time = ''
domestic_sales_updated_time = ''
export_updated_time = ''
export_sales_updated_time = ''
exchange_rate = {"AUD":0,
"CHF":0,
"EUR":0,
"HKD":0,
"MOP":0,
"NZD":0,
"SEK":0,
"THB":0,
"CAD":0,
"DMK":0,
"GBP":0,
"JPY":0,
"NOK":0,
"PHP":0,
"SGD":0,
"USD":0
}


def send_email(to:str, subject:str, text:str=None):
    _user = "375002410@qq.com"
    _pwd = "vqfsdpjaaxeobhji"

    if text:
        msg = MIMEText(text)
    else:
        msg = MIMEText("")
    msg["Subject"] = subject
    msg["From"] = _user
    msg["To"] = to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, to, msg.as_string())
        s.quit()
    except smtplib.SMTPException:
        print("send email faild, {}".format(smtplib.SMTPException))

def int_sd_updated(s:requests.session):
    global int_sd_updated_time

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_MSG_Int_sd.asp')
    data.encoding = 'gbk'
    times = re.search(r'(\d)+/(\d+)/(\d+) (\d+):(\d+):(\d+)', data.text)
    latest_time = times.group(0)
    if int_sd_updated_time == latest_time:
        return False
    else:
        int_sd_updated_time = latest_time
        return True

def main():
    username = 'ftcl03'
    password = 'Stl292707'
    session = requests.session()
    payload = {'account': username, 'password': password}
    session.post(url='http://cn.its.glo-ots.cn/login.asp', data=payload)

    while True:
        if int_sd_updated (session):
            send_email("375002410@qq.com", "int_sd_updated")
        time.sleep(5)

if __name__ == '__main__':
    main()