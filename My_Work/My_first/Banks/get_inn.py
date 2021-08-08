# -*- coding: utf-8 -*-
import datetime
import re
import psycopg2
from psycopg2 import Error
from selenium import webdriver
import os
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from termcolor import cprint
import parsePdf
import mod_logger
from My_Work.My_first.Banks import test_dx

logger = mod_logger.get_logger(__name__)
# logging.disable(logging.INFO)


HOST = 'https://zakupki.gov.ru/'
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

# start_search = datetime.date.today().strftime('%d.%m.%Y')
stupdateDateFrom = '14.07.2021'
recordsPerPage = 50
priceFromGeneral = '3000000'

all_info = []
urls = f'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&' \
       f'pageNumber=1&sortDirection=false&recordsPerPage=_{recordsPerPage}&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&' \
       f'placingWayList=EA44%2CEAP44%2CEAB44%2CEAO44%2CEEA44%2COK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%' \
       f'2COKI504%2COKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504&selectedLaws=FZ44&' \
       f'priceFromGeneral={priceFromGeneral}&currencyIdGeneral=-1&updateDateFrom={stupdateDateFrom}&OrderPlacementSmallBusinessSubject=on&' \
       f'OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&' \
       f'orderPlacement94_1=0&orderPlacement94_2=0'

# АО «ЕЭТП»
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=OK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504%2COKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504%2CEA44%2CEAP44%2CEAB44%2CEAO44%2CEEA44&selectedLaws=FZ44&etp_7360767=on&etp=7360767&priceFromGeneral=1000000&currencyIdGeneral=-1&updateDateFrom=17.06.2021&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# 'АГЗ РТ'
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=OKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504%2COK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504%2CEA44%2CEAP44%2CEAB44%2CEAO44%2CEEA44&selectedLaws=FZ44&etp_7360766=on&etp=7360766&priceFromGeneral=1000000&currencyIdGeneral=-1&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# 'РТС-ТЕНДЕР'
url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=OKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504%2COK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504&selectedLaws=FZ44&etp_7360768=on&etp=7360768&priceFromGeneral=1000000&currencyIdGeneral=-1&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# 'НАЦИОНАЛЬНАЯ ЭЛЕКТРОННАЯ ПЛОЩАДКА'
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=EA44%2CEAP44%2CEAB44%2CEAO44%2CEEA44%2COK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504%2COKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504&selectedLaws=FZ44&etp_7360770=on&etp=7360770&priceFromGeneral=1000000&currencyIdGeneral=-1&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# ЭТП Газпромбанк
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=EA44%2CEAP44%2CEAB44%2CEAO44%2CEEA44%2COK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504%2COKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504&selectedLaws=FZ44&etp_24319911=on&etp=24319911&priceFromGeneral=10000000&currencyIdGeneral=-1&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# 'АО "РАД"'
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=OK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504&selectedLaws=FZ44&etp_9584642=on&etp=9584642&priceFromGeneral=1000000&currencyIdGeneral=-1&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

# 'ЭТП ТЭК-ТОРГ'
# url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=Дате+размещения&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&pc=on&placingWayList=OKU504%2COKUP504%2COKUI504%2CEOKU504%2COKUK504%2CEA44%2CEAP44%2CEAB44%2CEAO44%2CEEA44%2COK504%2COKP504%2COKK504%2COKA504%2CEOK504%2COKB504%2COKI504&selectedLaws=FZ44&etp_24319912=on&etp=24319912&priceFromGeneral=1000000&currencyIdGeneral=-1&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0'

file_way = os.path.abspath('C:\\working_download\\down_step_1\\download')
caching = {}

