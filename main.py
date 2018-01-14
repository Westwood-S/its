#!/usr/bin/python3
# -*- coding: utf-8 -*-
"fetch data from Device Status Website"

import json
import time
import requests
from bs4 import BeautifulSoup

def get_equipment_data(session: requests, domain_name):
    data = session.get(url=domain_name)
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    p_lists = soup.find_all('p')
    
    power_status = str(p_lists[0].text).split(':').pop().strip(' ')
    serial_number = str(p_lists[1].text).split(':').pop().strip(' ')

    print("电源状态: ", power_status)
    print("设备序列号: ", serial_number)

def main():
    "Work Function"
    print("开始运行了……")
     
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

    session = requests.session()

    while True:
        get_equipment_data(session, domain_name)
        time.sleep(sleep_time)
    
if __name__ == '__main__':
    main()
