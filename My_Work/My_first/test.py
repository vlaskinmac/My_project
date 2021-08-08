# -*- coding: utf-8 -*-
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import json
import re
import datetime
from requests.exceptions import InvalidSchema
from selenium import webdriver
import csv


from termcolor import cprint

HOST = 'https://zakupki.gov.ru'

file_base = 'file_base.csv'
file_mail = 'file_mail.csv'
mail_send = 'file_mail_send.csv'
pre_mail_send = {}

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}

start_search_delta = datetime.date.today() - datetime.timedelta(days=15)
start_search_date = start_search_delta.strftime('%d.%m.%Y')

end_search_delta = datetime.date.today() - datetime.timedelta(days=6)
end_search_date = end_search_delta.strftime('%d.%m.%Y')

recordsPerPage = 50
start_search = start_search_date
end_search = end_search_date
start_price_teder = '1000000'

all_links = []


def get_tender_number_code():
    global link_tender_number_code, date_pre_contract, get_sum_bg, winner, inn, pre_links_contracts, mail_phone_winner, \
        res_mail_phone_winner, zz, q1, soup, get_, price_contract, demping, res_demping, status_contract, \
        status_contract_check, phone, email, file_base, all_links, all_links_2, z2, phone1, z4, soup_winner_protokol, \
        item, item2, link_winner_protokol, data_tender, date_winner_protokol, total_sum_tender_winner_pre, soup_code, \
        site_tender, soup_site_contacts_winner, soup_site_contracts, email_crm, time_zone, email_crm_1, email_crm_2, \
        email_crm_3, email_crm_4, email_crm_5, email_crm_7, email_crm_6, email_crm_8, email_crm_9, email_crm_10, email_crm_1_0, emaill, vowels, y, pre_get_sum_bg, res_data_tender

    pagina = 1
    iteration = 0
    count = 0
    HOST = 'https://zakupki.gov.ru'
    HEADERS = {
        'Accept': '*/*', 'Sec-Fetch-Site': 'same-origin', 'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
    }

    URL2 = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
           f'pageNumber=1&sortDirection=true&recordsPerPage=_{recordsPerPage}&showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
           f'pc=on&priceFromGeneral={start_price_teder}&currencyIdGeneral=-uu&EADateFrom={start_search}&EADateTo={end_search}&' \
           f'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&' \
           f'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'
    try:
        base_html_code = requests.get(URL2, headers=HEADERS)
        if base_html_code.status_code == 200:
            soup = BeautifulSoup(base_html_code.text, 'lxml')
    except Exception:
        print('Нет соединения')

    # print(base_html_code)
    try:
        base_html_code = requests.get(URL2, headers=HEADERS)
        if base_html_code.status_code == 200:
            soup = BeautifulSoup(base_html_code.text, 'lxml')
    except Exception:
        pass
    get_all_note = soup.find('div', class_='search-results__total').get_text(strip=True)
    all_note_2 = ''.join(re.findall("\d", str(get_all_note)))
    all_note_3 = int(all_note_2)
    print('найдено тендеров', all_note_3)
    h = all_note_3 // recordsPerPage
    print('страниц всего', h)

    while int(pagina) < h:
        pagination = f'{pagina}'
        cprint(f'страница {pagina}', color='green')
        URL = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
              f'pageNumber={pagination}&sortDirection=true&recordsPerPage=_{recordsPerPage}&showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
              f'pc=on&priceFromGeneral={start_price_teder}&currencyIdGeneral=-uu&EADateFrom={start_search}&EADateTo={end_search}&' \
              f'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&' \
              f'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'
        try:
            base_html_code = requests.get(URL, headers=HEADERS)
            if base_html_code.status_code == 200:
                soup = BeautifulSoup(base_html_code.text, 'lxml')
        except Exception:
            print('Нет соединения')

        # print(base_html_code)
        contaner_with_links = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')
        if contaner_with_links:
            for item in contaner_with_links:
                pre_links = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href')
                tender_number = item.find('div', class_='registry-entry__header-mid__number').get_text(strip=True)
                res_tender_number = re.sub("\D", "", str(tender_number))
                # res_tender_number += '0001'

                for i in range(1, 2):
                    pre_links = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get(
                        'href')
                    tender_number = item.find('div', class_='registry-entry__header-mid__number').get_text(
                        strip=True)
                    res_tender_number = re.sub("\D", "", str(tender_number))
                    res_tender_number += f'000{i}'
                link_tender_number_code = HOST + f'/epz/order/notice/rpec/common-info.html?regNumber={res_tender_number}'
                # print(link_tender_number_code)
                try:
                    get_site_code = requests.get(url=link_tender_number_code, headers=HEADERS)
                    if get_site_code.status_code == 200:
                        soup_code = BeautifulSoup(get_site_code.text, 'lxml')
                except Exception:
                    pass
                # дата проекта контракта
                date_pre_contract = soup_code.find_all('span', class_='cardMainInfo__content')[3].get_text(strip=True)
                # print(date_pre_contract,'дата проекта контракта')
                try:
                    get_site_tender = requests.get(url=pre_links, headers=HEADERS)
                    if get_site_tender.status_code == 200:
                        site_tender = BeautifulSoup(get_site_tender.text, 'lxml')
                except Exception:
                    pass
                try:
                    link_winner_protokol = HOST + \
                                           site_tender.find('div', class_='tabsNav d-flex align-items-end').find_all(
                                               'a')[
                                               2].get('href')
                except Exception:
                    pass
                # print(link_winner_protokol, 'сайт протокола')
                try:
                    get_site_winner_protokol = requests.get(url=link_winner_protokol, headers=HEADERS)
                    if get_site_winner_protokol.status_code == 200:
                        soup_winner_protokol = BeautifulSoup(get_site_winner_protokol.text, 'lxml')
                except Exception:
                    print('Нет соединения')
                try:
                    total_sum_tender_winner_pre = soup_winner_protokol.find(
                        'span', class_='cardMainInfo__content cost').get_text(
                        strip=True).replace('\xa0', ' ', ).replace('\u20bd', ' ').replace('\r', '').replace(
                        '\n', '').replace(' ', '').replace(',', '.')
                    total_sum_tender_winner_pre = float(total_sum_tender_winner_pre)
                except Exception:
                    pass
                # дата протокола

                try:  # сумма бг  числа или %
                    pre_get_sum_bg = \
                        site_tender.find_all(class_='row blockInfo')[10].find_all(class_='section__info')[
                            1].get_text().replace('\r', '').replace('\n', '').replace(' ', '').replace(',', '.')
                    print(pre_get_sum_bg)
                    x = pre_get_sum_bg
                    get_sum_bg_1 = x[:x.find('₽')]
                    pre_get_sum_bg_2 = re.findall('\d+', str(get_sum_bg_1))
                    print(pre_get_sum_bg_2, 'сумма ---------')
                    y = re.sub(r"['|\"|\s|\]|\[|\b|(|)\.]", "", str(pre_get_sum_bg_2))
                    print(y, '==-=-=-')
                    # y_2 = re.sub(r"[\s]", "", str(y))
                    # print(y_2, '+++++++++')
                    if len(re.findall('\d', str(y))) > 8:
                        print(y, 'oioi')
                        tt = y.split(",")[:3]
                        t = ''.join(tt)
                        print(t, 'uuuuuuuu')
                    elif len(re.findall('\d', str(y))) < 9:
                        ttt = y.split(",")[:2]
                        q = ''.join(ttt)
                        print(q, 'eeeeee')
                    # else:
                    #     m='00'
                    #     print(m,'rfgsdf')

                    # pattern = re.sub(',00', '', str(y_2))
                    # x = re.sub("',00'$", '', str(y_2))
                    # # x = y_2.replace(',', '')
                    # print(x, '----+++')

                    # get_sum = float(x)
                    # print(get_sum, 'сумма бг')
                    # if len(re.findall('\D+', str(y))) > 4:
                    #     pre_get_sum_bg = \
                    #         site_tender.find_all(class_='row blockInfo')[11].find_all(class_='section__info')[
                    #             1].get_text().replace('\r', '').replace('\n', '').replace(' ', '').replace(
                    #             ',', '.')
                    #     x = pre_get_sum_bg
                    #     get_sum_bg_1 = x[:x.find('₽')]
                    #     pre_get_sum_bg_2 = re.findall('\d+', str(get_sum_bg_1))
                    #     y = re.sub(r"['|\"|\s|\]|\[|\b|(|)\.]", "", str(pre_get_sum_bg_2))
                    #     y_2 = re.sub(r"[\s]", "", str(y))
                    #     y_2.replace(',', '.')
                    #     get_sum_bg = float(y)
                except Exception:
                    pass
                    # try:
                    #     if 'list index out of range' in exc.args[0]:
                    #         pre_get_sum_bg = \
                    #             site_tender.find('div', class_='collapse__content collapse__content0').find_all(
                    #                 'div', class_='content__block blockInfo')[4].find_all(
                    #                 'section', class_='blockInfo__section section')[1].find(
                    #                 'span', class_='section__info').get_text().replace('\r', '').\
                    #                 replace('\n', '').replace(' ', '').replace(',', '.')
                    #         x = pre_get_sum_bg
                    #         get_sum_bg_1 = x[:x.find('₽')]
                    #         pre_get_sum_bg_2 = re.findall('\d+', str(get_sum_bg_1))
                    #         y = re.sub(r"['|\"|\s|\]|\[|\b|(|)\.]", "", str(pre_get_sum_bg_2))
                    #         y_2 = re.sub(r"[\s]", "", str(y))
                    #         y_2.replace(',', '.')
                    #         get_sum_bg = float(y)
                    #     # get_sum_bg = float(y_2)
                    # except Exception:
                    #     print('0000')

                # print(get_sum_bg, 'сумма бг')

                # print(link_winner_protokol, 'сайт протокола')


