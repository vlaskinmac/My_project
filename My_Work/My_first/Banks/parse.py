# -*- coding: utf-8 -*-
import datetime
import json
import timedelta
import re
import clipboard as clipboard
import cv2
import psycopg2
import pytesseract
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import auth_data
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup
from termcolor import cprint
import datetime
import psycopg2
from psycopg2 import Error

HOST = 'https://zakupki.gov.ru'

file_base = 'file_base.csv'
file_mail = 'file_mail.csv'
mail_send = 'file_mail_send.csv'
pre_mail_send = {}

HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}

# start_search_delta = datetime.date.today() - datetime.timedelta(days=10)
# start_search_date = start_search_delta.strftime('%d.%m.%Y')
#
# end_search_delta = datetime.date.today() - datetime.timedelta(days=6)
# end_search_date = end_search_delta.strftime('%d.%m.%Y')
#
# recordsPerPage = 50
# start_search = start_search_date
# end_search = end_search_date
# start_price_teder = '80000000'
#
# all_links = []

start_search = datetime.date.today().strftime('%d.%m.%Y')
recordsPerPage = 50
start_price_teder = '100000'

all_links = []
url = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&' \
      f'search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_{recordsPerPage}&' \
      f'showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&priceFromGeneral={start_price_teder}&currencyIdGeneral=-1&' \
      f'updateDateFrom={start_search}&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&' \
      f'OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'


class Parser:
    # start_search_delta = datetime.date.today() - datetime.timedelta(days=10)
    # start_search_date = start_search_delta.strftime('%d.%m.%Y')

    # end_search_delta = datetime.date.today() - datetime.timedelta(days=6)
    # end_search_date = end_search_delta.strftime('%d.%m.%Y')

    def __init__(self, url=url):
        self.url = url

    def time_date(self):
        try:
            base_html_code = requests.get(self.url, headers=HEADERS)
            if base_html_code.status_code == 200:
                self.soup = BeautifulSoup(base_html_code.text, 'lxml')
        except Exception:
            print('Нет соединения')
            # блок с ссылками на закупки
        contaner_with_links = self.soup.find_all(class_='search-registry-entry-block box-shadow-search-input')
        if contaner_with_links:
            count = 0
            x = datetime.datetime.now()
            print(x, 'start')
            for item in contaner_with_links:

                count += 1
                # проверка на отмену  процедуры
                chek_error = item.find('div', class_='error')
                if not chek_error:
                    # ссылка  тендера
                    self.pre_links = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href')
                    # номер  тендера  стр
                    tender_number = item.find('div', class_='registry-entry__header-mid__number').get_text(strip=True)
                    self.res_tender_number = re.sub("\D", "", str(tender_number))
                    #         print(self.pre_links)
                    # print(count)

                    # print(self.res_tender_number)
                    try:
                        get_site_tender = requests.get(url=self.pre_links, headers=HEADERS)
                        if get_site_tender.status_code == 200:
                            self.site_tender = BeautifulSoup(get_site_tender.text, 'lxml')
                    except Exception:
                        pass
                    try:  # ссылка протокола
                        self.link_winner_protokol = HOST + \
                                                    self.site_tender.find('div',
                                                                          class_='tabsNav d-flex align-items-end').find_all(
                                                        'a')[
                                                        2].get('href')
                    except Exception:
                        pass
                    # print(self.link_winner_protokol, 'сайт протокола')
                    try:  # сайт протокола
                        get_site_winner_protokol = requests.get(url=self.link_winner_protokol, headers=HEADERS)
                        if get_site_winner_protokol.status_code == 200:
                            self.soup_winner_protokol = BeautifulSoup(get_site_winner_protokol.text, 'lxml')
                    except Exception:
                        print('Нет соединения')
                    # print(self.soup_winner_protokol)
                    try:  # дата протокола
                        self.date_protokol = self.soup_winner_protokol.find_all('span', class_='section__info')[
                            1].get_text(
                            strip=True)
                    except Exception:
                        pass

                    self.date_winner_protokol_pre = str(self.date_protokol)[:str(self.date_protokol).find('(')]
                    # print(self.date_winner_protokol_pre)
                    # дата протокола  для расчета
                    self.date_winner_protokol = datetime.datetime.strptime(self.date_winner_protokol_pre,
                                                                           '%d.%m.%Y %H:%M')
                    # print(self.date_winner_protokol)

                    # дата протокола для базы
                    self.pre_date_winner_protokol_base = self.date_protokol[:self.date_protokol.find('(')]
                    # date_winner_protokol_base = datetime.datetime.strptime(pre_date_winner_protokol_base,'%d.%m.%Y %H:%M')
                    self.date_winner_protokol_base = datetime.datetime.strptime(self.pre_date_winner_protokol_base,
                                                                                '%d.%m.%Y %H:%M').isoformat()
                    # print(date_winner_protokol_base)
                    # print(date_winner_protokol)
                    # условие по сбору протоколов за последний час
                    x = '2021-05-29 12:05:00'  # вместо х поставить: self.date_winner_protokol

                    vv = datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
                    # now = datetime.datetime.now()
                    # now = now - datetime.timedelta(hours=1) синхронизировать с временем запуска потока таймера,
                    # тут имеется ввиду что поток  запускался час назад и закончил обновление данных час назад.
                    now = vv - datetime.timedelta(hours=2)
                    # print(till_ten_hours_fifteen_minutes)
                    if self.date_winner_protokol < now:
                        print(self.link_winner_protokol, 'сайт протокола')
                        print(self.date_winner_protokol)

            y = datetime.datetime.now()
            print(y, 'finish')

    def winner(self):
        pass

    def main(self):
        self.time_date()


