# -*- coding: utf-8 -*-
import csv
import json
import logging
import re
import zipfile
import random
import datetime
import fitz
import psycopg2
from psycopg2 import Error
import pytesseract
from selenium import webdriver
import os
import time
import requests
from bs4 import BeautifulSoup

import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from termcolor import cprint

# from My_Work.My_first.Banks.get_inn import caching
# import test_dx
# from test_dx import delete_file
# import parsePdf


HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}

# url = 'https://synapsenet.ru/searchorganization/organization/1135920001645-ooo-avtosnab'
HOST = 'https://zakupki.gov.ru'

# url = 'https://www.google.ru/search?q=ОБЩЕСТВО+С+ОГРАНИЧЕННОЙ+ОТВЕТСТВЕННОСТЬЮ+%22УРАЛБИЗНЕСЛИЗИНГ%22&newwindow=1&sxsrf=ALeKk03vi5QhOwjlrgZXiBKHOhPytiKL1A%3A1625074885034&source=hp&ei=xKzcYMa0O5C1sAfu34mIBg&iflsig=AINFCbYAAAAAYNy61Vhg0FavwWOja_CyxjeJXbDLsgpz&oq=ОБЩЕСТВО+С+ОГРАНИЧЕННОЙ+ОТВЕТСТВЕННОСТЬЮ+%22УРАЛБИЗНЕСЛИЗИНГ%22&gs_lcp=Cgdnd3Mtd2l6EAMyBggAEBYQHlDL8AFYy_ABYJT0AWgAcAB4AIABT4gBT5IBATGYAQCgAQKgAQGqAQdnd3Mtd2l6&sclient=gws-wiz&ved=0ahUKEwjGpoLa87_xAhWQGuwKHe5vAmEQ4dUDCAc&uact=5'
# url = 'https://yandex.ru/search/?text=ОБЩЕСТВО%20С%20ОГРАНИЧЕННОЙ%20ОТВЕТСТВЕННОСТЬЮ%20%22УРАЛБИЗНЕСЛИЗИНГ%22&lr=118655&clid=2270455&win=456'
# url = 'https://nova.rambler.ru/search?utm_source=head&utm_campaign=self_promo&utm_medium=form&utm_content=search&query=реквизиты%20ОБЩЕСТВО%20С%20ОГРАНИЧЕННОЙ%20ОТВЕТСТВЕННОСТЬЮ%20%22УРАЛБИЗНЕСЛИЗИНГ%22'

# start_end_date = '10.01.2019'


r = 'реквизиты ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "КЛИНИНГ СЕРВИС"'

# url = f'https://zakupki.gov.ru/epz/eruz/search/results.html?morphology=on&search-filter=Дате+размещения' \
#       f'&sortBy=BY_REGISTRY_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&' \
#       f'participantType_0=on&participantType_1=on&participantType_2=on&participantType_3=on&participantType_4=on&' \
#       f'participantType_5=on&participantType_6=on&participantType_7=on&participantType=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&' \
#       f'registered=on&rejectReasonIdNameHidden=%7B%7D&countryRegIdNameHidden=%7B%7D&' \
#       f'registryDateFrom={start_end_date}&registryDateTo={start_end_date}'


def start_base():
    global soup
    collection_list = []
    try:
        base_html_code = requests.get(url, headers=HEADERS)
        if base_html_code.status_code == 200:
            soup = BeautifulSoup(base_html_code.text, 'lxml')
    except:
        print('Нет соединения')
        # блок с ссылками
    contaner_with_links = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')
    if contaner_with_links:
        for item in contaner_with_links:
            # ссылка записи
            pre_links = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href')
            collection_list.append(pre_links)
        # print(self.collection_list)
        return collection_list


def collection_data():
    links_url = start_base()
    for item in links_url:
        # print(item)
        try:
            get_site = requests.get(url=item, headers=HEADERS)

            site = BeautifulSoup(get_site.text, 'lxml')
            # print(self.site )
            # except:
            #     logger.info(f'<ошибка нет сайта>')
            #     logger.warning(f'<ошибка нет сайта>')
            # try:  # название компании
            name_company = site.find(class_='sectionMainInfo__body').find_all(class_='cardMainInfo__section')[
                0].get_text(strip=True)
            print(name_company)
        except:
            logger.info(f'<ошибка название компании>')
            logger.warning(f'<ошибка название компании>')


# collection_data()
# if self.sourse_open.status_code == 200:
        # print('000000000')

        # with open('index.html', 'w', encoding='utf-8') as file:
        # #     file.write(str(soup))
        # with open('index.html', encoding='utf-8') as file:
        #     soup_3 = file.read()
        #     soup_4 = BeautifulSoup(soup_3, 'lxml')
        # print(soup_4)




# url = 'https://www.list-org.com/company/413217'

# url = 'https://www.rusprofile.ru/id/3125250'

# url = 'https://sbis.ru/contragents/1835061171/592001001'