class Parser:
    # options = webdriver.ChromeOptions()
    # browser = webdriver.Chrome('chromedriver', options=options)

    # start_search_delta = datetime.date.today() - datetime.timedelta(days=10)
    # start_search_date = start_search_delta.strftime('%d.%m.%Y')

    # end_search_delta = datetime.date.today() - datetime.timedelta(days=6)
    # end_search_date = end_search_delta.strftime('%d.%m.%Y')
    file_way = os.path.abspath('C:\\working_download\\down_step_1\\download')

    list_inn = []

    def __init__(self, url=url, list_inn=None, caching=caching):

        self.url = url
        self.list_inn = list_inn
        self.caching = caching

    # def time_date(self):
    #     pass

    def get_first_links(self):
        try:
            base_html_code = requests.get(self.url, headers=HEADERS)
            if base_html_code.status_code == 200:
                self.soup = BeautifulSoup(base_html_code.text, 'lxml')
        except Exception:
            print('Нет соединения')
            # отдельный блок с ссылкой на закупку
        contaner_with_links = self.soup.find_all(class_='search-registry-entry-block box-shadow-search-input')
        if contaner_with_links:
            count = 0
            # x = datetime.datetime.now()
            # print(x, 'start')
            for item in contaner_with_links:
                count += 1
                # print(item)
                # проверка на отмену  процедуры
                chek_error = item.find('div', class_='error')
                if not chek_error:
                    # ссылка  тендера
                    self.pre_links = HOST + item.find(class_='registry-entry__header-mid__number').find('a').get('href')
                    # номер  тендера  стр
                    # print(self.pre_links)
                    tender_number_pre = item.find('div', class_='registry-entry__header-mid__number').get_text(
                        strip=True)
                    self.tender_number = re.sub("\D*", "", str(tender_number_pre))
                    logger.info(f'<-------------------------------------------------> - новая закупка')
                    logger.info(f'<номер тендера> - {self.tender_number}')
                    self.caching['tender_number'] = self.tender_number
                    # print(self.caching['tender_number'])
                    # вид торгов
                    procedura = item.find(class_='registry-entry__header-top__title text-truncate').get_text(strip=True)
                    x = re.sub(r'[\r|\n]', '', str(procedura))
                    if not procedura:
                        logger.warning(f'поле <вид торгов> пустое,{self.tender_number}')
                        logger.info(f'поле <вид торгов> пустое ')

                    y = x.split()[1:3]
                    self.r = re.sub(r'[,|\'\[|\]]', '', str(y))
                    logger.info(f'<вид торгов> - {self.r}')
                    procedura_go = re.findall(self.r, str('Электронный аукцион'))
                    procedura_go_pre = re.sub(r'[,|\'\[|\]]', '', str(procedura_go))

                    procedura_auction = str(procedura_go_pre).upper()
                    self.caching['auction'] = procedura_auction
                    procedura_go = re.findall(self.r, str('Открытый конкурс'))
                    procedura_go_pre = re.sub(r'[,|\'\[|\]]', '', str(procedura_go))

                    procedura_conkurs = str(procedura_go_pre).upper()
                    self.caching['conkurs'] = procedura_conkurs
                    procedura_go = re.findall(self.r, str('Конкурс с'))
                    procedura_go_pre = re.sub(r'[,|\'\[|\]]', '', str(procedura_go))

                    procedura_ogr_conkurs = str(procedura_go_pre).upper()
                    self.caching['ogr_conkurs'] = procedura_ogr_conkurs
                    self.caching['pre_links'] = self.pre_links

                    yield self.caching


