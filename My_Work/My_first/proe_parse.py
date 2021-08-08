# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json

#  блок запроса
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
#       'pageNumber=uu&sortDirection=true&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=PUBLISH_DATE&fz44=on&' \
#       'pc=on&priceFromGeneral=10000000&currencyIdGeneral=-uu&EADateFrom=19.03.2021&EADateTo=23.03.2021&' \
#       'OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&' \
#       'orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'
#
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}
#
# # requests.get() отправляет запрос на внешний сайт через get и получает ответ
#
# reg = requests.get(url, headers=headers) # получаем результат запроса get т.е. ответ и сохраняем в переменную reg
#
# src = reg.text # сохраняем в переменную результат запроса get т.е. ответ
# # print(src)
#
# # сохраняем результат запроса в файл, это нужно чтобы не прервалась работа из-за блокировки  обрабатываемым сайтом
# # если поймет что парсит робот. Страхуемся и продолжаем работу  локально
# #_____________________________
# # качаем и сохраняем html
# with open('index.html', 'w', encoding='utf-8') as file:
#       file.write(src)
# ____________________________________
# сохраняем локальный файл html в переменную
with open('index.html', encoding='utf-8') as file:
    src = file.read()
# ____________________________________
# создаем экземпляр класса BeautifulSoup т.е. объект, в параметры передаем переменную с html данными и параметр
# парсера в нашем случае парсер 'lxml'
HOST = 'https://zakupki.gov.ru'
soup = BeautifulSoup(src, 'lxml')
# метод если ссылка прописана на уровне класса в одной строке не в потомке теге '<a>'

# contaner_links = soup.find_all(class_='href d-flex')
# print(contaner_links)
# for item in contaner_links:
#     item_text = item.text # текст извлекаем и получаем методом .text (если все в одной строке)
#     item_href = item.get('href') # ссылку извлекаем и получаем методом .get('href') (если все в одной строке)
#     print(f'{item_text} {item_href}')
# ___________________________________________________
all_links = []
contaner_links = soup.find_all(class_='search-registry-entry-block box-shadow-search-input')  # контейнер отдельно
for item in contaner_links:  # проход по контейнерам и добавление в отдельный список all_links
    all_links.append({
        'link_tender': HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href'),
        'tender_number': item.find('div', {'class': 'registry-entry__header-mid__number'}).get_text(strip=True)
    })

dict_data = {}
for item in all_links:  # проход по отдельному списку all_links
    item_text_tender_number = item['tender_number']
    item_href_link_tender = item['link_tender']
    # print(f" {item_text}:  {item_href}")
    dict_data[item_text_tender_number] = item_href_link_tender  # добавляем в словарь dict_data где ключ это номер
    # тендера item_text = item['tender_number'],
    # а значение ссылка item_href = item['link_tender']
# ____________________________________________
# сохраняем словарь в формат  json

# with open('dict_data.json', 'w', encoding='utf-8') as file:
#     json.dump(dict_data, file, indent=4, ensure_ascii=False) # indent=4 это отступ и перенос строки,
# ensure_ascii=False не экранирует символы и позволяет видеть кириллицу


# загружаем файл json в переменную
with open('dict_data.json', encoding='utf-8') as file:
    data_json = json.load(file)
# print(data_json)
# проходим по словарю data_json
count = 0
for item_text_tender_number, item_href_link_tender in data_json.items():
    # при необходимости предварительная чистка, сейчас чистим строку ключа одновременно от нескольких символов
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in item_text_tender_number:
            item_text_tender_number = item_text_tender_number.replace(item, "_")  # заменяем при необходимости
            # не желательные смвоы на "_"
    # открываем каждую ссылку:
    req = requests.get(url=item_href_link_tender, headers=headers)
    src = req.text  # сохраняем в переменную результат запроса

    # сохранение станицы полученной по ссылке в html под именем ключа (номер тендера) в созданную папку data
    # with open(f"data/{count}_{item_text_tender_number}.html",'w', encoding='utf-8') as file:
    #     file.write(src)
    with open(f"data/{count}_{item_text_tender_number}.html", encoding='utf-8') as file:
        srcparse = file.read()
    soup = BeautifulSoup(srcparse, 'lxml')

    contaner_links = soup.find_all(class_='href d-flex')
    print(contaner_links)
    for item in contaner_links:
        item_text = item.text  # текст извлекаем и получаем методом .text (если все в одной строке)
        item_href = item.get('href')  # ссылку извлекаем и получаем методом .get('href') (если все в одной строке)
        print(f'{item_text} {item_href}')
    count += 1
    # сохраняем файлы html в переменную
