# -*- coding: utf-8 -*-
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import json
import re
import locale
from requests.exceptions import InvalidSchema
from selenium import webdriver
import csv

HOST = 'https://zakupki.gov.ru'

url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
      'pageNumber=uu&sortDirection=true&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
      'pc=on&priceFromGeneral=1000000&currencyIdGeneral=-uu&EADateFrom=01.03.2021&EADateTo=05.03.2021&' \
      'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&' \
      'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}


def get_data_with_seleniun(url):
    global hendler_src3
    options = webdriver.FirefoxOptions()
    options.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                                         ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                                         ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663'
                                                         ' Yowser/2.5 Safari/537.36')
    try:
        driver = webdriver.Firefox(
            executable_path='/Users/User/PycharmProjects/python_base/python_base/My_Work/My_first/geckodriver.exe',
            options=options
        )
        driver.get(url=url)
        time.sleep(5)

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as exc:
        print(exc)

    finally:
        driver.close()
        driver.quit()


# x = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/supplier-results.html?regNumber=0875600002521000011'

# get_data_with_seleniun(url)
with open('index.html', encoding='utf-8') as file:
    hendler_src3 = file.read()

reg = requests.get(url, headers=headers)  # получаем результат запроса get т.е. ответ и сохраняем в переменную reg
src = reg.text
soup = BeautifulSoup(src, 'lxml')
# pre_links1 = {}
all_links = []
contaner_links = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')  # контейнер отдельно
for item in contaner_links:
    pre_links1 = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href')

    reg2 = requests.get(url=pre_links1, headers=headers)
    src2 = reg2.text
    soup2 = BeautifulSoup(src2, 'lxml')
    # print(pre_links1)
    try:
        data_tender = soup2.find_all(class_='container')[7].find_all(class_='blockInfo__section')[5].find(
            class_='section__info').get_text(strip=True)
        if len(re.compile('\d+').findall(str(data_tender))) < 3:
            raise ValueError('uuu')
    except Exception as exc:
        data_tender = soup2.find_all(class_='container')[7].find_all(class_='blockInfo__section')[4].find(
            class_='section__info').get_text(strip=True)
    try:
        sum_bg = soup2.find_all(class_='row blockInfo')[10].find_all(class_='section__info')[1].get_text(). \
            replace('\xa0', ' ', ).replace('\u20bd', ' ').replace('\r', '').replace('\n', '').replace(' ', '')
    except Exception as exc:
        if 'list index out of range' in exc.args[0]:
            sum_bg = soup2.find('div', class_='collapse__content collapse__content0').find_all(
                'div', class_='content__block blockInfo')[4].find_all('section', class_='blockInfo__section section')[
                1].find(
                'span', class_='section__info').get_text(). \
                replace('\xa0', ' ', ).replace('\u20bd', ' ').replace('\r', '').replace('\n', '').replace(' ', '')

    pre_links2 = HOST + soup2.find('div', class_='tabsNav d-flex align-items-end').find_all('a')[2].get('href')
    # print(pre_links2)
    reg3 = requests.get(url=pre_links2, headers=headers)
    src3 = reg3.text
    soup3 = BeautifulSoup(src3, 'lxml')
    try:
        res_tender_winner = soup3.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[2]. \
            get_text(strip=True)
    except Exception as exc:
        # if 'list index out of range' in exc.args[0]:
        get_data_with_seleniun(pre_links2)
        with open('index.html', encoding='utf-8') as file:
            hendler_src3 = file.read()
        soup4 = BeautifulSoup(hendler_src3, 'lxml')
        res_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[2]. \
            get_text(strip=True)
        # print(f'заряжаем{exc}')
    print(res_tender_winner)

    try:
        status_tender_winner = soup3.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[3]. \
            get_text(strip=True)
    except Exception as exc:
        # if 'list index out of range' in exc.args[0]:
        # get_data_with_seleniun(pre_links2)
        # with open('index.html', encoding='utf-8') as file:
        #     hendler_src3 = file.read()
        soup4 = BeautifulSoup(hendler_src3, 'lxml')
        status_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[3]. \
            get_text(strip=True)
    print(status_tender_winner)

    try:
        sum_tender_winner = soup3.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
            4].get_text(
            strip=True)
    except Exception as exc:
        # if 'list index out of range' in exc.args[0]:
        # get_data_with_seleniun(pre_links2)
        # with open('index.html', encoding='utf-8') as file:
        #     hendler_src3 = file.read()
        soup4 = BeautifulSoup(hendler_src3, 'lxml')
        sum_tender_winner = soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
            4].get_text(strip=True)
    print(sum_tender_winner)

    try:
        link_tender_winner = HOST + soup3.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
            3]. \
            find('a').get('href')
    except Exception as exc:
        # if 'list index out of range' in exc.args[0]:
        # get_data_with_seleniun(pre_links2)
        # with open('index.html', encoding='utf-8') as file:
        #     hendler_src3 = file.read()
        soup4 = BeautifulSoup(hendler_src3, 'lxml')
        link_tender_winner = HOST + soup4.find('div', id='searchResWrapper').find_all('td', class_='tableBlock__col')[
            3].find('a').get('href')
        # print(f'заряжаем{exc}')
    print(link_tender_winner)

    # try:
    #     time_contract_winner = soup3.find('td', class_='tableBlock__col tableBlock__row').find_all(
    #         'td', class_='tableBlock__col')[2].get_text(strip=True)
    # except Exception as exc:
    #     # if 'list index out of range' in exc.args[0]:
    #         # get_data_with_seleniun(pre_links2)
    #         # with open('index.html', encoding='utf-8') as file:
    #         #     hendler_src3 = file.read()
    #     soup4 = BeautifulSoup(hendler_src3, 'lxml')
    #     time_contract_winner = soup4.find('td', class_='tableBlock__col tableBlock__row').find_all(
    #     'td', class_='tableBlock__col')[2].get_text(strip=True)
    #     # print(f'заряжаем{exc}')
    # print(time_contract_winner)

    try:
        file_contract_winner = soup3.find('td', class_='tableBlock__col tableBlock__row').find(
            'span', class_='section__value').find('a').get('href')
    except Exception as exc:

        soup4 = BeautifulSoup(hendler_src3, 'lxml')
        file_contract_winner = soup4.find('td', class_='tableBlock__col tableBlock__row').find('span',
                                                                                               class_='section__value').find(
            'a').get('href')

        print(f'заряжаем{exc}')
    print(file_contract_winner)

    # all_links.append(
    #     {
    #         'link_tender': HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href'),
    #         'tender_number': item.find('div', {'class': 'registry-entry__header-mid__number'}).get_text(strip=True),
    #         'price_tender': item.find('div', {'class': 'price-block__value'}).get_text(strip=True).replace(
    #             '\xa0', ' ', ).replace('\u20bd', ' '),
    #         'sm_bg': sum_bg,
    #         'd_tender': data_tender,
    #         'status_tender': item.find('div', {'class': 'registry-entry__header-mid__title'}).get_text(strip=True),
    #         'res_tender_winner': res_tender_winner,
    #         'status_tender_winner': status_tender_winner,
    #         'sum_tender_winner': sum_tender_winner,
    #         'link_tender_winner': link_tender_winner,
    #         'time_contract_winner': time_contract_winner,
    #         'file_contract_winner': file_contract_winner
    #     }
    # )