get_tender_number_code()

# HOST = 'https://zakupki.gov.ru'
#
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
#       'pageNumber=uu&sortDirection=true&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
#       'pc=on&priceFromGeneral=1000000&currencyIdGeneral=-uu&EADateFrom=01.03.2021&EADateTo=05.03.2021&' \
#       'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&' \
#       'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'
#
# headers = {
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
#               'q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                   ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
# }
#
#
# def get_data_with_seleniun(url):
#     options = webdriver.FirefoxOptions()
#     options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
#                                                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
#                                                          ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663'
#                                                          ' Yowser/2.5 Safari/537.36')
#     try:
#         driver = webdriver.Firefox(
#             executable_path='C:/Users/User/PycharmProjects/python_base/python_base/My_Work/My_first/geckodriver.exe',
#             options=options
#         )
#         driver.get(url=url)
#         time.sleep(5)
#
#         with open('index.html', 'w', encoding='utf-8') as file:
#             file.write(driver.page_source)
#
#     except Exception as exc:
#         print(exc)
#
#     finally:
#         driver.close()
#         driver.quit()
#
#
# z = 'soup4.find('
# span
# ', class_='
# chevronRight
# draftArrow
# ')'
# x = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/supplier-results.html?regNumber=0875600002521000011'
# get_data_with_seleniun(x)
# with open('index.html', encoding='utf-8') as file:
#     hendler_src3 = file.read()
#
# # reg4 = requests.get(url=hendler_src3, headers=headers)
# soup4 = BeautifulSoup(hendler_src3, 'lxml')

