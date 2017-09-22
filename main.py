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
config = {}
import_data = {}

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
        import_data["int_sd_updated_time"] = latest_time
        with open("data.json", "w") as f:
            json.dump(import_data, f)
        return True

def dom_sd_updated(s:requests.session):
    global dom_sd_updated_time
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_MSG_Dom_sd.asp')
    data.encoding = 'gbk'
    times = re.search(r'(\d)+/(\d+)/(\d+) (\d+):(\d+):(\d+)', data.text)
    latest_time = times.group(0)
    if dom_sd_updated_time == latest_time:
        return False
    else:
        dom_sd_updated_time = latest_time
        import_data["dom_sd_updated_time"] = latest_time
        with open("data.json", "w") as f:
            json.dump(import_data, f)
        return True

def main():
    print ("开始运行了……")
    username = ''
    password = ''
    sleep_time = 0
    email = ''
    global config
    global import_data
    global int_sd_updated_time
    global dom_sd_updated_time

    with open("config.json", "r") as f:
        config = json.load(f)
    with open("data.json", "r") as f:
        import_data = json.load(f)
    username = config["username"]
    password = config["password"]
    sleep_time = config["time"]
    email = config["email"]
    int_sd_updated_time = import_data["int_sd_updated_time"]
    dom_sd_updated_time = import_data["dom_sd_updated_time"]
    print ("用户名:{}".format(username))
    print ("密码:{}".format(password))
    print ("采集周期:{}".format(sleep_time))
    print ("发送邮箱:{}".format(email))
    print ("导入海外供求更新时间:{}".format(int_sd_updated_time))
    print ("导入本地供求更新时间:{}".format(dom_sd_updated_time))

    session = requests.session()
    payload = {'account': username, 'password': password}
    session.post(url='http://cn.its.glo-ots.cn/login.asp', data=payload)

    while True:
        if int_sd_updated(session):
            send_email(email, "海外供求更新")
        if dom_sd_updated(session):
            send_email(email, "本地求购更新")

        time.sleep(sleep_time)

if __name__ == '__main__':
    main()