# pprint(all_links)
# dict_data = {}
# for item in all_links:  # проход по отдельному списку all_links
#     item_text_tender_number = item['tender_number']
#     item_href_link_tender = item['link_tender']
#     item_href_price_tender = item['price_tender']
#     item_href_status_tender = item['status_tender']
#     item_href_data_tender = item['d_tender']
#     item_href_sum_bg = item['sm_bg']
#     dict_data[item_text_tender_number] = item_href_price_tender, item_href_link_tender,\
#                                          item_href_status_tender, item_href_sum_bg, item_href_data_tender
#
# with open('dict_data.json', 'w', encoding='utf-8') as file:
#     json.dump(dict_data, file, indent=4, ensure_ascii=False) # indent=4 это отступ и перенос строки, ensure_ascii=False #не экранирует символы и позволяет видеть кириллицу
#
#     # загружаем файл json в переменную
#     with open('dict_data.json', encoding='utf-8') as file:
#         data_json = json.load(file)
# TODO __________________________


# with open('dict_data.csv', 'w', newline='', encoding='1251') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['Номер тендера', 'Ссылка', 'НМЦК', 'Статус Тендера', 'Дата', 'Сумма Бг'])
#     for item in all_links:
#         writer.writerow([item['tender_number'], item['link_tender'], item['price_tender'],
#                          item['status_tender'], item['d_tender'], item['sm_bg']])
# TODO __________________________


