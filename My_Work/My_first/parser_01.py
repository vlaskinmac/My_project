# -*- coding: utf-8 -*-
from pprint import pprint
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import csv
import re

CSV = 'base.csv'

HOST = 'https://zakupki.gov.ru'

EADATEFROMSTART = '19.03.2021'
EADATEFROMEND = '23.03.2021'
PRICEMIN = '50000000'
page = None

URL = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=' \
      f'Дате+размещения&pageNumber={page}&sortDirection=true&recordsPerPage=_10&' \
      f'showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
      f'pc=on&priceFromGeneral={PRICEMIN}&currencyIdGeneral=-1&' \
      f'EADateFrom={EADATEFROMSTART}&EADateTo={EADATEFROMEND}&' \
      f'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", {"class": "row no-gutters registry-entry__form mr-0"})
    links = []
    for item in items:
        links.append({'link_tender': HOST + item.find('div', {'class': 'registry-entry__header-mid__number'}).find(
            'a').get('href')})
        pprint(links)
    return links


html = get_html(URL)
get_link(html.text)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", {"class": "row no-gutters registry-entry__form mr-0"})
    data = []
    for item in items:
        data.append(
            {
                'tender_number': item.find('div', {'class': 'registry-entry__header-mid__number'}).get_text(strip=True),
                'link_tender': HOST + item.find('div', {'class': 'registry-entry__header-mid__number'}).find('a').get(
                    'href'),
                'price_tender': item.find('div', {'class': 'price-block__value'}).get_text(strip=True).replace(
                    '\xa0', ' ', ).replace('\u20bd', ' '),
                'status_tender': item.find('div', {'class': 'registry-entry__header-mid__title'}).get_text(strip=True)
            }
        )

    return data


# html = get_html(URL)
# pprint(get_content(html.text))

def file_base(items, path):
    with open(path, 'w', newline='', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Номер тендера', 'Ссылка', 'НМЦК', 'Статус Тендера'])
        for item in items:
            writer.writerow([item['tender_number'], item['link_tender'], item['price_tender'], item['status_tender']])


def parser():
    global URL
    html = get_html(URL)
    if html.status_code == 200:
        data = []
        page = 0
        while get_content(html.text):
            page += 1
            print(f'страница: {page}')
            URL = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter' \
                  f'=Дате+размещения&' \
                  f'pageNumber={page}&sortDirection=true&recordsPerPage=_10&showLotsInfoHidden=false&sortBy' \
                  f'=PUBLISH_DATE&fz44=on&' \
                  f'pc=on&priceFromGeneral={PRICEMIN}&currencyIdGeneral=-1&EADateFrom={EADATEFROMSTART}&' \
                  f'EADateTo={EADATEFROMEND}&' \
                  f'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&' \
                  f'OrderPlacementExecutionRequirement=on&' \
                  f'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'
            html = get_html(URL, params=page)
            data.extend(get_content(html.text))
            file_base(data, CSV)

        print(f'стр занончены')

    else:
        print('error')


parser()
