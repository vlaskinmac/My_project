# -*- coding: utf-8 -*-
import psycopg2
from psycopg2 import Error
from datetime import datetime
from pprint import pprint
import os
import time
from random import random
import requests
from bs4 import BeautifulSoup
import json
import re
from requests.exceptions import InvalidSchema
from selenium import webdriver
import csv
from termcolor import cprint
import datetime

# from My_Work.My_first.test_3 import get_tender_number_code, all_links


# TODO  Выполнение SQL-запроса для вставки данных в таблицу
# '%Y.%m.%d'
# start_search_delta = '06.05.2021'
# start_search_date = datetime.datetime.strptime(start_search_delta, '%d.%m.%Y')
# start_search_date.date()
g = '11.22'
# g = float(get_sum_bg)
if not g.isalpha():
    print(g)
else:
    print('000')

#        cursor.execute("INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s, %s, %s)", (count, x,
# #                                                                                          y))
# cursor.execute(insert_query)
# # connection.commit()
# # print("1 запись успешно вставлена")
#
# # cursor.execute("SELECT PRICE from mobile")
# # TODO Получить результат записи
# # record = cursor.fetchall()
# # print("Результат", record)
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")
#
#
#
#
#
#
# try:
#     count = 1
#     for item in all_links:
#         count += 1
#         cursor.execute("INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s, %s, %s)",([item['price_tender'], item['price_contract'], item['demping'], item['sum_bg'],
#                          item['tender_winner'], item['inn'], item['phone'], item['time_zone'], item['email'],
#                          item['status_contract'], item['tender_number'], item['link_tender'],
#                          item['date_pre_contract'], item['date_winner_protokol'], item['data_tender']])
# except Exception:
#     pass
# with open('mail_send.json', 'w', encoding='utf-8') as file:
#     json.dump(pre_mail_send, file, indent=4, ensure_ascii=False)
# with open('mail_send.json', encoding='utf-8') as file:
#     pre_mail_send_json = json.load(file)
#
# pre_mail_sends = []
#
#
# def mail_send_f():
#     global vow
#     for k, v in pre_mail_send_json.items():
#         y = [k]
#         for i in v:
#             mail_send_d = dict.fromkeys(y, i)
#             # pprint(vow)
#             for k, v in mail_send_d.items():
#                 pre_mail_sends.append(
#                     {
#                         'k': k,
#                         'v': v
#                     }
#                 )
#
#     # pprint(all_links)
#
#     return pre_mail_sends
#
#
# send = mail_send_f()
# file_b = 'file_b.csv'
# with open(mail_send, 'w', newline='', encoding='cp1251') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['ИНН', 'Email'])
#     for item in pre_mail_sends:
#         writer.writerow([item['k'], item['v']])