class Router(Parser):

    def etp_identification(self):

        logger.info(f'<начало работы роутера>')
        for self.item in self.get_first_links():
            logger.info(f'<номер тендера> - {self.tender_number}')
            # print(self.pre_links)
            try:
                try:
                    get_site_tender = requests.get(url=self.item['pre_links'], headers=HEADERS)
                    if get_site_tender.status_code == 200:
                        self.site_tender = BeautifulSoup(get_site_tender.text, 'lxml')
                        self.caching['site_tender'] = self.site_tender
                except:
                    pass
                    # ссылка на позицию графика заказчика - срок контракта определяем
                try:
                    self.link_term_contract = HOST + self.site_tender.find_all(class_="row blockInfo")[0].find_all(
                        class_="section__info")[6].find('a').get('href')
                except:
                    pass
                try:
                    self.link_term_contract = HOST + self.site_tender.find_all(class_="row blockInfo")[0].find_all(
                        class_="section__info")[7].find('a').get('href')
                except:
                    pass
                self.term_contract = requests.get(url=self.link_term_contract, headers=HEADERS)
                self.site_term_contract = BeautifulSoup(self.term_contract.text, 'lxml')

                self.term_contract_pre = self.site_term_contract.find_all(class_="tableBlock__body")[0].find_all(
                    class_="tableBlock__col")[0].get_text(strip=True)
                self.term_contract_21 = re.sub("[\D+]", "", str(self.term_contract_pre))
                self.term_contract_pre = self.site_term_contract.find_all(class_="tableBlock__body")[0].find_all(
                    class_="tableBlock__col")[1].get_text(strip=True)
                self.term_contract_22 = re.sub("\D+", "", str(self.term_contract_pre))
                self.term_contract_pre = self.site_term_contract.find_all(class_="tableBlock__body")[0].find_all(
                    class_="tableBlock__col")[2].get_text(strip=True)
                self.term_contract_23 = re.sub("\D+", "", str(self.term_contract_pre))
                # срок контракта/бг определяем
                if len(self.term_contract_21) > 3:
                    self.caching['term'] = '2022.01.31'
                    if self.caching['term']:
                        logger.info(f"<срок контракта> - {self.caching['term']}")
                elif len(self.term_contract_22) > 3:
                    self.caching['term'] = '2023.01.31'
                    if self.caching['term']:
                        logger.info(f"<срок контракта> - {self.caching['term']}")
                elif len(self.term_contract_23) > 3:
                    self.caching['term'] = '2024.01.31'
                    if self.caching['term']:
                        logger.info(f"<срок контракта> - {self.caching['term']}")
                if not self.caching['term']:
                    logger.warning(f'ошибка <срока контракта> ,{self.tender_number}')

            except Exception as exc:
                self.caching['term'] = '2022.01.31'
                logger.warning(f'ошибка <срока контракта>,{self.tender_number}, {exc}')

            try:
                self.etp_pre = self.site_tender.find_all(class_="row blockInfo")[0].find_all(
                    'span', class_="section__info")[1].get_text(strip=True)
                self.caching['etp_pre'] = self.etp_pre
                logger.info(f"<ЭТП> - {self.caching['etp_pre']}")
                if not self.caching['etp_pre']:
                    logger.warning(f'поле <ЭТП> пустое ,{self.tender_number}')
                    logger.info(f'поле <ЭТП> пустое')
            except:
                pass
            yield self.caching


    def link_protokol(self):
        logger.info(f" начало функции <link_protokol> ")
        for self.item in self.etp_identification():

            try:  # ссылка протокола
                self.link_winner_protokol = HOST + self.item['site_tender'].find(
                    'div', class_='tabsNav d-flex align-items-end').find_all('a')[2].get('href')
                # ссылка протокола
                self.caching['link_winner_protokol'] = self.link_winner_protokol
            except:
                pass
            try:  # сайт протокола
                get_site_winner_protokol = requests.get(url=self.link_winner_protokol, headers=HEADERS)
                if get_site_winner_protokol.status_code == 200:
                    self.site_winner_protokol = BeautifulSoup(get_site_winner_protokol.text, 'lxml')
                    # print(self.site_winner_protokol, 'сайт протокола')
            except:
                pass

            # ссылка на документ протокола
            try:
                self.pre_links_w = self.site_winner_protokol.find('span', class_='section__info').find('a').get(
                    'href')

                self.caching['pre_links_w'] = self.pre_links_w


            except Exception:
                self.caching['pre_links_w'] = None
                logger.info(f'поле <ссылка на документ протокола> пустое ,{self.tender_number}')
                logger.warning(f'поле <ссылка на документ протокола> пустое ,{self.tender_number}')

            # победитель название и сумма договора
            try:
                self.winner = (
                    self.site_winner_protokol.find_all(class_='tableBlock__body')[1].find(
                        class_='tableBlock__row').find_all('td', class_='tableBlock__col')[0].get_text(strip=True))
                self.winner_1 = (
                    self.site_winner_protokol.find_all(class_='tableBlock__body')[1].find(
                        class_='tableBlock__row').find_all('td', class_='tableBlock__col')[1].get_text(strip=True))
                self.sum_dogovor = (
                    self.site_winner_protokol.find_all(class_='tableBlock__body')[1].find(
                        class_='tableBlock__row').find_all('td', class_='tableBlock__col')[2].get_text(strip=True))

                # sum_bg прописать
                self.caching['sum_bg'] = 'sum_bg'
                self.caching['date_record'] = 'date_record'
                self.caching['mail_company'] = 'mail_company'
                if self.sum_dogovor != '1 - Победитель' and self.sum_dogovor != '2 - Второй номер':
                    self.caching['sum_dogovor'] = self.sum_dogovor
                    logger.info(f"<сумма договора> - {self.caching['sum_dogovor']}")

                    if not self.caching['sum_dogovor']:
                        logger.warning(f'поле <сумма договора> пустое ,{self.tender_number}')
                        logger.info(f'поле <сумма договора> пустое ,{self.tender_number}')
                if self.winner_1 == '1 - Победитель' or re.findall(r'ч. 9 ст. 54.7', str(self.winner_1), flags=re.I):
                    if self.caching['pre_links_w'] is None:
                        self.caching['winner'] = None
                    else:
                        self.caching['winner'] = self.winner
                        logger.info('-')
                        logger.info(f"<победитель с сайта> - {self.caching['winner']}")
                        logger.info('-')
                    if not self.caching['winner']:
                        logger.warning(f'поле <победитель > пустое ,{self.tender_number}')
                        logger.info(f'поле <победитель > пустое ,{self.tender_number}')
                        continue

                elif re.findall(r'ч. 16 ст. 54.4', str(self.winner_1), flags=re.I) or re.findall(
                        r'ч. 8 ст. 54.5', str(self.winner_1), flags=re.I):
                    if self.caching['pre_links_w'] is None:
                        self.caching['winner'] = None
                    else:
                        self.caching['winner'] = self.winner
                        logger.info(f"<победитель с сайта> - {self.caching['winner']}")
                    if not self.caching['winner']:
                        logger.warning(f'поле <победитель > пустое ,{self.tender_number}')
                        logger.info(f'поле <победитель > пустое ,{self.tender_number}')
            except:
                pass
            # время публикования протокола
            try:
                self.time_protocol_pre = (
                    self.site_winner_protokol.find_all(class_='section__info')[1].get_text(strip=True))
                self.date_winner_protokol_pre = str(self.time_protocol_pre).split("(")[0]
                self.date_winner_protokol_pre_2 = re.split('\s+', str(self.time_protocol_pre))[0]
                self.date_winner_protokol_zone_pre = str(self.time_protocol_pre).split("(")[1]
                self.date_winner_protokol_zone = re.findall(r"МСК[+|-][\d]{1,2}",
                                                            str(self.date_winner_protokol_zone_pre),
                                                            flags=re.I)
                self.time_protocol = datetime.datetime.strptime(self.date_winner_protokol_pre, '%d.%m.%Y %H:%M')
                self.time_protocol_zone = datetime.datetime.strptime(self.date_winner_protokol_pre_2, '%d.%m.%Y').date()
                self.caching['time_protocol'] = self.time_protocol
                self.caching['time_zone'] = self.date_winner_protokol_zone
                if not self.caching['time_protocol']:
                    logger.warning(f'поле <время публикования протокола> пустое ,{self.tender_number}')
                    logger.info(f'поле <время публикования протокола> пустое ,{self.tender_number}')
            except:
                pass
            logger.info(f"<время публикования протокола> - {self.caching['time_protocol']}")
            yield self.caching

    def check_etp(self):

        for self.item in self.link_protokol():
            if self.item['etp_pre']:
                self.etp_up = self.item['etp_pre'].upper()
                if self.etp_up == 'АО «ЕЭТП»':
                    roseltorg.roseltorg_open_file()
                elif self.etp_up == 'АГЗ РТ':
                    # agz.agz_rt_open_file()
                    agz.agz_rt_protocol_win()
                elif self.etp_up == 'РТС-ТЕНДЕР':  # нет данных инн и адреса по эл. аукционам, брать из своей базы
                    return rts.rts_open_file()
                elif self.etp_up == 'АО «СБЕРБАНК-АСТ»':  # вообще нет данных инн и адреса брать из своей базы
                    pass
                    # sber.sber_protocol_win()
                elif self.etp_up == 'НАЦИОНАЛЬНАЯ ЭЛЕКТРОННАЯ ПЛОЩАДКА':
                    nep.nep_protocol_win()
                elif self.etp_up == 'АО "РАД"':
                    rad.rad_open_file()
                elif self.etp_up == 'ЭТП ГАЗПРОМБАНК':
                    gazprom.gazprom_protocol_win()
                elif self.etp_up == 'ЭТП ТЭК-ТОРГ':
                    tek_torg.tek_torg_open_file()

    def res_collection_(self):
        count = 0
        for self.item in self.check_etp():
            try:
                connection = psycopg2.connect(user="postgres",
                                              password="Vfrcvfrc1",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="general_lids")
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO data_for_letter(res_winner_base, tender_number, mail_company, sum_bg,"
                    "term, time_protocol, date_record) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (str(self.item['res_winner_base']), str(self.item['tender_number']), str(self.item['mail_company']),
                     str(self.item['sum_bg']), str(self.item['term']), str(self.item['time_protocol']),
                     str(self.item['date_record'])))
                connection.commit()
            except (Exception, Error) as error:
                print("Ошибка при работе с PostgreSQL", error)
                logger.info(f'<"Ошибка при работе с PostgreSQL", error> {error}')
                logger.warning(f'<"Ошибка при работе с PostgreSQL", error> {error}')
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Соединение с PostgreSQL закрыто")
            count += 1
            cprint(f' Всего записей: {count}', color='green')