# url = 'https://zachestnyibiznes.ru/company/ul/1096320001634_6321225134_OOO-KLINING-SERVIS'

# url = 'https://www.spark-interfax.ru/permski-krai-chaikovski/ooo-uralbizneslizing-inn-1835061171-ogrn-1041804302462-076a3fcee226434a9fe630a0c8ac00b2'


# url = 'https://www.1cont.ru/contragent/1041804302462'
# url = 'https://synapsenet.ru/searchorganization/organization/1041804302462-ooo-uralbizneslizing'
# url = 'https://comfex.ru/1041804302462/ооо-уралбизнеслизинг'
# url = f'https://kontragent.pro/organization/%D1%87%D0%B0%D0%B9%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%B8%D0%B9/' \
#       f'%D0%BE%D0%BE%D0%BE-%D1%83%D1%80%D0%B0%D0%BB%D0%B1%D0%B8%D0%B7%D0%BD%D0%B5%D1%81%D0%BB%D0%B8%D0%B7%D0%B8%D0%BD' \
#       f'%D0%B3-1041804302462'

url = 'https://zachestnyibiznes.ru/company/ul/1167746699746_7751024840_OOO-TPK-SALARYEVO'


def rusprofile_site():
    try:
        sourse_open = requests.get(url=url, headers=HEADERS)
        time.sleep(random.randint(1, 3))
        soup_4 = BeautifulSoup(sourse_open.text, 'lxml')
        # print(soup_4)

        name_company = soup_4.find('h2', class_='f-s-16 f-w-400 m-b-15').get_text(strip=True)[32: -42]
        try:
            boss_company = soup_4.find_all(class_='m-t-15')[5].find_all(target='_blank')[0].get_text(strip=True)
        except:
            try:
                boss_company = soup_4.find_all(class_='m-t-15')[7].find_all(target='_blank')[0].get_text(strip=True)
            except:
                boss_company = soup_4.find_all(class_='m-t-15')[8].find_all(target='_blank')[0].get_text(strip=True)
                try:
                    boss_company = soup_4.find_all(class_='m-t-15')[6].find_all(target='_blank')[0].get_text(strip=True)
                except Exception as exc:
                    print(exc)

        adress_company = soup_4.find(itemprop='address').get_text(strip=True)[32:]

        # inn_company = soup_4.find(id='copy-details-inn').get_text(strip=True)
        #
        # kpp_company = soup_4.find(id='copy-details-kpp').get_text(strip=True)
        #
        # ogrn_company = soup_4.find(id='copy-details-ogrn').get_text(strip=True)
        # name_ooo_pre = re.findall(r'[\w+]', str(name_company), flags=re.I)
        # name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)
        #
        # winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
        # winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
        print(name_company)
        print(boss_company)
        print(adress_company)
        # print(inn_company)
        # print(kpp_company)
        # print(ogrn_company)

    except Exception as exc:
        print(exc)
        # if 'list' in exc.args[0]:
        #     print('3333')


# rusprofile_site()
# print(caching['winner'])

# get_first_links()
# get_first()

# ______________________________________________
def get_first_links():
    # urll = check_inn_ya.router_site()
    # print(url, '777777777777')

    global soup
    try:
        base_html_code = requests.get(url=url, headers=HEADERS)
        time.sleep(1)
        print(base_html_code)
        if base_html_code.status_code == 200:
            soup = BeautifulSoup(base_html_code.text, 'lxml')
            print(soup)

            # name_company = soup.find('div', id="org-full-header").find('h2').get_text(strip=True)
            # print(name_company)
    except Exception:
        print('Нет соединения', '222222222222222222')
    # pre_links_w = soup.find_all(class_ ='Serp__item__title--2KnDi') #.find('a') #.get('href')
    # print(pre_links_w)
    # отдельный блок с ссылкой на закупку
    # contaner_with_links = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')


# if __name__ == '__main__':
#     get_first_links()

# _________________________________________
registration_date_end_pre = '8yinfo@y-s45fnfuit.ru'
# registration_date_end_pre_1 = re.compile(r'[\d+]{2}\.[\d+]{2}\.[\d+]{4}', flags=re.I)
# registration_date_end_pre_2 = registration_date_end_pre_1.findall(str(registration_date_end_pre))
# registration_date_end = re.sub(r'[\[|]|\'|]', '', str(registration_date_end_pre_2))
registration_date_end = re.findall(r"@\S*", str(registration_date_end_pre))

# line_pre = re.findall(r'@\S*\.', str(line['Email']), flags=re.I)
#             line_pre_2 = re.findall(r'\S*@', str(line['Email']), flags=re.I)

print(str(registration_date_end)[3:-2])

"'['@y-st.']'"

