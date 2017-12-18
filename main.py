#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This code is dedicated to Cecilia Shih. 

import json
import os
import sys

import requests
from bs4 import BeautifulSoup
import xlwings as xw

def get_speakforcabin_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_EXPORT_SPEAKFORCABIN.asp?contractid=%27{}%27&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')
    
    for idx, tr in enumerate(tables[8].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            info_dict['装运港口'] = tds[1].contents[0].rstrip().lstrip()
            info_dict['目的港口'] = tds[2].contents[0].rstrip().lstrip()

    for idx, tr in enumerate(tables[9].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            info_dict['英文船名'] = tds[1].contents[0].rstrip().lstrip()
            info_dict['航次'] = tds[2].contents[0].rstrip().lstrip()
            info_dict['提单号'] = tds[3].contents[0].rstrip().lstrip()
            info_dict['付费方式'] = tds[5].contents[0].rstrip().lstrip()
        
    data_dict["订舱信息"] = info_dict

    for idx, tr in enumerate(tables[10].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_list.append({'品名': tds[1].contents[0].rstrip().lstrip()})
    
    data_dict["货物信息"] = cargo_list
    
    return data_dict

def get_contractsignviewdetail_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/its_export_contractsignviewdetail.asp?contractnumber={}'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')

    trs = tables[10].find_all('tr')
    tds = trs[3].find_all('td')
    p = tds[1].find_all('p')
    info_dict['Seller'] = p[0].contents[0].rstrip().lstrip()

    tds = trs[4].find_all('td')
    p = tds[1].find_all('p')
    info_dict['Buyer'] = p[0].contents[0].rstrip().lstrip()

    for idx, tr in enumerate(tables[11].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_dict = {}
            cargo_dict['ArtNo'] = tds[0].contents[0].rstrip().lstrip()
            cargo_dict['Name'] = tds[1].contents[0].rstrip().lstrip()
            cargo_dict['Quantity'] = tds[2].contents[0].rstrip().lstrip()
            cargo_dict['Unit'] = tds[3].contents[0].rstrip().lstrip()
            cargo_dict['UnitPrice'] = tds[4].contents[0].rstrip().lstrip()
            cargo_dict['FOBNet'] = tds[5].contents[0].rstrip().lstrip()
            cargo_dict['CIFNet'] = tds[6].contents[0].rstrip().lstrip()
            cargo_list.append(cargo_dict)

    data_dict["货物信息"] = cargo_list
    data_dict['订货信息'] = info_dict
    
    return data_dict

def get_launchintoinsurance_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/its_export_launchintoinsurance.asp?contractid=%27{}%27&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')

    trs = tables[8].find_all('tr')
    tds = trs[1].find_all('td')
    info_dict['船名'] = tds[0].contents[0].rstrip().lstrip()
    info_dict['航次'] = tds[1].contents[0].rstrip().lstrip()
    info_dict['目的港口'] = tds[2].contents[0].rstrip().lstrip()
    info_dict['投保金额'] = tds[3].contents[0].rstrip().lstrip()
    info_dict['保险费'] = tds[4].contents[0].rstrip().lstrip()
    info_dict['保单号'] = tds[5].contents[0].rstrip().lstrip()

    if info_dict['保单号'] == '未办理':
        for idx, tr in enumerate(tables[10].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                cargo_dict = {}
                a = tds[0].find_all('a')            
                cargo_dict['货号'] = a[0].contents[0].rstrip().lstrip()
                cargo_dict['品名'] = tds[1].contents[0].rstrip().lstrip()
                cargo_dict['数量'] = tds[2].contents[0].rstrip().lstrip()
                cargo_dict['件数'] = tds[3].contents[0].rstrip().lstrip()
                cargo_dict['毛重'] = tds[4].contents[0].rstrip().lstrip()
                cargo_list.append(cargo_dict)
    else:
        for idx, tr in enumerate(tables[12].find_all('tr')):
            if idx != 0:
                tds = tr.find_all('td')
                cargo_dict = {}
                a = tds[0].find_all('a')            
                cargo_dict['货号'] = a[0].contents[0].rstrip().lstrip()
                cargo_dict['品名'] = tds[1].contents[0].rstrip().lstrip()
                cargo_dict['数量'] = tds[2].contents[0].rstrip().lstrip()
                cargo_dict['件数'] = tds[3].contents[0].rstrip().lstrip()
                cargo_dict['毛重'] = tds[4].contents[0].rstrip().lstrip()
                cargo_list.append(cargo_dict)

    data_dict["货物信息"] = cargo_list
    data_dict['保险信息'] = info_dict
    
    return data_dict

def get_outofstorage(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_EXPORT_OUTSTORAGE.asp?contractid={}&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')

    for idx, tr in enumerate(tables[8].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_dict = {}
            cargo_dict['货号'] = tds[0].find('p').contents[0].rstrip().lstrip()
            cargo_dict['品名'] = tds[1].find('p').contents[0].rstrip().lstrip()
            cargo_dict['包装方式'] = tds[2].find('p').contents[0].rstrip().lstrip()
            cargo_dict['出库件数'] = tds[3].find('p').contents[0].rstrip().lstrip()
            cargo_list.append(cargo_dict)
    
    data_dict["货物信息"] = cargo_list
    
    return data_dict

def get_checkandaccept_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_EXPORT_CHECKANDACCEPT.asp?contractid={}&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')

    trs = tables[8].find_all('tr')
    tds = trs[1].find_all('td')
    info_dict['目的港'] = tds[0].contents[0].rstrip().lstrip()
    info_dict['操作模式'] = tds[1].find('p').contents[0].rstrip().lstrip()
    info_dict['检验证书号码'] = tds[2].contents[0].rstrip().lstrip()
    info_dict['检验费用'] = tds[3].find('p').contents[0].rstrip().lstrip()

    for idx, tr in enumerate(tables[11].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_dict = {}
            cargo_dict['货号'] = tds[0].find('a').contents[0].rstrip().lstrip()
            cargo_dict['品名'] = tds[1].contents[0].rstrip().lstrip()
            cargo_dict['数量'] = tds[2].contents[0].rstrip().lstrip()
            cargo_dict['件数'] = tds[3].contents[0].rstrip().lstrip()
            cargo_dict['毛重'] = tds[4].contents[0].rstrip().lstrip()
            cargo_dict['尺码'] = tds[5].contents[0].rstrip().lstrip()
            cargo_list.append(cargo_dict)
    
    data_dict["货物信息"] = cargo_list
    data_dict['检验程序'] = info_dict
    
    return data_dict

def get_authentication_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_EXPORT_AUTHENTICATION.asp?contractid={}&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')

    trs = tables[8].find_all('tr')
    tds = trs[1].find_all('td')
    info_dict['目的港'] = tds[0].contents[0].rstrip().lstrip()
    info_dict['状态'] = tds[1].find('p').contents[0].rstrip().lstrip()
    info_dict['一般原产地证书'] = tds[2].find('p').contents[0].rstrip().lstrip()
    info_dict['普惠制原产地证书'] = tds[3].contents[0].rstrip().lstrip()
    info_dict['认证费用'] = tds[4].contents[0].rstrip().lstrip()

    for idx, tr in enumerate(tables[11].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_dict = {}
            cargo_dict['货号'] = tds[0].find('a').contents[0].rstrip().lstrip()
            cargo_dict['品名'] = tds[1].contents[0].rstrip().lstrip()
            cargo_dict['数量'] = tds[2].contents[0].rstrip().lstrip()
            cargo_dict['件数'] = tds[3].contents[0].rstrip().lstrip()
            cargo_dict['毛重'] = tds[4].contents[0].rstrip().lstrip()
            cargo_list.append(cargo_dict)
    
    data_dict["货物信息"] = cargo_list
    data_dict['检验程序'] = info_dict
    
    return data_dict

def get_applytocustom_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_EXPORT_APPLYTOCUSTOM.asp?contractid={}&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')
    trs = tables[8].find_all('tr')
    tds = trs[1].find_all('td')
    info_dict['提单号'] = tds[0].contents[0].rstrip().lstrip()
    info_dict['船名'] = tds[1].find('p').contents[0].rstrip().lstrip()
    info_dict['航次'] = tds[2].find('p').contents[0].rstrip().lstrip()
    info_dict['目的港'] = tds[3].contents[0].rstrip().lstrip()
    info_dict['报关费用'] = tds[4].contents[0].rstrip().lstrip()
    info_dict['放行号'] = tds[5].contents[0].rstrip().lstrip()
    info_dict['出口关税'] = tds[6].contents[0].rstrip().lstrip()

    for idx, tr in enumerate(tables[9].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_dict = {}
            cargo_dict['货号'] = tds[0].find('a').contents[0].rstrip().lstrip()
            cargo_dict['品名'] = tds[1].contents[0].rstrip().lstrip()
            cargo_dict['数量'] = tds[2].contents[0].rstrip().lstrip()
            cargo_dict['件数'] = tds[3].contents[0].rstrip().lstrip()
            cargo_dict['毛重'] = tds[4].find('p').contents[0].rstrip().lstrip()
            cargo_dict['税号'] = tds[5].find('p').contents[0].rstrip().lstrip()
            cargo_list.append(cargo_dict)
    
    data_dict["货物信息"] = cargo_list
    data_dict['履约信息'] = info_dict

    return data_dict

def get_shipment_data(s:requests.session, contract_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_EXPORT_SHIPMENT.asp?contractid={}&op=0'.format(contract_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    
    data_dict = {}
    info_dict = {}
    cargo_list = []
    tables = soup.find_all('table')

    trs = tables[8].find_all('tr')
    tds = trs[1].find_all('td')
    info_dict['提单号'] = tds[0].find('p').contents[0].rstrip().lstrip()
    info_dict['目的港'] = tds[1].find('p').contents[0].rstrip().lstrip()
    info_dict['船名'] = tds[2].contents[0].rstrip().lstrip()
    info_dict['航次'] = tds[3].contents[0].rstrip().lstrip()
    info_dict['装船日期'] = tds[4].find('p').contents[0].rstrip().lstrip()
    
    trs = tables[9].find_all('tr')
    tds = trs[1].find_all('td')
    info_dict['20FCL海洋运费'] = tds[0].find('p').contents[0].rstrip().lstrip()
    info_dict['40FCL海洋运费'] = tds[1].find('p').contents[0].rstrip().lstrip()
    info_dict['付费方式'] = tds[2].find('p').contents[0].rstrip().lstrip()
    info_dict['20FCL个数'] = tds[3].find('p').contents[0].rstrip().lstrip()
    info_dict['40FCL个数'] = tds[4].find('p').contents[0].rstrip().lstrip()

    for idx, tr in enumerate(tables[10].find_all('tr')):
        if idx != 0:
            tds = tr.find_all('td')
            cargo_dict = {}
            cargo_dict['货号'] = tds[0].find('a').contents[0].rstrip().lstrip()
            cargo_dict['品名'] = tds[1].contents[0].rstrip().lstrip()
            cargo_dict['数量'] = tds[2].contents[0].rstrip().lstrip()
            cargo_dict['件数'] = tds[3].contents[0].rstrip().lstrip()
            cargo_dict['毛重'] = tds[4].contents[0].rstrip().lstrip()
            cargo_list.append(cargo_dict)
    
    data_dict["货物信息"] = cargo_list
    data_dict['装船信息'] = info_dict

    return data_dict
 

def get_letterofcredit(s:requests.session, letter_number: str):
    global config

    data = s.get(url='http://cn.its.glo-ots.cn/ITS_LC_View.asp?ViewLCID={}'.format(letter_number))
    data.encoding = 'gbk'
    soup = BeautifulSoup(data.text, "lxml")
    data_dict = {}
    tables = soup.find_all('table')

    data_dict['ReceivedFrom'] = ''
    trs = tables[2].find_all('tr')
    tr_length = len(trs)
    for tr_idx in range(tr_length):
        if tr_idx == 0:
            tds = trs[tr_idx].find_all('td')
            data_dict['ReceivedFrom'] == tds[2].contents[0].rstrip().lstrip() + '\n'
        elif tr_idx == 1:
            tds = trs[tr_idx].find_all('td')
            data_dict['ReceivedFrom'] += tds[2].contents[0].rstrip().lstrip() + '\n'
        elif tr_idx == 2:
            tds = trs[tr_idx].find_all('td')
            data_dict['ReceivedFrom'] += tds[2].contents[0].rstrip().lstrip() + ' ' + tds[3].contents[0].rstrip().lstrip() + '\n'

    trs = tables[3].find_all('tr')
    tr_length = len(trs)
    for tr_idx in range(tr_length):
        tds = trs[tr_idx].find_all('td')
        td_length = len(tds)
        for idx in range(td_length):
            if ':50:' in tds[idx].contents[0]:
                td = trs[tr_idx+1].find_all('td')
                data_dict["Applicant"] = td[1].contents[0].rstrip().lstrip()
            if ':59:' in tds[idx].contents[0]:
                td = trs[tr_idx+1].find_all('td')
                data_dict["Beneficiary"] = td[1].contents[0].rstrip().lstrip()
            if ':44A:' in tds[idx].contents[0]:
                td = trs[tr_idx+1].find_all('td')
                data_dict["PortOfLoading"] = td[1].contents[0].rstrip().lstrip()
            if ':44B:' in tds[idx].contents[0]:
                td = trs[tr_idx+1].find_all('td')
                data_dict["PortOfDischarge"] = td[1].contents[0].rstrip().lstrip()   
            if ':20:' in tds[idx].contents[0]:
                td = trs[tr_idx+1].find_all('td')
                data_dict["LCNo"] = td[1].contents[0].rstrip().lstrip()   
            if ':32B:' in tds[idx].contents[0]:
                td = trs[tr_idx].find_all('td')
                data_dict["CurrencyCode"] = td[2].contents[0].rstrip().lstrip()
                td = trs[tr_idx + 1].find_all('td')
                data_dict['Amount'] = td[2].contents[0].rstrip().lstrip()
                td = trs[tr_idx + 2].find_all('td')
                data_dict['AmountInWords'] = td[2].contents[0].rstrip().lstrip()
            if ':31C:' in tds[idx].contents[0]:
                td = trs[tr_idx+1].find_all('td')
                data_dict["DateOfIssue"] = td[1].contents[0].rstrip().lstrip()
    return data_dict    

def write_billcn(credict_letter, checkandaccept, speakforcabin, file_path):
    wb = xw.Book(r'bl-cn.xlsx')
    ws = wb.sheets[0]

    gross_weight = 0
    measurement = 0;

    ws.range('S1').value = (speakforcabin['订舱信息']['提单号'])
    ws.range('C2').value = credict_letter['Beneficiary']
    ws.range('C7').value = 'TO ORDER'
    ws.range('C11').value = credict_letter['Applicant']
    ws.range('C18').value = speakforcabin['订舱信息']['英文船名'] + '/' + speakforcabin['订舱信息']['航次']
    ws.range('H18').value = credict_letter['PortOfLoading']
    ws.range('C20').value = credict_letter['PortOfDischarge']
    for idx, data in enumerate(checkandaccept['货物信息']):
        gross_weight += float (data['毛重'])
    ws.range('Q25').value = str(gross_weight) + 'Kgs'
    for idx, data in enumerate(checkandaccept['货物信息']):
        measurement += round (float (data['尺码']), 3)
    ws.range('T25').value = str(measurement) + 'Cbm'

    ws.range('N46').value = 'THREE (3)'
    ws.range('M48').value = 'SHANGHAI, CHINA'

    wb.save(r"./{}/bl-cn.xlsx".format(file_path))

def write_insurecn(credict_letter, checkandaccept, speakforcabin,contract_number, insure, file_path):
    wb = xw.Book(r'insure-cn.xlsx')
    ws = wb.sheets[0]

    ws.range('E8').value = str(contract_number)
    ws.range('D9').value = credict_letter['LCNo']
    ws.range('L8').value = insure['保险信息']['保单号']

    ws.range('C11').value = credict_letter['Beneficiary']
    ws.range('B22').value = 'AS PER INVOICE'

    ws.range('M35').value = speakforcabin['订舱信息']['英文船名'] + '/' + speakforcabin['订舱信息']['航次']
    ws.range('C37').value = credict_letter['PortOfLoading']
    ws.range('L37').value = credict_letter['PortOfDischarge']
    ws.range('E66').value = 'KAOHSIUNG, IN USD'

    wb.save(r"./{}/insure-cn.xlsx".format(file_path))

def write_draft(credict_letter, file_path):
    wb = xw.Book(r'draft.xlsx')
    ws = wb.sheets[0]

    ws.range('C6').value = credict_letter['CurrencyCode'] + ' ' + credict_letter['Amount']
    ws.range('F6').value = 'SHANGHAI'
    ws.range('C11').value = credict_letter['Beneficiary']
    ws.range('B14').value = credict_letter['AmountInWords']
    ws.range('C17').value = credict_letter['ReceivedFrom']
    ws.range('C19').value = credict_letter['LCNo']
    ws.range('G19').value = credict_letter['DateOfIssue']

    received_from = credict_letter['ReceivedFrom'].lstrip('\n').rstrip('\n').split('\n')
    ws.range('C22').value = received_from[0]
    ws.range('C23').value = received_from[-1]

    wb.save(r"./{}/draft.xlsx".format(file_path))

def write_cocn(credict_letter, checkandaccept, speakforcabin, insure, authentication, applytocustom, file_path):
    wb = xw.Book(r'co-cn.xlsx')
    ws = wb.sheets[0]

    measurement = 0;

    ws.range('O2').value = authentication['检验程序']['一般原产地证书']
    ws.range('B3').value = credict_letter['Beneficiary']
    ws.range('B8').value = credict_letter['Applicant']
    ws.range('B13').value = 'FROM SHANGHAI TO KAOHSIUNG, BY SEA'
    ws.range('B14').value = speakforcabin['订舱信息']['英文船名'] + '/' + speakforcabin['订舱信息']['航次']
    ws.range('B18').value = 'TAIWAN'
    ws.range('P22').value = applytocustom['货物信息'][0]['税号']
    for idx, data in enumerate(insure['货物信息']):
            measurement += int(data['数量'])
    ws.range('R22').value = str(measurement) + 'PCS'

    wb.save(r"./{}/co-cn.xlsx".format(file_path))

def write_inspectioncn(credict_letter, checkandaccept, speakforcabin, file_path):
    wb = xw.Book(r'inspection-cn.xlsx')
    ws = wb.sheets[0]

    ws.range('Q5').value = checkandaccept['检验程序']['检验证书号码']
    ws.range('D10').value = credict_letter['Beneficiary']
    ws.range('D12').value = credict_letter['Applicant']
    ws.range('E20').value = speakforcabin['订舱信息']['英文船名'] + '/' + speakforcabin['订舱信息']['航次']

    wb.save(r"./{}/inspection-cn.xlsx".format(file_path))

def write_jdwtcn(credict_letter, file_path):
    wb = xw.Book(r'jdwt-cn.xlsx')
    ws = wb.sheets[0]

    ws.range('E12').value = '上海泽川有限公司'
    ws.range('E14').value = credict_letter['Beneficiary']
    ws.range('D20').value = 'BAC10708'
    ws.range('O20').value = 'RCS10708'
    ws.range('D24').value = 'BAC10708'
    ws.range('O24').value = 'RCS10708'
    
    ws.range('C30').value = credict_letter['LCNo']
    ws.range('G30').value = credict_letter['DateOfIssue']
    ws.range('L30').value = credict_letter['CurrencyCode'] + ' ' + credict_letter['Amount']
    ws.range('O30').value = credict_letter['ReceivedFrom']

    wb.save(r"./{}/jdwt-cn.xlsx".format(file_path))
    
def main():
    print ("开始运行了……")
    username = 'ftcl03'
    password = 'Stl292707'
    concract_credit_list = []

    with open("config.json", "r") as f:
        concract_credit_list = json.load(f)
    
    print ("用户名:{}".format(username))
    print ("密码:{}".format(password))

    session = requests.session()
    payload = {'account': username, 'password': password}
    session.post(url='http://cn.its.glo-ots.cn/login.asp', data=payload)

    for idx, contract_credit_pair in enumerate(concract_credit_list):
        if not os.path.exists(contract_credit_pair['contract_number']):
            os.makedirs(contract_credit_pair['contract_number'])

        contract_number = contract_credit_pair['contract_number']
        credit_number = contract_credit_pair['credit_number']

        data_applytocustom = get_applytocustom_data(session, contract_number)
        data_authentication = get_authentication_data(session, contract_number)
        data_check_and_accept = get_checkandaccept_data(session, contract_number)
        data_contract_sign_view_detail = get_contractsignviewdetail_data(session, contract_number)
        data_insure = get_launchintoinsurance_data(session, contract_number)
        data_outofstorage = get_outofstorage(session, contract_number)
        data_shipment = get_shipment_data(session, contract_number)
        data_speak_of_cabin = get_speakforcabin_data(session, contract_number)

        data_credit = get_letterofcredit(session, credit_number)

        write_billcn(credict_letter = data_credit, checkandaccept = data_check_and_accept, speakforcabin = data_speak_of_cabin, file_path = contract_number)
        write_insurecn(credict_letter = data_credit, checkandaccept = data_check_and_accept, speakforcabin = data_speak_of_cabin, contract_number = contract_number, insure = data_insure, file_path = contract_number)
        write_draft(credict_letter = data_credit, file_path = contract_number)
        write_cocn(credict_letter = data_credit, checkandaccept = data_check_and_accept, speakforcabin = data_speak_of_cabin, insure = data_insure, authentication = data_authentication, applytocustom = data_applytocustom, file_path = contract_number)
        write_inspectioncn(credict_letter = data_credit, checkandaccept = data_check_and_accept, speakforcabin = data_speak_of_cabin, file_path = contract_number)
        write_jdwtcn(credict_letter = data_credit, file_path = contract_number)

if __name__ == '__main__':
    main()