class Roseltorg(Router):

    def __init__(self, url=url):
        super().__init__(url)
        self.test_dx = None

    def roseltorg_protocol_win(self):
        print(self.caching['tender_number'])
        logger.info(f" начало функции <roseltorg> ")
        for self.item in self.link_protokol():
            print(self.caching['link_winner_protokol'])
            try:
                options = webdriver.ChromeOptions()
                self.browser = webdriver.Chrome('chromedriver', options=options)
                self.browser.get(self.item['pre_links_w'])
                time.sleep(2)

                self.username_pre = self.browser.find_element_by_xpath(
                    '/html/body/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/'
                    'form/div[4]/div[2]/div/div/div/div/table/tbody/tr/td[1]/div/div/'
                    'div/div/a').click()
                time.sleep(1)
                self.browser.close()
                self.browser.quit()
            except:
                pass
            yield

    def roseltorg_open_file(self):
        for self.item in self.roseltorg_protocol_win():
            for dirpath, dirnames, filenames in os.walk(file_way):
                for file in filenames:
                    logger.info(f" чтение файла <roseltorg>")
                    if file.endswith('.pdf'):
                        logger.info(f"{self.tender_number}")
                        parsePdf.parse_inn()
                    else:
                        logger.info(f"{self.tender_number}")
                        test_dx.parse.parse_list_inn_docx()


