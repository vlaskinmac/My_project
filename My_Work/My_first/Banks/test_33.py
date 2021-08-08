# -*- coding: utf-8 -*-
import csv
import re
import smtplib
import ssl
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version

from verify_email import verify_email

# validate = validate_email('econom@bnmotors.ru')
# print(validate)
# #
# validate = validate_email('smykchita@mail.ru', check_mx=True)
# print(validate)
import multiprocessing

from datetime import datetime
from termcolor import cprint
from validate_email import validate_email


# if is_valid == 550:
# 	print('Success')
# else:
# 	print('Bad')
# validate = validate_email('econom@bnmotors.ru', check_mx=True)
# print(validate)

# validate = validate_email('smykchita@mail.ru', verify=True)
# print(validate)
#
# validate = validate_email(email_address='econom@bnmotors.ru')
# print(validate)

# x =  get_mx_ip('bnmotors.ru')
# print(x)


# with open(mail_send, 'w', newline='', encoding='cp1251') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['ИНН', 'Email'])

# file_b = 'file_mail_send.csv'
# with open(file_b, mode='r', encoding='utf-8') as file:
#     reader = csv.DictReader(file, delimiter=";")
#     email = []
#     count_all = 0
#     for line in reader:
#         count_all += 1
#         if validate_email(line['Email']) == True:
#             email.append(str(line['Email']).lower())
#     # print(count_all, 'count_all')
# y = []
# count_1 = 0
# for i in email:
#     if i not in y:
#         y.append(i)
#         count_1 += 1
#     else:
#         del i


# print(y)
# print(count_1, 'count_1')
# email_res = re.sub(r"['|\]|\[|\b]", "", str(y))
# print(email_res)

def validate_1():
    var_path_file = 'file_base.csv'
    with open(var_path_file, mode='r') as file:
        reader = csv.DictReader(file, delimiter=";")
        # reader = csv.reader(file)
        for line in reader:
            # print(line['Email'])
            line_pre = re.findall(r'@\S*\.', str(line['Email']), flags=re.I)
            line_pre_2 = re.findall(r'\S*@', str(line['Email']), flags=re.I)
            line_domain = re.findall(r'@\S*', str(line['Email']), flags=re.I)

            yield str(line_domain)[3:-2], line['Email'].lower(), str(line_pre_2)[2:-3].lower()
            # yield line_domain, str(line_pre_2)[2:-3].lower(), str(line_pre)[3:-3].lower()


# validate_1()

def validate_2():
    # for dom, adress, befor in validate_1():
    for dom, adress, befor in validate_1():
        verivy = verify_email(adress, debug=True)
        # print(adress,'-----', verivy)
        # ------------------------------

        try:
            time.sleep(1)
            is_valid = validate_email(adress, check_mx=True, debug=True, )  # есть ли у хоста SMTP-сервер
            is_verify = validate_email(adress, verify=True, debug=True, )  # имеет ли хост SMTP Сервер и электронная
            # почта действительно существуют

            # print(adress, is_valid, 'valid')
            print(adress, '--------', is_valid, is_verify, verivy, ' -----------')

        except Exception as exc:
            print(exc)


validate_2()


def validate():
    list_valid = []
    # count_verify_check_mx = 0
    count_verify = 0
    # check_mx = 0
    for line in y:
        try:
            is_valid = validate_email(line, verify=True, check_mx=True)
            if is_valid == True:
                # count_verify_check_mx += 1
                count_verify += 1
                list_valid.append(line)
                # check_mx += 1
                print(line, '++++')
        except Exception:
            pass
    # print(count_verify_check_mx, 'count_verify_check_mx')
    print(count_verify, 'count_verify')
    # print(check_mx, 'check_mx')
    return list_valid


# print(validate())


# 52 count_verify_check_mx
# 52 count_verify
# 66 check_mx

# c = ['0opk@fortdialog.ru','nasledie.saratov@mail.ru','chiklonpenza@mail.ru','biznesstroybelgorod@yandex.ru', '2617994skolimpnn@mail.ru', 'corp@technotemp.ru']

# for i in c:
#     print(i)

bad = []