parser = Parser()

if __name__ == '__main__':
    parser.main()


def get_tender_number_code():
    global link_tender_number_code, date_pre_contract, get_sum_bg, winner, inn, pre_links_contracts, mail_phone_winner, \
        res_mail_phone_winner, zz, q1, soup, get_, price_contract, demping, res_demping, status_contract, \
        status_contract_check, phone, email, file_base, all_links, all_links_2, z2, phone1, z4, soup_winner_protokol, \
        item, item2, link_winner_protokol, data_tender, date_winner_protokol, total_sum_tender_winner_pre, soup_code, \
        site_tender, soup_site_contacts_winner, soup_site_contracts, email_crm, time_zone, email_crm_1, email_crm_2, \
        email_crm_3, email_crm_4, email_crm_5, email_crm_7, email_crm_6, email_crm_8, email_crm_9, email_crm_10, \
        email_crm_1_0, emaill, vowels, y, pre_get_sum_bg, res_data_tender, date_winner_protokol_base

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
                try:
                    date_protokol = soup_winner_protokol.find_all('span', class_='section__info')[1].get_text(
                        strip=True)
                    date_winner_protokol = re.split('\s+', str(date_protokol))[0]
                    # print(date_winner_protokol)
                    # даты протокола и договора
                    date_winner_protokol = datetime.datetime.strptime(date_winner_protokol, '%d.%m.%Y')
                    date_winner_protokol = date_winner_protokol.date()
                    # дата протокола для базы
                    pre_date_winner_protokol_base = date_protokol[:date_protokol.find('(')]
                    # date_winner_protokol_base = datetime.datetime.strptime(pre_date_winner_protokol_base,'%d.%m.%Y %H:%M')
                    date_winner_protokol_base = datetime.datetime.strptime(pre_date_winner_protokol_base,
                                                                           '%d.%m.%Y %H:%M').isoformat()
                    # print(date_winner_protokol_base)
                #
                except Exception:
                    pass
                try:  # статус процедуры
                    status_contract_check = soup_code.find('span', class_='cardMainInfo__state').get_text(strip=True)
                    if status_contract_check == 'Подписание поставщиком':
                        status_contract = status_contract_check
                except Exception:
                    pass
                # _________________________________________________________________
                try:  # чаовой пояс
                    time_zone = soup_code.find('div', class_='time-zone__value').get_text(strip=True)
                except Exception:
                    pass
                try:
                    # даты протокола и договора
                    date_pre_contract = datetime.datetime.strptime(date_pre_contract, '%d.%m.%Y')
                    date_pre_contract = date_pre_contract.date()
                except Exception:
                    pass
                iteration += 1
                # убрать условие статуса процедуры
                if date_pre_contract and status_contract_check == 'Подписание поставщиком':
                    if date_pre_contract > date_winner_protokol:
                        # проверяем наличие инн и поля
                        try:
                            inn = soup_code.find_all('span', class_='section__info')[15].get_text(strip=True)
                            x = re.sub("\D", "", str(inn))
                            if not x.isdigit():
                                inn = soup_code.find_all('span', class_='section__info')[16].get_text(strip=True)
                                inn = int(inn)
                        except Exception:
                            pass
                        try:  # победитель
                            winner = soup_code.find_all('span', class_='section__info')[14].get_text(strip=True)
                            if len(re.findall('\D+', str(winner))) < 16:
                                winner = soup_code.find_all('span', class_='section__info')[15].get_text(strip=True)
                            try:  # победитель
                                winner = soup_code.find_all('span', class_='section__info')[14].get_text(strip=True)
                            except Exception:
                                pass
                        except Exception:
                            pass
                        try:  # цена заключаемого контракта
                            price_contract = soup_code.find('span', class_='cardMainInfo__content cost').get_text(
                                strip=True).replace('\xa0', ' ', ).replace('\u20bd', ' ').replace('\r', '').replace(
                                '\n', '').replace(' ', '').replace(',', '.')
                            price_contract = float(price_contract)
                            count += 1
                        except Exception:
                            pass
                        try:  # демпинг
                            # sum_contract = re.sub(r"[\D+]", "", str(price_contract))
                            # nmck = re.sub(r"[\D+]", "", str(total_sum_tender_winner_pre))
                            # sum_contract = re.findall(r"\d+", str(price_contract))
                            # nmck = re.findall(r"\d+", str(total_sum_tender_winner_pre))
                            # x_contract_1 = sum_contract.replace(',', '.').replace('', '')
                            # x_contract = float(x_contract_1)
                            # nmck_1 = nmck.replace(',', '.').replace('', '')
                            # y_nmck = float(nmck_1)
                            res_demping = (100 - ((price_contract / total_sum_tender_winner_pre) * 100))
                            demping = round(res_demping, 2)
                        except Exception:
                            pass
                        try:  # сумма бг  числа или %
                            pre_get_sum_bg = \
                                site_tender.find_all(class_='row blockInfo')[10].find_all(class_='section__info')[
                                    1].get_text().replace('\r', '').replace('\n', '').replace(' ', '').replace(',', '.')
                            x = pre_get_sum_bg
                            get_sum_bg_1 = x[:x.find('₽')]
                            pre_get_sum_bg_2 = re.findall('\d+', str(get_sum_bg_1))
                            y = re.sub(r"['|\"|\s|\]|\[|\b|(|)\.]", "", str(pre_get_sum_bg_2))
                            if len(re.findall('\d', str(y))) > 8:
                                # print(y, 'oioi')
                                y_2 = y.split(",")[:3]
                                y_3 = ''.join(y_2)
                                # print(y_3, 'uuuuuuuu')
                                get_sum_bg = float(y_3)
                            elif len(re.findall('\d', str(y))) < 9:
                                y_2 = y.split(",")[:2]
                                y_3 = ''.join(y_2)
                                # print(y_3, 'eeeeee')
                                get_sum_bg = float(y_3)
                            if len(re.findall('\D+', str(y))) > 4:
                                pre_get_sum_bg = \
                                    site_tender.find_all(class_='row blockInfo')[11].find_all(class_='section__info')[
                                        1].get_text().replace('\r', '').replace('\n', '').replace(' ', '').replace(
                                        ',', '.')
                                x = pre_get_sum_bg
                                get_sum_bg_1 = x[:x.find('₽')]
                                pre_get_sum_bg_2 = re.findall('\d+', str(get_sum_bg_1))
                                y = re.sub(r"['|\"|\s|\]|\[|\b|(|)\.]", "", str(pre_get_sum_bg_2))
                                if len(re.findall('\d', str(y))) > 8:
                                    # print(y, 'oioi')
                                    y_2 = y.split(",")[:3]
                                    y_3 = ''.join(y_2)
                                    # print(y_3, 'uuuuuuuu')
                                    get_sum_bg = float(y_3)
                                elif len(re.findall('\d', str(y))) < 9:
                                    y_2 = y.split(",")[:2]
                                    y_3 = ''.join(y_2)
                                    # print(y_3, 'eeeeee')
                                    get_sum_bg = float(y_3)
                        except Exception as exc:
                            try:
                                if 'list index out of range' in exc.args[0]:
                                    pre_get_sum_bg = \
                                        site_tender.find('div', class_='collapse__content collapse__content0').find_all(
                                            'div', class_='content__block blockInfo')[4].find_all(
                                            'section', class_='blockInfo__section section')[1].find(
                                            'span', class_='section__info').get_text().replace('\r', ''). \
                                            replace('\n', '').replace(' ', '').replace(',', '.')
                                    x = pre_get_sum_bg
                                    get_sum_bg_1 = x[:x.find('₽')]
                                    pre_get_sum_bg_2 = re.findall('\d+', str(get_sum_bg_1))
                                    y = re.sub(r"['|\"|\s|\]|\[|\b|(|)\.]", "", str(pre_get_sum_bg_2))
                                    if len(re.findall('\d', str(y))) > 8:
                                        # print(y, 'oioi')
                                        y_2 = y.split(",")[:3]
                                        y_3 = ''.join(y_2)
                                        # print(y_3, 'uuuuuuuu')
                                        get_sum_bg = float(y_3)
                                    elif len(re.findall('\d', str(y))) < 9:
                                        y_2 = y.split(",")[:2]
                                        y_3 = ''.join(y_2)
                                        # print(y_3, 'eeeeee')
                                        get_sum_bg = float(y_3)
                            except Exception:
                                pass
                        try:
                            try:  # дата тендера проверяем поля =\- 1
                                data_tender = \
                                    site_tender.find_all(class_='container')[7].find_all(class_='blockInfo__section')[
                                        5].find(
                                        class_='section__info').get_text(strip=True)
                                # q = re.sub(r"\d{8}", "", str(data_tender))
                                if len(re.findall('\W+', str(data_tender))) < 2 and \
                                        len(re.findall('\d+', str(data_tender))) == 8:
                                    res_data_tender = datetime.datetime.strptime(data_tender, '%d.%m.%Y')
                                    res_data_tender = res_data_tender.date()
                                elif not re.findall('@', str(data_tender)):
                                    res_data_tender = datetime.datetime.strptime(data_tender, '%d.%m.%Y')
                                    res_data_tender = res_data_tender.date()
                            except Exception:
                                data_tender = \
                                    site_tender.find_all(class_='container')[7].find_all(class_='blockInfo__section')[
                                        4].find(class_='section__info').get_text(strip=True)

                                if len(re.findall('\W+', str(data_tender))) < 2 and \
                                        len(re.findall('\d+', str(data_tender))) == 8:
                                    res_data_tender = datetime.datetime.strptime(data_tender, '%d.%m.%Y')
                                    res_data_tender = res_data_tender.date()
                                elif not re.findall('@', str(data_tender)):
                                    res_data_tender = datetime.datetime.strptime(data_tender, '%d.%m.%Y')
                                    res_data_tender = res_data_tender.date()
                        except Exception:
                            data_tender = '0000-00-00'
                        cprint(f'{iteration}', color='magenta')
                        cprint(f'Номер записи: {count}', color='cyan')
                        print(demping, '%-----снижение в ходе торгов')
                        print(price_contract, '----цена заключаемого контракта')
                        print(status_contract, '---статус  процедуры')
                        print(link_tender_number_code, 'code')
                        print(link_winner_protokol, 'сайт протокола')
                        print(date_winner_protokol_base, 'дата протокола')
                        print(date_pre_contract, 'дата проекта контракта')
                        print(get_sum_bg, 'сумма бг')
                        print(total_sum_tender_winner_pre, 'НМЦК')
                        print(res_data_tender, 'дата тендера')
                        print(winner, 'победитель')
                        print('ИНН', inn)
                        print(time_zone)
                        print('*' * 20)
                        URL_contracts = f'https://zakupki.gov.ru/epz/contract/search/results.html?morphology=on&' \
                                        f'search-filter=Дате+размещения&fz44=on&contractStageList_0=on&contractStageList_1=on&' \
                                        f'contractStageList=0%2C1&contractCurrencyID=-1&budgetLevelsIdNameHidden=%7B%7D&' \
                                        f'supplierTitle={inn}&countryRegIdNameHidden=%7B%7D&sortBy=UPDATE_DATE&pageNumber=1&' \
                                        f'sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false'
                        try:
                            get_site_contracts = requests.get(url=URL_contracts, headers=HEADERS)
                            if get_site_contracts.status_code == 200:
                                soup_site_contracts = BeautifulSoup(get_site_contracts.text, 'lxml')
                        except Exception:
                            pass
                        html_contaner_contracts = soup_site_contracts.find_all(
                            'div', class_='search-registry-entry-block box-shadow-search-input')
                        res_mail_phone_winner = []

                        for item2 in html_contaner_contracts:
                            try:
                                pre_links_contracts = HOST + item2.find('div',
                                                                        class_='registry-entry__header-mid__number').find(
                                    'a').get('href')
                            except Exception:
                                pass
                            # print(pre_links_contracts)
                            try:
                                get_site_contacts_winner = requests.get(url=pre_links_contracts, headers=HEADERS)
                                if get_site_contacts_winner.status_code == 200:
                                    soup_site_contacts_winner = BeautifulSoup(get_site_contacts_winner.text, 'lxml')
                            except Exception:
                                pass
                            try:
                                mail_phone_winner = \
                                    soup_site_contacts_winner.find('div', class_='participantsInnerHtml').find_all(
                                        'td', class_='tableBlock__col')[3].get_text(strip=True)
                                if re.findall('@', mail_phone_winner):
                                    res_mail_phone_winner.append(mail_phone_winner)
                                    # print(res_mail_phone_winner)
                                    # print(mail_phone_winner)
                                if not re.findall('@', mail_phone_winner):
                                    mail_phone_winner2 = \
                                        soup_site_contacts_winner.find('div', class_='participantsInnerHtml').find_all(
                                            'td', class_='tableBlock__col')[4].get_text(strip=True)
                                    res_mail_phone_winner.append(mail_phone_winner2)
                                    # print(res_mail_phone_winner)
                                    # print(mail_phone_winner2, '---------')
                            except Exception:
                                pass
                        # print(set(res_mail_phone_winner))
                        try:
                            t = re.sub(r"[-|(|)|+|\s]", "", str(res_mail_phone_winner))
                            q = re.sub(r"\d{11}", "", str(t))
                            emaill = re.sub(r"['|''|\s|\]|\[|\b]", "", str(q))
                            email = emaill.split(',')
                            # отбираем email
                            y = []
                            for i in email:
                                if i not in y:
                                    y.append(i)
                                else:
                                    del i
                                email = re.sub(r"['|\]|\[|\b]", "", str(y))
                            # print(email)
                        except Exception:
                            pass
                        print(email)
                        try:
                            t = re.sub(r"[-|(|)|+|\s]", "", str(res_mail_phone_winner))
                            z = re.compile('\d{11}').findall(str(t))
                            phone_1 = set(z)
                            # phone_2 = re.sub(r"['|}|{|+|\s]", "", str(phone_1))
                            # print(phone_1)
                            phone_3 = []
                            x = re.findall("'89'*?\d+", str(phone_1))
                            phone_3.append(x)
                            y = re.findall("'7'*?\d+", str(phone_1))
                            phone_3.append(y)
                            # phone_3 = str(phone_3).replace(',', '')
                            phone = re.sub(r"[\]|\[|\"|'|}|{|+|\t|\r|\n|\s]", "", str(phone_3))
                            # phone = phone.replace(',', '')
                            print(phone)
                        except Exception:
                            pass
                        # print(phone)
                        # для json собираем mail
                        inn_2 = [inn]
                        pre_mail_send.update(dict.fromkeys(inn_2, email))
                        all_links.append(
                            {
                                'link_tender': HOST + item.find(
                                    class_='registry-entry__header-mid__number').find(
                                    'a').get('href'),
                                'tender_number': item.find('div', class_='registry-entry__header-mid__number').
                                    get_text(strip=True),
                                'demping': demping,
                                'price_contract': price_contract,
                                'status_contract': status_contract,
                                'price_tender': total_sum_tender_winner_pre,
                                'sum_bg': get_sum_bg,
                                'data_tender': res_data_tender,
                                'tender_winner': winner,
                                'date_winner_protokol': date_winner_protokol_base,
                                'date_pre_contract': date_pre_contract,
                                'inn': inn,
                                'phone': phone,
                                'email': email,
                                'time_zone': time_zone

                            }
                        )

            pagina += 1

    return all_links, pre_mail_send