class AgzRt(Router):
    countt = 0

    def __init__(self, url=url):
        super().__init__(url)

    def agz_rt_protocol_win(self):
        print(self.caching['tender_number'])
        logger.info(f" начало функции <agz_rt_protocol_win> ")
        for self.item in self.link_protokol():
            print(self.caching['link_winner_protokol'])
            try:
                get_site_tender = requests.get(url=self.item['pre_links_w'], headers=HEADERS)
                if get_site_tender.status_code == 200:
                    self.site_tender = BeautifulSoup(get_site_tender.text, 'lxml')
            except:
                pass
            try:
                self.etp_pre = self.site_tender.find_all(class_="view-form")
                if not self.etp_pre:
                    logger.warning(f'поле <инн> пустое ,{self.tender_number}')
                    logger.info(f'поле <инн> пустое ,{self.tender_number}')
                self.inn_table_pre = re.compile(r'(\W[\d]{10},)', flags=re.I)
                self.inn_table = self.inn_table_pre.findall(str(self.etp_pre))
                self.inn_table_pre_ip = re.compile(r'(\W[\d]{12},)', flags=re.I)
                self.inn_table_ip = self.inn_table_pre_ip.findall(str(self.etp_pre))
                if self.inn_table_ip:
                    self.inn_pre = re.sub(r"[\s|\]|\[\']", '', str(self.inn_table_ip))
                    self.inn = self.inn_pre.replace(',', '', 1)
                    self.list_inn = []
                    self.list_inn.append(self.inn)
                    logger.info(f'список <инн>,{self.list_inn},  {self.tender_number}')
                    if not self.list_inn:
                        logger.warning(f'список <инн> пустое ,{self.tender_number}')
                        logger.info(f'список <инн> пустое ,{self.tender_number}')
                elif self.inn_table:
                    self.inn_pre = re.sub(r"[\s|\]|\[\']", '', str(self.inn_table))
                    self.inn = self.inn_pre.replace(',', '', 1)
                    self.list_inn = []
                    self.list_inn.append(self.inn)
                    logger.info(f'список <инн>,{self.list_inn},  {self.tender_number}')
                    if not self.list_inn:
                        logger.warning(f'список <инн> пустое ,{self.tender_number}')
                        logger.info(f'список <инн> пустое ,{self.tender_number}')
            except:
                pass
            yield self.list_inn

    def agz_rt_inn_check_base(self):
        for self.item in self.agz_rt_protocol_win():
            # взов модуля с поиском в базе
            pass


class RtsTender(Router):
    countt = 0

    def __init__(self, url=url):
        super().__init__(url)

    def rts_protocol_win(self):
        logger.info(f" начало функции <rts_protocol_win>")
        try:
            print(self.caching['tender_number'])
            for self.item in self.link_protokol():
                print(self.caching['link_winner_protokol'])
                # parser.caching['winner']
                # print(self.pre_links)
                get_site_tender = requests.get(url=self.item['pre_links_w'], headers=HEADERS)
                if self.item['auction'] != 'ЭЛЕКТРОННЫЙ АУКЦИОН':
                    self.site_tender = BeautifulSoup(get_site_tender.text, 'lxml')
                    # print(self.site_tender)
                    self.doc_protocol = self.site_tender.find("table").find('a').get('href')
                    # print(self.doc_protocol)
                    options = webdriver.ChromeOptions()
                    self.browser = webdriver.Chrome('chromedriver', options=options)
                    self.browser.get(self.doc_protocol)
                    time.sleep(3)
                    self.browser.close()
                    self.browser.quit()
                    self.countt += 1
                    cprint(self.countt, color='green')
                else:
                    pass
                    # self.item['winner'] логика с поиском в базе
                yield
        except:
            pass

    def rts_open_file(self):
        logger.info(f" начало функции <rts_open_file> ")

        try:
            count_pdf = 0
            count_doc = 0
            for self.item in self.rts_protocol_win():
                for dirpath, dirnames, filenames in os.walk(file_way):
                    logger.info(f"чтение файла <rts_open_file> ")
                    for file in filenames:
                        if file.endswith('.pdf'):
                            res_winner_base_Pdf = parsePdf.parse_list_inn_pdf(self.caching['winner'])
                            if res_winner_base_Pdf:
                                self.caching['res_winner_base'] = res_winner_base_Pdf
                                count_pdf += 1
                                print(res_winner_base_Pdf, '======================== count_pdf', count_pdf)
                                yield self.caching
                        else:
                            res_winner_base = test_dx.parse.parse_list_inn_docx(self.caching['winner'])
                            if res_winner_base:
                                self.caching['res_winner_base'] = res_winner_base
                                count_doc += 1
                                print(res_winner_base, '======================== count_doc', count_doc)
                                yield self.caching

        except Exception as exc:
            logger.info(f"<rts_open_file>{exc}")
            logger.warning(f"<rts_open_file>{exc}")


