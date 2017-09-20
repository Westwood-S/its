#!/usr/bin/python3
# -*- coding: utf-8 -*-
"fetch data from ITS website periodically"

import smtplib
from email.mime.text import MIMEText
import time
import re
import json
import requests

int_sd_updated_time = ''
dom_sd_updated_time = ''
news_updated_time = ''
config = {}

def send_email(to: str, subject: str, text: str=None):
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
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_MSG_Int_sd.asp')
    data.encoding = 'gbk'
    times = re.search(r'(\d)+/(\d+)/(\d+) (\d+):(\d+):(\d+)', data.text)
    latest_time = times.group(0)
    if int_sd_updated_time == latest_time:
        return False
    else:
        int_sd_updated_time = latest_time
        config["int_sd_updated_time"] = latest_time
        with open("configure.json", "w") as f:
            json.dump(config, f)
        return True

def main():
    username = 'ftcl03'
    password = 'Stl292707'
    sleep_time = 60
    email = "375002410@qq.com"
    global config
    global int_sd_updated_time
    global dom_sd_updated_time
    global news_updated_time

    with open("configure.json", "r") as f:
        config = json.load(f)
    username = config["username"]
    password = config["password"]
    sleep_time = config["time"]
    email = config["email"]
    int_sd_updated_time = config["int_sd_updated_time"]
    dom_sd_updated_time = config["dom_sd_updated_time"]
    news_updated_time = config["news_updated_time"]

    session = requests.session()
    payload = {'account': username, 'password': password}
    session.post(url='http://cn.its.glo-ots.cn/login.asp', data=payload)

    while True:
        if int_sd_updated (session):
            send_email(email, "int_sd_updated")
        time.sleep(sleep_time)

if __name__ == '__main__':
    main()