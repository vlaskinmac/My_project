# -*- coding: utf-8 -*-
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import json
import re
import html
from requests.exceptions import InvalidSchema
from selenium import webdriver
import csv

file_b = 'file_b.csv'

with open('nok_in_year.json', encoding='utf-8') as file:
    vowels_1 = json.load(file)
    # pprint(vowels_1)

all_links = []


#
def tt():
    global vow
    for k, v in vowels_1.items():
        y = [k]
        for i in v:
            vow = dict.fromkeys(y, i)
            # pprint(vow)
            for k, v in vow.items():
                all_links.append(
                    {
                        'k': k,
                        'v': v
                    }
                )

    # pprint(all_links)

    return all_links


t = tt()

with open(file_b, 'w', newline='', encoding='cp1251') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['ИНН', 'Email'])
    for item in all_links:
        writer.writerow([item['k'], item['v']])

# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
#       'pageNumber=uu&sortDirection=true&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
#       'pc=on&priceFromGeneral=1000000&currencyIdGeneral=-uu&EADateFrom=01.03.2021&EADateTo=05.03.2021&' \
#       'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&' \
#       'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'



#
#
# x = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/supplier-results.html?regNumber=0875600002521000011'
# y = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/supplier-results.html?regNumber=0358300102021000006'
#
#
# reg4 = requests.get(url=x, headers=headers)
# # src2 = reg2.text
# soup4 = BeautifulSoup(reg4.text, 'lxml')


# url = 'https://zakupki.gov.ru/epz/contract/contractCard/common-info.html?reestrNumber=2662311635719000390'


# print(soup4)

# list_actions=soup4.find('script',type="text/javascript")
# print(list_actions)

# file_contract=soup4.find('span', class_='section__value').find('a').get('href')
# print(file_contract)
#
# date_contract=soup4.find_all('div', class_='section__value')[1].get_text(strip=True)
# print(date_contract)

# list_actions=soup4.find('div', class_='container').find_all('td',class_='table__cell table__cell-body')
# print(list_actions)


# with open('index.html', 'w', encoding='utf-8') as file:
#      file.write(str(soup4))
# ____________________________________
# сохраняем локальный файл html в переменную
# with open('index.html', encoding='utf-8') as file:
#     soup4 = file.read()


# response2 = requests.get(soup4, headers=headers )


# print(soup5)

# list_actions=soup5.find('script',type="text/javascript")
# print(list_actions)


# soup5 = BeautifulSoup(response.text, 'lxml')
# list_actions=soup5.find_all('td', class_="tableBlock__col")[4].get_text(strip=True)
# print(list_actions)

# ___________

# class AppleJobsScraper(object):
#     def __init__(self):
#         self.search_request = {"orderNum": '0875600002521000011'}
#
#     def scrape (self):
#         draftId = self.scrape_draftId()
#         print(draftId)
#
#     def scrape_draftId(self):
#
#         payload = {
#             "orderNum": json.dumps(self.search_request)
#         }
#         r = requests.post(
#             url = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/supplier-results.html?regNumber=0875600002521000011',
#             data = payload,
#             headers = {'X-Requested-With': 'XMLHttpRequest'
#             }
#         )
#         s = BeautifulSoup(r.text, 'lxml')
#
#         # id = {}
#         # id['draftId'] = r.s.text
#         return s.findAll(class_='blockInfo__table tableBlock')
# scraper = AppleJobsScraper()
# scraper.scrape()


# test = soup4.find(action="/epz/order/notice/rpec/search-results.html?orderNum=0875600002521000011") #.get_text(strip=True) #.find_all('td',class_='tableBlock__col') #.get_text(strip=True)
# print(test)

# time_contract_winner = soup4.find('tbody', class_='tableBlock__body').find_all_next('td', class_='tableBlock__col')[5].get_text(strip=True)
# print(time_contract_winner)

# with open('y.txt', encoding='utf-8') as file:
#     # print(file.read())

# print(soup4)
# res_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[2].
# get_text(strip=True)
# print(res_tender_winner)

# response.xpath("//div[@class='col-6']/text()").get()


#
# status_tender_winner = soup4.find('span', class_='chevronRight draftArrow') #.find_all('td', class_='tableBlock__col')[3]. \
#     # get_text(strip=True)
# print(status_tender_winner)
#
#
# sum_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
#     4].get_text(strip=True)
# print(sum_tender_winner)
#


# link_tender_winner = HOST + soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
# 3].find('a').get('href')
# print(link_tender_winner)


#
# file_contract_winner = soup5.find_all('div', class_='col-6').find('a').get('href')
# print(file_contract_winner)


#
#
# file_contract_winner = soup4.find('td', class_='tableBlock__col tableBlock__row').find('span', class_='section__value').find('a').get('href')
# print(file_contract_winner)