class Sber(Router):
    def __init__(self, url=url):
        super().__init__(url)

    def sber_protocol_win(self):
        print(self.caching['link_winner_protokol'])
        try:
            print(self.caching['tender_number'])
            logger.info(f" начало функции <sber_protocol_win> ")
            for self.item in self.link_protokol():
                # self.item['winner'] логика с поиском в базе

                print('sber')
        except:
            pass


class Nep(Router):

    def __init__(self, url=url):
        super().__init__(url)

    def nep_protocol_win(self):
        try:
            print(self.caching['tender_number'])
            logger.info(f" начало функции <nep_protocol_win> ")
            for self.item in self.link_protokol():
                print(self.caching['link_winner_protokol'])
                self.get_site_protocol = requests.get(url=self.item['pre_links_w'], headers=HEADERS)
                self.site_protocol = BeautifulSoup(self.get_site_protocol.text, 'lxml')
                print(self.item['pre_links_w'], '----')
                print(self.item['tender_number'])
                for i in range(20):
                    try:
                        self.contaner = self.site_protocol.find_all('fieldset', class_='accreditationInfoFieldset')[
                            i].get_text(
                            strip=True)
                        # print(self.contaner, 'перебор')

                        # if self.contaner:
                        #     self.pars_contaner = str(self.contaner).split('(')[0]
                        #     # print(self.item['winner'], 'с сайта')
                        #     if self.pars_contaner == self.item['winner']:
                        #         print(self.contaner, 'итог победитель')
                        #     else:
                        #         logger.warning(f'поле <победитель> пустое ,{self.tender_number}')
                        #         logger.info(f'поле <победитель> пустое ,{self.tender_number}')
                        #         break
                        if self.contaner:
                            self.pars_contaner = str(self.contaner).split('(')[0]
                            x = str(self.pars_contaner).split(' ')
                            self.pars_contaner_pr = re.sub(r"[\r|\t|\n|\s|'|\\N|\]|\[]", '', str(x).upper())
                            self.pars_contaner = str(self.pars_contaner_pr).replace(',', '')
                            # self.pars_contaner = str(self.pars_contaner_pr)

                            y = str(self.item['winner']).split(' ')
                            winner_pr = re.sub(r"[\r|\t|\n|\s|'|\\N|\]|\[]", '', str(y).upper())
                            winner_pr_2 = str(winner_pr).replace(',', '')
                            if self.pars_contaner != winner_pr_2:
                                continue
                            else:
                                logger.info(f"поле <сумма договора> {self.item['sum_dogovor']}")
                                logger.info(f"<победитель с сайта> {self.item['winner']}")
                                logger.info(f"<итог победитель> {self.contaner}")
                                self.inn_pre = re.compile(r'(ИНН\W*[\d*]{10})', flags=re.I)
                                self.inn_pre_2 = self.inn_pre.findall(str(self.contaner))
                                self.inn_gaz = str(self.inn_pre_2).replace('\\xa0', ' ', )
                                self.list_inn = []
                                self.list_inn.append(self.inn_gaz)
                                logger.info(f'список <инн>,{self.list_inn},  {self.tender_number}')
                                if not self.list_inn:
                                    logger.warning(f'список <инн> пустое ,{self.tender_number}')
                                    logger.info(f'список <инн> пустое ,{self.tender_number}')

                                if not self.item['sum_dogovor']:
                                    logger.warning(f"поле <сумма договора> пустое {self.item['sum_dogovor']}")
                                    logger.info(f"поле <сумма договора> пустое {self.item['sum_dogovor']}")
                                if not self.contaner:
                                    logger.warning(f"поле <итог победитель> пустое {self.contaner}")
                    except:
                        pass
                    yield self.list_inn
        except:
            pass

    def nep_inn_check_base(self):
        for self.item in self.nep_protocol_win():
            # взов модуля с поиском в базе
            pass