# print(soup4)
# res_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[2]. \
#     get_text(strip=True)
# print(res_tender_winner)
#
#
# status_tender_winner = soup4.find('div', id='searchResWrapper') #.find_all('td', class_='tableBlock__col')[3]. \
#     # get_text(strip=True)
# print(status_tender_winner)
#
#
# sum_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
#     4].get_text(strip=True)
# print(sum_tender_winner)
#
# get_data_with_seleniun(link_tender_winner)
# # reg5 = requests.get(url=link_tender_winner, headers=headers)
# with open('index.html', encoding='utf-8') as file:
#     hendler_src4 = file.read()
# soup5 = BeautifulSoup(hendler_src4, 'lxml')

# link_tender_winner = HOST + soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
# 3].find('a').get('href')
# print(link_tender_winner)


#
# file_contract_winner = soup5.find_all('div', class_='col-6').find('a').get('href')
# print(file_contract_winner)


# time_contract_winner = soup4.find('tbody', class_='tableBlock__body').find_all_next('td', class_='tableBlock__col')[
#     5].get_text(strip=True)
# print(time_contract_winner)
#
#
# file_contract_winner = soup4.find('td', class_='tableBlock__col tableBlock__row').find('span', class_='section__value').find('a').get('href')
# print(file_contract_winner)

#
# reg = requests.get(url, headers=headers)  # получаем результат запроса get т.е. ответ и сохраняем в переменную reg
# src = reg.text
# soup = BeautifulSoup(src, 'lxml')
# # pre_links1 = {}
# all_links = []
# contaner_links = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')  # контейнер отдельно
# for item in contaner_links:
#     pre_links1 = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href')
#
#     reg2 = requests.get(url=pre_links1, headers=headers)
#     src2 = reg2.text
#     soup2 = BeautifulSoup(src2, 'lxml')
#     # print(pre_links1)
#     try:
#         data_tender = soup2.find_all(class_='container')[7].find_all(class_='blockInfo__section')[5].find(
#             class_='section__info').get_text(strip=True)
#         if len(re.compile('\d+').findall(str(data_tender))) < 3:
#             raise ValueError('uuu')
#     except Exception as exc:
#         data_tender = soup2.find_all(class_='container')[7].find_all(class_='blockInfo__section')[4].find(
#             class_='section__info').get_text(strip=True)
#     try:
#         sum_bg = soup2.find_all(class_='row blockInfo')[10].find_all(class_='section__info')[1].get_text(). \
#             replace('\xa0', ' ', ).replace('\u20bd', ' ').replace('\r', '').replace('\n', '').replace(' ', '')
#     except Exception as exc:
#         if 'list index out of range' in exc.args[0]:
#             sum_bg = soup2.find('div', class_='collapse__content collapse__content0').find_all(
#                 'div', class_='content__block blockInfo')[4].find_all('section', class_='blockInfo__section section')[1].find(
#                 'span', class_='section__info').get_text(). \
#                 replace('\xa0', ' ', ).replace('\u20bd', ' ').replace('\r', '').replace('\n', '').replace(' ', '')
#
#     pre_links2 = HOST + soup2.find('div', class_='tabsNav d-flex align-items-end').find_all('a')[2].get('href')
#     # print(pre_links2)
#     reg3 = requests.get(url=pre_links2, headers=headers)
#     src3 = reg3.text
#     soup3 = BeautifulSoup(src3, 'lxml')
#     # print(soup3)
# #________________________
# x = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/supplier-results.html?regNumber=0875600002521000011'
# with open('index.html', 'r', encoding='utf-8') as file:
#     hendler_src3 = file.read()