def send_email(*args):
    msg = MIMEMultipart()
    text = "ERROR: Could not find a version that satisfies the requirement." \
           " This is the mail system at host smtp-out5." \
           " I'm sorry to have to inform you that your message could not be delivered to one or " \
           "more recipients."
    subject = 'Undelivered Mail Returned to Sender'

    user = 'vlaskin@offenbach.ru'
    password = 'Vfrcvfrc11'
    sender = 'vlaskin@offenbach.ru'

    # user = 'kangelina86@mail.ru'
    # password = 'vfrcvfrc1'
    # sender = 'kangelina86@mail.ru'

    # user = 'qwertys.90@bk.ru'
    # password = '84Z-qRG-TWf-AAZ'
    # sender = 'qwertys.90@bk.ru'

    msg['Subject'] = subject
    msg['From'] = 'Mail System at Host <' + sender + '>'
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')

    msg.attach(part_text)

    context = ssl.create_default_context()

    server = smtplib.SMTP('smtp.jino.ru', 25)

    # server = smtplib.SMTP('smtp.mail.ru','25')

    server.ehlo()
    server.starttls(context=context)
    server.ehlo()

    server.login(user, password)

    count_send = 0
    no_count_send = 0
    for line in args:
        for i in line:
            try:
                server.sendmail(sender, i, msg.as_string())
                cprint(i, color='green')
            except Exception as exc:
                bad.append(i), cprint(exc, color='blue')
                bad.append(exc)
                no_count_send += 1
        count_send += 1
        print()
    print(count_send, 'count_send')
    print(no_count_send, 'no_count_send')
    print('*' * 30)
    print(bad)

    server.quit()


# send_email(c)

# send_email(validate())


# user = 'vlaskin@offenbach.ru'
# password = 'Vfrcvfrc11'
# sender = 'vlaskin@offenbach.ru'
#
#
# # user = 'kangelina86@mail.ru'
# # password = 'vfrcvfrc1'
# # sender = 'kangelina86@mail.ru'
#
# mail = imaplib.IMAP4('imap.mail.jino.ru')
# mail.login(user, password)
#
# mail.list()
# mail.select("inbox")


#     # server = 'smtp.jino.ru'
#     # user = 'vlaskin@offenbach.ru'
#     # password = 'Vfrcvfrc11'
#     sender = 'kangelina86@mail.ru'
#     user = 'kangelina86@mail.ru'
#     password = 'vfrcvfrc1'
#     server = 'smtp.mail.ru: 25'
#     # recipients = validate()
#     recipients = args
#
#     subject = 'Undelivered Mail Returned to Sender'
#     text = "ERROR: Could not find a version that satisfies the requirement." \
#            " This is the mail system at host smtp-out5." \
#            " I'm sorry to have to inform you that your message could not be delivered to one or " \
#            "more recipients."
#     msg = MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = 'Python script <' + sender + '>'
#     msg['To'] = ', '.join(recipients)
#     msg['Reply-To'] = sender
#     msg['Return-Path'] = sender
#     msg['X-Mailer'] = 'Python/' + (python_version())
#     part_text = MIMEText(text, 'plain')
#     msg.attach(part_text)
#     mail = smtplib.SMTP(server)
#     mail.login(user, password)
#     mail.sendmail(sender, recipients, msg.as_string())
#     mail.quit()
# send_email('vlaskin@offenbach.ru', 'offenbakh.debyussi@bk.ru')


def send_email(*args, **kwargs):
    msg = MIMEMultipart()
    text = "ERROR: Could not find a version that satisfies the requirement." \
           " This is the mail system at host smtp-out5." \
           " I'm sorry to have to inform you that your message could not be delivered to one or " \
           "more recipients."

    # user = 'vlaskin@offenbach.ru'
    # password = 'Vfrcvfrc11'
    # sender = 'vlaskin@offenbach.ru'

    # user = 'kangelina86@mail.ru'
    # password = 'vfrcvfrc1'
    # sender = 'kangelina86@mail.ru'

    user = 'qwertys.90@bk.ru'
    password = '84Z-qRG-TWf-AAZ'
    sender = 'qwertys.90@bk.ru'

    server = smtplib.SMTP('smtp.mail.ru: 25')
    # server = smtplib.SMTP('smtp.jino.ru: 587')

    # recipients = validate()

    msg.attach(MIMEText(text, 'plain'))

    server.starttls()
    server.login(user, password)

    recipients = args
    for i in recipients:
        # subject = 'Undelivered Mail Returned to Sender'

        server.sendmail(sender, i, msg.as_string())

    # msg['Subject'] = subject
    # msg['From'] = 'Python script <' + sender + '>'
    # msg['To'] = ', '.join(recipients)
    # msg['Reply-To'] = sender
    # msg['Return-Path'] = sender
    # msg['X-Mailer'] = 'Python/' + (python_version())
    # part_text = MIMEText(text, 'plain')
    # msg.attach(part_text)

    # mail = smtplib.SMTP(server)
    # mail.login(user, password)
    # mail.sendmail(sender, recipients, msg.as_string())
    server.quit()