class Rad(Router):
    countt = 0

    def __init__(self, url=url):
        super().__init__(url)
        self.test_dx = None

    def rad_protocol_win(self):
        host = 'https://gz.lot-online.ru'
        logger.info(f" начало функции <rad_protocol_win> ")
        for self.item in self.link_protokol():
            print(self.caching['link_winner_protokol'])
            try:
                get_site_tender = requests.get(url=self.item['pre_links_w'], headers=HEADERS)
                if get_site_tender.status_code == 200:
                    self.site_tender = BeautifulSoup(get_site_tender.text, 'lxml')
                    if self.item['auction'] == 'ЭЛЕКТРОННЫЙ АУКЦИОН':
                        logger.warning(f" процедура {self.item['auction']}")
                        logger.info(f" процедура {self.item['auction']}")
                        self.doc_protocol = host + self.site_tender.find('p', class_="upload-filename").find(
                            'a').get('href')
                        # print(self.item['auction'])
                        options = webdriver.ChromeOptions()
                        self.browser = webdriver.Chrome('chromedriver', options=options)
                        self.browser.get(self.doc_protocol)
                        time.sleep(3)
                        self.countt += 1
                        self.browser.close()
                        self.browser.quit()
                        cprint(self.countt, color='green')
                    elif self.item['ogr_conkurs'] == 'КОНКУРС С':
                        logger.warning(f" процедура {self.item['ogr_conkurs']}")
                        logger.info(f" процедура {self.item['ogr_conkurs']}")
                        # print(self.caching['ogr_conkurs'])
                        self.options = webdriver.ChromeOptions()
                        self.browser = webdriver.Chrome('chromedriver', options=self.options)
                        self.browser.get(self.item['pre_links_w'])
                        time.sleep(5)
                        self.action = ActionChains(self.browser)
                        self.action.send_keys(Keys.PAGE_DOWN * 5).perform()
                        time.sleep(1)
                        self.username_pre = self.browser.find_element_by_xpath(
                            '/html/body/app-root/div/div[2]/div/div[2]/document-id/div[1]/'
                            'document-types-prteokousummarizing/div[1]/document-fields-view[2]/fields-block-view/div/'
                            'fields-file-view/div/div/div/div/div/a')
                        time.sleep(4)
                        self.action.click(on_element=self.username_pre).perform()
                        time.sleep(3)
                        self.browser.close()
                        self.browser.quit()
                    elif self.item['conkurs'] == 'ОТКРЫТЫЙ КОНКУРС':
                        logger.info(f" процедура {self.item['conkurs']}")
                        # print(self.caching['conkurs'])
                        self.options = webdriver.ChromeOptions()
                        self.browser = webdriver.Chrome('chromedriver', options=self.options)
                        self.browser.get(self.item['pre_links_w'])
                        time.sleep(5)
                        self.action = ActionChains(self.browser)
                        self.action.send_keys(Keys.PAGE_DOWN * 5).perform()
                        time.sleep(1)
                        self.username_pre = self.browser.find_element_by_xpath(
                            '/html/body/app-root/div/div[2]/div/div[2]/document-id/div[1]/'
                            'document-types-prteoksummarizing/div[1]/document-fields-view[2]/fields-block-view/div/'
                            'fields-file-view/div/div/div/div/div/a')
                        time.sleep(4)
                        self.action.click(on_element=self.username_pre).perform()
                        time.sleep(3)
                        self.browser.close()
                        self.browser.quit()
            except:
                pass
            yield

    def rad_open_file(self):
        for self.item in self.rad_protocol_win():
            for dirpath, dirnames, filenames in os.walk(file_way):
                logger.info(f"чтение файла <rad_open_file> ")
                for file in filenames:
                    if file.endswith('.pdf'):
                        parsePdf.parse_inn()
                    else:
                        test_dx.parse.parse_list_inn_docx()