boss_company = "boss_company 'ПОПКОВА 112ЕЛЕНА 7011188597415  701118859741512 ЭДУА4РДОВНА'info@y-st.ru,metallkom2015@list.ru 'tel_company7 4959742274'}"
# tel_company = tel_company.replace(' ', '')
# pick_tel_company_pattern = re.compile(r'[\d+]{11}', flags=re.I)
# pick_tel_company = re.findall(r'[\d+]{11}', str(tel_company))
# print(pick_tel_company, '11111111111111111111111111111111111111111111111111')
# x = 'КАРАЧАЕВО-ЧЕРКЕССКОЕ РЕГИОНАЛЬНОЕ ОТДЕЛЕНИЕ ОБЩЕРОССИЙСКОЙ ОБЩЕСТВЕННОЙ ОРГАНИЗАЦИИ ИНВАЛИДОВ "ВСЕРОССИЙСКОЕ ОБЩЕСТВО ГЛУХИХ"'
# xy = re.findall(r'КАРАЧАЕВО-ЧЕРКЕССКОЕ РЕГИОНАЛЬНОЕ ОТДЕЛЕНИЕ ОБЩЕРОССИЙСКОЙ ОБЩЕСТВЕННОЙ ОРГАНИЗАЦИИ ИНВАЛИДОВ "ВСЕРОССИЙСКОЕ ОБЩЕСТВО ГЛУХИХ"', x, flags=re.I)

e = '630129'
i = '"ЭСБИ"'

data_search = f'инн ООО {i} Юридический адрес {e},'
# data_search = f'инн {i}'
#
# check_inn_ya.router_site()

# date_time_str = '2018-06-29 08:15:27.243860'
# date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f') # строка в дату и разбивка по периодам
# print('Дата:', date_time_obj.date())
# print('Время:', date_time_obj.time())
# print('Дата и время:', date_time_obj)
# #------------------------------
# # Дата в строку и дальше в число через  replace
# start_date_pre = datetime.date.today().strftime('%d.%m.%Y')
# start_date = start_date_pre.replace("'", " ").replace(" ", "")
# #----------------------------
# start_search_delta = datetime.now().isoformat() #  формат базы данных
# pre_date_winner_protokol_hour = start_search_delta[:start_search_delta.find('.')]
# print(pre_date_winner_protokol_hour)
# date_winner_protokol_hour = datetime.datetime.strptime(start_search_delta,'%d.%m.%Y %H:%M')
# print(date_winner_protokol_hour)


# def get_info():
#     var_path_file = 'file_base.csv'
#     with open(var_path_file, mode='r',  encoding='utf-8') as file:
#         reader = csv.DictReader(file, delimiter=",")
#         # reader = csv.reader(file, delimiter=",")
#         for line in reader:
#             print(line['ИНН'])

def get_info():
    try:
        # Подключиться к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="Vfrcvfrc1",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="general_lids")

        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        var_path_file = 'data-1626600342122.csv'
        with open(var_path_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # reader = csv.reader(file)
            for line in reader:
                print(line['name_company'], line['inn_company'], line['adress_index_company'])
                cursor.execute(
                    f"select name_company from no_validate_lids where adress_index_company = {line['adress_index_company']};")

                record = cursor.fetchall()
                print("Результат", record)


    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


# get_info()


# print('Время:', date_time_obj.time())
# print('Дата и время:', date_time_obj)
# ------------------------------
# Дата в строку и дальше в число через  replace
# start_date_pre = datetime.date.today().strftime('%d.%m.%Y')

# start_date = start_date_pre.replace("'", " ").replace(" ", "")
# #----------------------------
# start_search_delta = datetime.now().isoformat() #  формат базы данных
# pre_date_winner_protokol_hour = start_search_delta[:start_search_delta.find('.')]
# print(pre_date_winner_protokol_hour)
# date_winner_protokol_hour = datetime.datetime.strptime(start_search_delta,'%d.%m.%Y %H:%M')
# print(date_winner_protokol_hour)
#
e = '18.07.2021'

# start_search = datetime.date.strftime('%d.%m.%Y')

# TODO конвертация в строку
# start_search = datetime.date.strftime(e,'%Y.%m.%d %H:%M')
# TODO конвертация в объект времени

# start_search = datetime.datetime.now(datetime.timezone.utc).astimezone()
# print(start_search)
start_search = datetime.datetime.now().date()
print(start_search)
# start_search_pre = datetime.datetime.strptime(start_search_,'%Y.%m.%d %H:%M')
# print(start_search_pre)
# start_search = datetime.datetime.strptime(start_search_pre,'%Y.%m.%d %H:%M')
# print(start_search)
# end_search_pre = datetime.datetime.strptime(e,'%d.%m.%Y')
# print(end_search_pre)

# x = '19.07.2021 00:00'
# end = datetime.datetime.strptime(x,'%d.%m.%Y %H:%M')
# print(end)

# print(end_search_pre)
# end_search = datetime.datetime.strftime(end_search_pre,'%Y.%m.%d %H:%M')
# print(end_search)
# end_search_res = start_search - end_search_pre
# end_search_res = start_search - end_search_pre


# print(end_search_res)