# with open('dict_data1.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['Дата'])
#     for item in step1:
#         writer.writerow([item['data_tender']])
# #
# with open('dict_data2.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['Сумма Бг'])
#     for item in step2:
#         writer.writerow([item['sm_bg']])


# for item in step1:  # проход по отдельному списку all_links
#     item_href_data_tender = item['data_tender']
#     item_href_sum_bg = item['sum_bg']
#     dict_data[item_href_data_tender] = item_href_sum_bg, item_href_data_tender

# with open('dict_data.csv', 'a', newline='', encoding='cp1251') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['Дата', 'СуммаБг'])
#     for item in step1:
#         writer.writerow([item['data_tender'], item['sum_bg']])

# print(f"{item_href_sum_bg}")
# тендера item_text = item['tender_number'],
# а значение ссылка item_href = item['link_tender']


# print(dict_data)


# ____________________________________________
# сохраняем словарь в формат  json

# with open('dict_data.json', 'w', encoding='utf-8') as file:
#     json.dump(dict_data, file, indent=4, ensure_ascii=False) # indent=4 это отступ и перенос строки, ensure_ascii=False #не экранирует символы и позволяет видеть кириллицу
#
#     # загружаем файл json в переменную
#     with open('dict_data.json', encoding='utf-8') as file:
#         data_json = json.load(file)


# dict_data = {}
# for item in all_links:  # проход по отдельному списку all_links
#     item_text_tender_number = item['tender_number']
#     item_href_link_tender = item['link_tender']
#     # print(f" {item_text}:  {item_href}")
#     dict_data[item_text_tender_number] = item_href_link_tender


# contaner_links = soup.find_all(class_='href d-flex')
# print(contaner_links)
# for item in contaner_links:
#     item_text = item.text  # текст извлекаем и получаем методом .text (если все в одной строке)
#     item_href = item.get('href')  # ссылку извлекаем и получаем методом .get('href') (если все в одной строке)
# print(f'{item_text} {item_href}')
# count += uu
# сохраняем файлы html в переменную


#  блок запроса
# url = 'https://zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=0134200000121000435'
#
# headers = {
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
#                 'q=0.8,application/signed-exchange;v=b3;q=0.9',
#       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                     ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
# }
#
# HOST = 'https://zakupki.gov.ru'

# reg = requests.get(url, headers=headers)


# создаем экземпляр класса BeautifulSoup т.е. объект, в параметры передаем переменную с html данными и параметр
# парсера в нашем случае парсер 'lxml'

# soup = BeautifulSoup(reg.text, 'lxml')
# метод если ссылка прописана на уровне класса в одной строке не в потомке теге '<a>'

# contaner_links = soup.find_all(class_='href d-flex')
# print(contaner_links)
# for item in contaner_links:
#     item_text = item.text # текст извлекаем и получаем методом .text (если все в одной строке)
#     item_href = item.get('href') # ссылку извлекаем и получаем методом .get('href') (если все в одной строке)
#     print(f'{item_text} {item_href}')
# ___________________________________________________
# step1 = []
# contaner_ = soup.find_all(class_='container')[7].find_all(class_='blockInfo__section')[5].find(class_='section__info')  # контейнер отдельно
# step_1 = contaner_.find_all(class_='blockInfo__section')[5].find(class_='section__info')
# step_2 = step_1.find(class_='section__info')

# print(contaner_.text.strip())


# for item in contaner_:  # проход по контейнерам и добавление в отдельный список all_links
#     all_links.append({
#         'link_tender': HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href'),
#         'tender_number': item.find('div', {'class': 'registry-entry__header-mid__number'}).get_text(strip=True)
#     })
#
# dict_data = {}
# for item in all_links:  # проход по отдельному списку all_links
#     item_text_tender_number = item['tender_number']
#     item_href_link_tender = item['link_tender']
#     # print(f" {item_text}:  {item_href}")
#     dict_data[item_text_tender_number] = item_href_link_tender  # добавляем в словарь dict_data где ключ это номер
#     # тендера item_text = item['tender_number'],
#     # а значение ссылка item_href = item['link_tender']
# # ____________________________________________
# # сохраняем словарь в формат  json
#
# # with open('dict_data.json', 'w', encoding='utf-8') as file:
# #     json.dump(dict_data, file, indent=4, ensure_ascii=False) # indent=4 это отступ и перенос строки,
# # ensure_ascii=False не экранирует символы и позволяет видеть кириллицу
#
#
# # загружаем файл json в переменную
# with open('dict_data.json', encoding='utf-8') as file:
#     data_json = json.load(file)