class Gazprom(Router):

    def __init__(self, url=url):
        super().__init__(url)

    def gazprom_protocol_win(self):
        try:
            logger.info(f" начало функции <gazprom_protocol_win> ")
            for self.item in self.link_protokol():

                self.get_site_protocol = requests.get(url=self.item['pre_links_w'], headers=HEADERS)
                self.site_protocol = BeautifulSoup(self.get_site_protocol.text, 'lxml')
                print(self.caching['tender_number'])
                print(self.item['pre_links_w'], '----')
                print(self.caching['link_winner_protokol'])
                if self.item['auction'] == 'ЭЛЕКТРОННЫЙ АУКЦИОН':
                    logger.info(f"проедура {self.item['auction']} ")
                    time.sleep(0.3)
                    for i in range(20):
                        try:
                            self.contaner = self.site_protocol.find_all('fieldset', class_='accreditationInfoFieldset')[
                                i].get_text(
                                strip=True)
                            #  определяем инн победителя чистим от пробелов названия для сравнения
                            if self.contaner:
                                self.pars_contaner = str(self.contaner).split('(')[0]
                                x = str(self.pars_contaner).split(' ')
                                self.pars_contaner_pr = re.sub(r"[\r|\t|\n|\s|'|\\N|\]|\[]", '', str(x).upper())
                                self.pars_contaner = str(self.pars_contaner_pr).replace(',', '')
                                # self.pars_contaner = str(self.pars_contaner_pr)

                                y = str(self.item['winner']).split(' ')
                                winner_pr = re.sub(r"[\r|\t|\n|\s|'|\\N|\]|\[]", '', str(y).upper())
                                winner_pr_2 = str(winner_pr).replace(',', '')
                                if self.pars_contaner != winner_pr_2:
                                    continue
                                else:
                                    logger.info(f"поле <сумма договора> {self.item['sum_dogovor']}")
                                    logger.info(f"<победитель с сайта> {self.item['winner']}")
                                    logger.info(f"<итог победитель> {self.contaner}")
                                    self.inn_pre = re.compile(r'(ИНН\W*[\d*]{10})', flags=re.I)
                                    self.inn_pre_2 = self.inn_pre.findall(str(self.contaner))
                                    self.inn_gaz = str(self.inn_pre_2).replace('\\xa0', ' ', )
                                    self.list_inn = []
                                    self.list_inn.append(self.inn_gaz)
                                    logger.info(f'список <инн>,{self.list_inn},  {self.tender_number}')
                                    if not self.list_inn:
                                        logger.warning(f'список <инн> пустое ,{self.tender_number}')
                                        logger.info(f'список <инн> пустое ,{self.tender_number}')
                                    if not self.item['sum_dogovor']:
                                        logger.warning(f"поле <сумма договора> пустое {self.item['sum_dogovor']}")
                                        logger.info(f"поле <сумма договора> пустое {self.item['sum_dogovor']}")
                                    if not self.contaner:
                                        logger.warning(f"поле <итог победитель> пустое {self.contaner}")
                        except:
                            pass
                        yield self.list_inn
                else:
                    for i in range(20):
                        try:
                            self.contaner = self.site_protocol.find_all('fieldset', class_='decisions-accreditation')[
                                i].get_text(
                                strip=True)
                            # print(self.contaner, 'перебор закупок')
                            if self.contaner:
                                self.pars_contaner = str(self.contaner).split('(')[0]
                                # print(self.item['winner'], 'с сайта')
                                if self.pars_contaner == self.item['winner']:
                                    logger.info(f"поле <сумма договора> {self.item['sum_dogovor']}")
                                    logger.info(f"<победитель с сайта> {self.item['winner']}")
                                    logger.info(f"<итог победитель> {self.contaner}")
                                    self.inn_pre = re.compile(r'(ИНН\W*[\d*]{10})', flags=re.I)
                                    self.inn_pre_2 = self.inn_pre.findall(str(self.contaner))
                                    self.inn_gaz = str(self.inn_pre_2).replace('\\xa0', ' ', )
                                    self.list_inn = []
                                    self.list_inn.append(self.inn_gaz)
                                    logger.info(f'список <инн>,{self.list_inn},  {self.tender_number}')
                                    if not self.list_inn:
                                        logger.warning(f'список <инн> пустое ,{self.tender_number}')
                                        logger.info(f'список <инн> пустое ,{self.tender_number}')
                        except:
                            pass
                        yield self.list_inn
        except:
            pass

    def gazprom_inn_check_base(self):
        for self.item in self.gazprom_protocol_win():
            # взов модуля с поиском в базе
            pass


class TekTorg(Router):
    countt = 0

    def __init__(self, url=url):
        super().__init__(url)
        self.test_dx = None

    def tek_torg_protocol_win(self):
        logger.info(f" начало функции <tek_torg_protocol_win> ")
        for self.item in self.link_protokol():
            print(self.caching['tender_number'])
            print(self.caching['link_winner_protokol'])
            try:
                options = webdriver.ChromeOptions()
                self.browser = webdriver.Chrome('chromedriver', options=options)
                self.browser.get(self.item['pre_links_w'])
                time.sleep(2)
                self.browser.close()
                self.browser.quit()
            except:
                pass
            yield

    def tek_torg_open_file(self):
        for self.item in self.tek_torg_protocol_win():
            for dirpath, dirnames, filenames in os.walk(file_way):
                logger.info(f"чтение файла <tek_torg_open_file> ")
                for file in filenames:
                    if file.endswith('.pdf'):
                        parsePdf.parse_inn()
                    else:
                        test_dx.parse.parse_list_inn_docx()

parser = Parser()
router = Router()
roseltorg = Roseltorg()
agz = AgzRt()
rts = RtsTender()
sber = Sber()
nep = Nep()
rad = Rad()
gazprom = Gazprom()
tek_torg = TekTorg()
if __name__ == '__main__':
    # router.check_etp()
    router.res_collection_()

# if __name__ == '__main__':
# roseltorg.open_file()
# agz.open_file()
# delete_file()