# get_tender_number_code()
# print(pre_mail_send)
# ----------------------------------------------------------
# try:
#     # TODO запись в базу данных 'database_parse'
#     connection = psycopg2.connect(user="postgres",
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="database_parse")
#
#     cursor = connection.cursor()
#     count = 1
#     for item in all_links:
#         cursor.execute("INSERT INTO lids (НМЦК, Сумма_контракта, Снижение, Сумма_Бг, Победитель, ИНН,"
#                        " Телефон, Часовой_пояс, Email, Статус_Тендера, Номер_тендера, Ссылка, "
#                        "Дата_контракта_ЕИС, Дата_протокола, Дата_тендера) VALUES (%s, %s, %s, %s, %s, %s, "
#                        "%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                        (item['price_tender'], item['price_contract'], item['demping'], item['sum_bg'],
#                         item['tender_winner'], item['inn'], item['phone'], item['time_zone'], item['email'],
#                         item['status_contract'], item['tender_number'], item['link_tender'],
#                         item['date_pre_contract'], item['date_winner_protokol'], item['data_tender']))
#         count += 1
#         connection.commit()
#     print(f'{count}', "Строк записано успешно")
# except (Exception, Error) as error:
#     print("Ошибка при работе с PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#         print("Соединение с PostgreSQL закрыто")
# ----------------------------------------------------------


# with open(file_base, 'w', newline='', encoding='cp1251') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['НМЦК', 'Сумма контракта', 'Снижение',
#                      'Сумма Бг', 'Победитель', 'ИНН', 'Телефон', 'Часовой пояс', 'Email', 'Статус Тендера',
#                      'Номер тендера',
#                      'Ссылка', 'Дата контракта ЕИС', 'Дата протокола', 'Дата тендера'])
#     try:
#         for item in all_links:
#             writer.writerow([item['price_tender'], item['price_contract'], item['demping'], item['sum_bg'],
#                              item['tender_winner'], item['inn'], item['phone'], item['time_zone'], item['email'],
#                              item['status_contract'], item['tender_number'], item['link_tender'],
#                              item['date_pre_contract'], item['date_winner_protokol'], item['data_tender']])
#     except Exception:
#         pass
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
