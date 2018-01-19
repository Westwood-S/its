#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"fetch data from Device Status Website"

import threading
import time
import socket
import json
import requests
from bs4 import BeautifulSoup
import sys
import getopt
import smtplib
from email.mime.text import MIMEText
import subprocess
import signal

ping_mode = False
mail_mode = False
CUI_mode = False
GUI_mode = False
local_mode = False
count = 0

def send_email(to: str, subject: str, text: str=None):
    _user = "375002410@qq.com"
    _pwd = "fxxswdackfaobhgd"

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

def tcplink(sock, addr, power_status, serial_number):
    
    print("Send finished")

def get_equipment_data_local(session: requests, domain_name):
    global count
    power_status = ''
    serial_number = ''

    if count % 2 == 0:
        power_status = 'On'
        serial_number = 'ABC123'
    else:
        power_status = 'Off'
        serial_number = 'ABC123'
    
    count += 1
    return power_status, serial_number

def get_equipment_data(session: requests, domain_name):
    data = session.get(url= ('http://' + domain_name))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    p_lists = soup.find_all('p')
    
    power_status = str(p_lists[0].text).split(':').pop().strip(' ')
    serial_number = str(p_lists[1].text).split(':').pop().strip(' ')

    return power_status, serial_number

def usage():
    print('-p ping mode\n\
    -m mail mode\n\
    -c CUI mode\n\
    -g GUI mode\n\
    -l local mode\n')

def main():
    "Work Function"
    print("开始运行了……")
    global ping_mode
    global mail_mode
    global CUI_mode
    global GUI_mode
    global local_mode

    try:
        opts, args = getopt.getopt(sys.argv[1:], "pmcgl", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    for o, a in opts:
        if o == "-p":
            ping_mode = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-m"):
            mail_mode = True
        elif o in ("-c"):
            CUI_mode = True
        elif o in ("-g"):
            GUI_mode = True
        elif o in ("-l"):
            local_mode = True
        else:
            assert False, "unhandled option"
     
    domain_name = ''
    sleep_time = 0
    email = ''
    config = {}

    with open("config.json", "r") as f:
        config = json.load(f)

    sleep_time = config["time"]
    email = config["email"]
    domain_name = config['domain_name']

    print("设备域名:{}".format(domain_name))
    print("采集周期:{}".format(sleep_time))
    print("发送邮箱:{}".format(email))

    if ping_mode:
        subprocess.call(['ping', domain_name, '-c', '10'])
    elif mail_mode:
        send_email(email, 'test')
    else:
        socket_1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_1.bind(('127.0.0.1', 10001))
        socket_1.listen(5)
        print ('Waiting for connection...')
        sock, addr = socket_1.accept()
        print("Connected")    
        session = requests.session()

        try:
            while True:
                if local_mode:
                    power_status, serial_number = get_equipment_data_local(session, domain_name)
                else:
                    power_status, serial_number = get_equipment_data(session, domain_name)

                if CUI_mode:
                    print(power_status)
                    print(serial_number)

                sock.send(("Power Status: " + power_status + "\n").encode())
                sock.send(("Serial Number: " + serial_number + "\n").encode())
            #threading.Thread(target=tcplink, args=(sock, addr, power_status, serial_number)).start()
                time.sleep(sleep_time)
        except BrokenPipeError:
            exit(0)
                
       
if __name__ == '__main__':
    main()