# send_email('kangelina86@mail.ru', 'garant.nikolaev.1982@mail.ru', 'vlaskin@offenbach.ru')


# # x= time()
# # print(x)
# start_date_pre = datetime.now().strftime('%d.%m.%Y')
# # print(start_date_pre)
# # start_search_date = start_search_delta.strftime('%d.%m.%Y')
#
# now = datetime.now()
# future = timedelta(minutes = 1)
# res = now + future
# # print(res)
#
# def xx():
#     print(datetime.now())
# x = '2021-05-29 12:05:00'
#
# vv = datetime.strptime(x,"%Y-%m-%d %H:%M:%S")
# print(vv)


# timer_1 = threading.Timer(3.0, xx)
# timer_1.start()
# timer_1.join()
#
# timer_2 = threading.Timer(3.0, xx)
# timer_2.start()
# timer_2.join()
#
# timer_3 = threading.Timer(3.0, xx)
# timer_3.start()
# timer_3.join()
#
# timer_4 = threading.Timer(3.0, xx)
# timer_4.start()
# timer_4.join()
#
# timer_5 = threading.Timer(3.0, xx)
# timer_5.start()
# timer_5.join()


# t=1
# for i, v in e.items():
# print(v['cost'])

# print(f"{t}", v['bank']['tid'], v['bank']['name'],v['cost'], sep= ': ')
# t+=1
# print(v['bank']['name'])


# get_all_note = soup.select('/html[1]/body[1]/div[8]/div[2]/ul[1]/li[2]/div[1]/div[2]/span[1]/img[1]')
# 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKwAAAAeBAMAAABDHeiVAAAAG1BMVEXw8PCnQWXdxM3CgpmwVna5bIfUrrvm2t7LmKosv+lwAAAC5klEQVRIie2Vz2/aMBTHX0iCc8RgE45EbNOOsKzqjrilKkdcirpjkFr1CqKVeoSp1fZn771nJ0RlWqetO20+BPvZ/vj9+NoA/G//dltuIWz/IUO8/9h/ZlrPIEp9f2B0gT83Rn11ho1RxwBNiQ0nEsvTB21j5MFErL+ZreveyzOrAa7lwqoVGRry9KPsQ6IWiwW6Y7Xt/IDakJ9vD62Pcup72TEIPOJNAcLOyBB1MUljSFySQr0SdnsIWL+QQ0HosVva4i8OMEM+9+vUWZ63UfFzbEnCFowrbAtCl/vlEPwJ0eytnK7A9jEDGqTfaqRU+POoLtz+WNawHD3shvSNuwyLW86GXiU9xk7VkTx353Qbuml1n7D5EWLvcKpg7LKG3W0pGwPNJRPmYqPZYQ4W9za5ZhHW8V5DgPYgTTp2bvB8UCAQi9nPUsKKiamowiAvk8qna8PCipTUqDgfM2F7vDKkYGahPEEJrkBowuIXwh5hw/YeS2HD5sh02Fu41rgHwrO5Rf9qWMrwaEuDURGSGG0BjQ5hKUtNTdhsuMd6AYkRlyxR/QfpLLu0jk1d+jE0CeQzDZo9woZ0dRhrVhU27tW9ZrXdtUtDLbepE8Zyi2PG4iDpEjbWeZ5/QiwOK2yldldxUqQDQdKpK8F7ux7HbWcivaTsLfuDWJRUia2c9dv3YZMhYz3tc1tgVVDZvAAFRMVXdLzDYmweK2xRYnkje+vXoVtBWt6+CG0Ci9/o4ftHGQbTJ4cR25Bc7OAEl3jsnQvgS1WyDGWQteEdGWaQoIJcliKUXUxOTixCdlc0RaGxbq8AbiG4PK+wVk0mkykYnfsXLJFzujJLtTB0P/AFcxmJOio35xQ7jUM5x8ETdgl7LxcGIyO9l1gnjsGlPPPZGBj1AeDBG/CSupJGrRt6EzAnHB8P7LHDwhMtDui8vW5/rfnbXOu8Sqv+TrLhX8GSAl8f29SvSS2xuU1fWPhb2NHp6sWl3wHVJn66vqIZRQAAAABJRU5ErkJggg=='
# from lxml import html
# import requests
# #
# page = requests.get('http://derzhava.online/#calc01')
# tree = html.fromstring(page.content)
# #This will create a list of buyers:
# buyers = tree.xpath('/html[1]/body[1]/div[8]/div[2]/ul[1]/li[2]/div[1]/div[2]/span[1]/img[1]')
# # #This will create a list of prices


# print('Buyers: ', buyers)


#
# print(get_all_note)

