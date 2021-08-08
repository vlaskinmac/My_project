# -*- coding: utf-8 -*-
import csv
import re
import time
from datetime import timedelta
import datetime
from random import random
import psycopg2
from psycopg2 import Error
import psycopg2
import requests
from bs4 import BeautifulSoup
# import datetime
from termcolor import cprint

from My_Work.My_first.Banks import mod_logger
from My_Work.My_first.Banks.decorators import time_track

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

# start_search = datetime.now().strftime('%d.%m.%Y')

# start_end_date = '10.01.2019'

logger = mod_logger.get_logger(__name__)
# logging.disable(logging.INFO)
collection_dict = {}
collection_list_data = []


class ParserBase:
    count_ip = 0

    def __init__(self, collection_dict, collection_list_data):
        self.collection_dict = collection_dict
        self.collection_list_data = collection_list_data

    def date_generator(self):

        # start_date = '09.01.2019'
        # date_time_obj = datetime.strptime(start_date, '%d.%m.%Y')
        # today_date = datetime.now()
        # period_pre = today_date - date_time_obj
        # period = str(period_pre.days)
        # print(period)

        # test date
        start_date = '09.01.2019'
        date_time_obj = datetime.datetime.strptime(start_date, '%d.%m.%Y')

        today_date = '11.01.2019'
        today_date_time_obj = datetime.datetime.strptime(today_date, '%d.%m.%Y')
        period_pre = today_date_time_obj - date_time_obj
        period = str(period_pre.days)
        print(period)

        for i in range(int(period)):
            date_time_obj += timedelta(1)
            step_date = date_time_obj.strftime('%d.%m.%Y')
            self.collection_dict['step_date'] = step_date
            yield self.collection_dict

    def start_base(self):
        start_date_generator = self.date_generator()
        for self.item in start_date_generator:
            print('дата:', self.item['step_date'])
            self.pagina = 1
            while True:
                pagination = f'{self.pagina}'
                url = f'https://zakupki.gov.ru/epz/eruz/search/results.html?morphology=on&search-filter=Дате+размещения' \
                      f'&sortBy=BY_REGISTRY_DATE&pageNumber={pagination}&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&' \
                      f'participantType_0=on&participantType_1=on&participantType_2=on&participantType_3=on&participantType_4=on&' \
                      f'participantType_5=on&participantType_6=on&participantType_7=on&participantType=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7&' \
                      f'registered=on&rejectReasonIdNameHidden=%7B%7D&countryRegIdNameHidden=%7B%7D&' \
                      f'registryDateFrom={self.item["step_date"]}&registryDateTo={self.item["step_date"]}'
                try:
                    self.base_html_code = requests.get(url, headers=HEADERS)
                    if self.base_html_code.status_code == 200:
                        self.soup = BeautifulSoup(self.base_html_code.text, 'lxml')
                except:
                    print('Нет соединения')
                try:
                    # блок с ссылками
                    self.contaner_with_links = self.soup.find_all(
                        class_='search-registry-entry-block box-shadow-search-input')
                    if self.contaner_with_links:
                        for self.item in self.contaner_with_links:
                            # ссылка записи
                            self.pre_links = HOST + self.item.find(class_='registry-entry__header-mid__number').find(
                                'a').get('href')
                            self.collection_dict['pre_links'] = self.pre_links
                            yield self.collection_dict
                except:
                    logger.info(f'<ошибка контента>')
                    logger.warning(f'<ошибка контента>')
                if not self.contaner_with_links:
                    logger.info(f'<нет контента>')
                    logger.warning(f'<нет контента>')
                    break
                cprint(f'страница {self.pagina}', color='cyan')
                self.pagina += 1

    def get_data_(self):
        links_url = self.start_base()
        for self.item in links_url:
            try:
                self.get_site = requests.get(url=self.item['pre_links'], headers=HEADERS)
                # time.sleep(random.randint(1))
                self.site = BeautifulSoup(self.get_site.text, 'lxml')
                self.collection_dict['site'] = self.site
            except:
                logger.info(f'<ошибка нет сайта> {self.item["pre_links"]}')
                logger.warning(f'<ошибка нет сайта> {self.item["pre_links"]}')
            yield self.collection_dict

    def name_company_(self):

        for self.item in self.get_data_():
            # название компании
            try:
                self.name_company = self.item['site'].find_all(class_='cardMainInfo__section')[0].find('a').get_text(
                    strip=True)
                if not self.name_company:
                    self.name_company = self.item['site'].find_all('span', class_='section__info')[5].get_text(
                        strip=True)
                    self.collection_dict['name_company'] = self.name_company
                else:
                    self.collection_dict['name_company'] = self.name_company
            except:
                logger.info(f'<ошибка название компании> {self.item["pre_links"]}')
                logger.warning(f'<ошибка название компании> {self.item["pre_links"]}')
            yield self.collection_dict

    def inn_company_(self):
        for self.item in self.name_company_():
            try:  # инн
                self.inn_company = self.item['site'].find_all('span', class_='cardMainInfo__content')[1].get_text(
                    strip=True)
                # if not self.inn_company:
                #     self.inn_company = self.item['site'].find_all('span', class_='section__info')[6].get_text(
                #         strip=True)
                #     self.collection_dict['inn_company'] = self.inn_company
                #     yield self.collection_dict
                # else:
                self.collection_dict['inn_company'] = self.inn_company
            except:
                logger.info(f'<ошибка inn> {self.collection_dict["pre_links"]}')
                logger.warning(f'<ошибка inn> {self.collection_dict["pre_links"]}')
            yield self.collection_dict

    def kpp_company_(self):
        for self.item in self.inn_company_():
            try:  # kpp
                self.kpp_company = self.item['site'].find_all('span', class_='cardMainInfo__content')[2].get_text(
                    strip=True)
                if len(self.kpp_company) != 9:
                    self.collection_dict['kpp_company'] = None
                else:
                    if len(self.kpp_company) == 9:
                        self.collection_dict['kpp_company'] = self.kpp_company
            except:
                logger.info(f'<ошибка kpp> {self.item["pre_links"]}')
                logger.warning(f'<ошибка kpp> {self.item["pre_links"]}')
            yield self.collection_dict

    def ogrn_company_(self):
        for self.item in self.kpp_company_():
            try:
                try:  # ogrn
                    self.ogrn_company = self.item['site'].find_all('span', class_='cardMainInfo__content')[3].get_text(
                        strip=True)
                    if not self.ogrn_company:
                        self.collection_dict['ogrn_company'] = None
                    else:
                        self.collection_dict['ogrn_company'] = self.ogrn_company
                except:
                    self.ogrn_company = self.item['site'].find_all('span', class_='section__info')[7].get_text(
                        strip=True)
                    if re.findall(r'([\d+]{15})', str(self.ogrn_company)):
                        self.collection_dict['ogrn_company'] = self.ogrn_company
                        self.count_ip += 1
            except:
                logger.info(f'<ошибка ogrn> {self.item["pre_links"]}')
                logger.warning(f'<ошибка ogrn> {self.item["pre_links"]}')
            yield self.collection_dict

    def registration_date_start_(self):
        for self.item in self.ogrn_company_():
            try:
                try:  # registration_date_start
                    self.registration_date_start_pre = \
                    self.item['site'].find_all('span', class_='cardMainInfo__content')[
                        4].get_text(strip=True)
                    self.registration_date_start = datetime.datetime.strptime(self.registration_date_start_pre,
                                                                              '%d.%m.%Y')
                    self.collection_dict['registration_date_start'] = self.registration_date_start
                except:
                    self.inn_company = self.item['site'].find_all('span', class_='section__info')[3].get_text(
                        strip=True)
                    self.collection_dict['registration_date_start'] = self.registration_date_start
            except:
                logger.info(f'<ошибка registration_date_start> {self.item["pre_links"]}')
                logger.warning(f'<ошибка registration_date_start> {self.item["pre_links"]}')
            yield self.collection_dict

    def registration_date_end_(self):
        for self.item in self.registration_date_start_():
            try:  # registration_date_end
                registration_date_end_pre = self.item['site'].find_all('span', class_='section__info')[4].get_text(
                    strip=True)
                registration_date_end_pre_1 = re.compile(r'[\d+]{2}\.[\d+]{2}\.[\d+]{4}', flags=re.I)
                registration_date_end_pre_2 = registration_date_end_pre_1.findall(str(registration_date_end_pre))
                if not registration_date_end_pre_2:
                    registration_date_end_pre = self.item['site'].find_all('span', class_='section__info')[5].get_text(
                        strip=True)
                    registration_date_end_pre_1 = re.compile(r'[\d+]{2}\.[\d+]{2}\.[\d+]{4}', flags=re.I)
                    registration_date_end_pre_2 = registration_date_end_pre_1.findall(str(registration_date_end_pre))
                    self.registration_date_end_pre_3 = re.sub(r'[\[|]|\'|]', '', str(registration_date_end_pre_2))
                    self.registration_date_end = datetime.datetime.strptime(self.registration_date_end_pre_3, '%d.%m.%Y'
                                                                            )
                    self.collection_dict['registration_date_end'] = self.registration_date_end
                elif not registration_date_end_pre_2:
                    registration_date_end_pre = self.item['site'].find_all('span', class_='section__info')[3].get_text(
                        strip=True)
                    registration_date_end_pre_1 = re.compile(r'[\d+]{2}\.[\d+]{2}\.[\d+]{4}', flags=re.I)
                    registration_date_end_pre_2 = registration_date_end_pre_1.findall(str(registration_date_end_pre))
                    self.registration_date_end_3 = re.sub(r'[\[|]|\'|]', '', str(registration_date_end_pre_2))
                    self.registration_date_end = datetime.datetime.strptime(self.registration_date_end_3, '%d.%m.%Y')
                    self.collection_dict['registration_date_end'] = self.registration_date_end
                else:
                    self.registration_date_end_5 = re.sub(r'[\[|]|\'|]', '', str(registration_date_end_pre_2))
                    self.registration_date_end = datetime.datetime.strptime(self.registration_date_end_5, '%d.%m.%Y')
                    self.collection_dict['registration_date_end'] = self.registration_date_end
            except:
                try:
                    registration_date_end_pre = self.item['site'].find_all('span', class_='section__info')[4].get_text(
                        strip=True)
                    registration_date_end_pre_1 = re.compile(r'[\d+]{2}\.[\d+]{2}\.[\d+]{4}', flags=re.I)
                    registration_date_end_pre_2 = registration_date_end_pre_1.findall(str(registration_date_end_pre))
                    self.registration_date_end = re.sub(r'[\[|]|\'|]', '', str(registration_date_end_pre_2))
                    self.collection_dict['registration_date_end'] = self.registration_date_end
                except:
                    logger.info(f'<ошибка registration_date_end> {self.item["pre_links"]}')
                    logger.warning(f'<ошибка registration_date_end> {self.item["pre_links"]}')
            try:
                self.date_now = datetime.datetime.now().date()
                self.collection_dict['date_record'] = self.date_now
            except:
                pass
            yield self.collection_dict

    def adress_company_(self):
        for self.item in self.registration_date_end_():
            try:  # adress_company
                self.adress_company = self.item['site'].find_all('span', class_='section__info')[7].get_text(strip=True)
                if str(self.adress_company).isdigit():
                    self.collection_dict['adress_company'] = None
                else:
                    self.collection_dict['adress_company'] = self.adress_company
                    adress_index_company_pre = str(self.adress_company).split(',')[0]
                    if re.findall(r'([\d+]{6})', str(adress_index_company_pre)):
                        self.collection_dict['adress_index_company'] = int(adress_index_company_pre)
            except:
                logger.info(f'<ошибка adress_company> {self.item["pre_links"]}')
                logger.warning(f'<ошибка adress_company> {self.item["pre_links"]}')
            yield self.collection_dict
    def boss_company_(self):
        for self.item in self.adress_company_():
            try:  # boss_company
                self.boss_company = self.item['site'].find_all('tr', class_='tableBlock__row')[1].find_all('td')[0] \
                    .get_text(strip=True)
                self.collection_dict['boss_company'] = self.boss_company
            except Exception as exc:
                if 'list' in exc.args[0]:
                    self.collection_dict['boss_company'] = None
            yield self.collection_dict

    def mail_company_(self):
        for self.item in self.boss_company_():
            try:
                try:  # mail_company
                    self.mail_company = self.item['site'].find_all('span', class_='section__info')[15].get_text(
                        strip=True)
                    if not re.findall(r'\w+\@\S+\.\w+', self.mail_company, flags=re.I):
                        self.mail_company = self.item['site'].find_all('span', class_='section__info')[14].get_text(
                            strip=True)
                        if re.findall(r'\w+\@\S+\.\w+', self.mail_company, flags=re.I):
                            self.collection_dict['mail_company'] = self.mail_company
                    elif not re.findall(r'\w+\@\S+\.\w+', self.mail_company, flags=re.I):
                        self.mail_company = self.item['site'].find_all('span', class_='section__info')[16].get_text(
                            strip=True)
                        if re.findall(r'\w+\@\S+\.\w+', self.mail_company, flags=re.I):
                            self.collection_dict['mail_company'] = self.mail_company
                    else:
                        self.mail_company = self.mail_company
                        if re.findall(r'\w+\@\S+\.\w+', self.mail_company, flags=re.I):
                            self.collection_dict['mail_company'] = self.mail_company
                except:
                    self.mail_company = self.item['site'].find_all('span', class_='section__info')[11].get_text(
                        strip=True)
                    if re.findall(r'\w+\@\S+\.\w+', self.mail_company, flags=re.I):
                        self.mail_company = self.mail_company
                        self.collection_dict['mail_company'] = self.mail_company
            except:
                logger.info(f'<ошибка mail_company> {self.item["pre_links"]}')
                logger.warning(f'<ошибка mail_company> {self.item["pre_links"]}')
            yield self.collection_dict

    def tel_company_(self):

        for self.item in self.mail_company_():
            try:
                try:  # tel_company
                    self.tel_company = self.item['site'].find_all('span', class_='section__info')[16].get_text(
                        strip=True)
                    self.tel_company = self.tel_company.replace(' ', '')
                    pick_tel_company_pattern = re.compile(r'[\d+]{10,11}', flags=re.I)
                    pick_tel_company = pick_tel_company_pattern.findall(str(self.tel_company))
                    if not pick_tel_company:
                        self.tel_company = self.item['site'].find_all('span', class_='section__info')[15].get_text(
                            strip=True)
                        self.tel_company = self.tel_company.replace(' ', '')
                        pick_tel_company_pattern = re.compile(r'[\d+]{10,11}', flags=re.I)
                        self.tel_company = pick_tel_company_pattern.findall(str(self.tel_company))
                        self.tel_company = re.sub(r"[\W]", '', str(self.tel_company))
                        self.collection_dict['tel_company'] = self.tel_company
                    else:
                        self.tel_company = re.sub(r"[\W]", '', str(self.tel_company))
                        self.collection_dict['tel_company'] = self.tel_company
                except Exception as exc:
                    if 'list' in exc.args[0]:
                        self.collection_dict['tel_company'] = None
            except:
                logger.info(f'<ошибка tel_company> {self.item["pre_links"]}')
                logger.warning(f'<ошибка tel_company> {self.item["pre_links"]}')
            yield self.collection_dict

    # @time_track
    def res_collection_(self):
        count = 1
        tel_company = self.tel_company_()
        for self.item in tel_company:
            try:
                connection = psycopg2.connect(user="postgres",
                                              password="Vfrcvfrc1",
                                              host="127.0.0.1",
                                              port="5432",
                                              database="general_lids")

                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO no_validate_lids(name_company, inn_company,  mail_company, tel_company,"
                    " kpp_company, ogrn_company, registration_date_start, registration_date_end,"
                    "adress_company, adress_index_company, boss_company, date_record) VALUES (%s, %s, %s, %s,"
                    " %s, %s, %s, %s, %s, %s, %s, %s)",
                    (str(self.item['name_company']), str(self.item['inn_company']), str(self.item['mail_company']),
                     str(self.item['tel_company']), str(self.item['kpp_company']), str(self.item['ogrn_company']),
                     str(self.item['registration_date_start']), str(self.item['registration_date_end']),
                     str(self.item['adress_company']), str(self.item['adress_index_company']),
                     str(self.item['boss_company']), str(self.item['date_record'])))
                # , str(self.item['date_record']), str(self.item['time_zone']))))
                cprint(f'ИП: {self.count_ip}', color='yellow')
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


parse_base = ParserBase(collection_dict, collection_list_data)


def main():
    parse_base.res_collection_()


if __name__ == '__main__':
    main()


def table_crud():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="Vfrcvfrc1",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="general_lids")
        cursor = connection.cursor()

        # # TODO Удалить таблицу
        # delete_query = """DROP TABLE no_validate_lids"""
        # cursor.execute(delete_query)
        # connection.commit()
        # count = cursor.rowcount
        # print(count, "Таблица успешно удалена")

        # TODO Создать таблицу
        # create_table_query = '''CREATE TABLE data_for_letter
        #                            (id SERIAL PRIMARY KEY,
        #                            res_winner_base TEXT,
        #                            tender_number TEXT,
        #                            mail_company TEXT,
        #                            sum_bg TEXT,
        #                            term TEXT,
        #                            time_protocol TEXT,
        #                            date_record TEXT);'''
        #
        # # Выполнение команды: это создает новую таблицу
        # cursor.execute(create_table_query)
        # connection.commit()
        # print("Таблица успешно создана в PostgreSQL")

        # TODO в столбик вывод
        # cursor.execute("SELECT adress_company from no_validate_lids")
        # for i in cursor:
        # print(i)
        # count += 1
        # print("Результат")
        # connection.commit()
        # print(f'{count}')
        # print()

        # cursor.execute("SELECT * from lids")
        # # TODO Результат записи
        # record = cursor.fetchall()
        # print("Результат", record)
        # TODO Результат простого запроса с разделением строк
        # print("Результат", cursor.fetchall())
        # print(connection.get_dsn_parameters(), "\n")

        # TODO обновить запись
        # count = 0
        # x = "'347909 ОБЛ РОСТОВСКАЯ61 Г ТАГАНРОГ УЛ СОЦИАЛИСТИЧЕСКАЯ'"
        # update_query = f"""UPDATE no_validate_lids SET adress_company = {x}  WHERE id = 5"""
        # cursor.execute(update_query)
        # connection.commit()
        # count = cursor.rowcount
        # print(count, "Запись успешно обновлена")

        # # TODO запись в файл таблицы с заголовками
        # sql = "COPY(SELECT inn_company FROM no_validate_lids) TO STDOUT WITH (FORMAT CSV, HEADER, DELIMITER ';')"
        # with open("table.csv", "w") as file:
        #     cursor.copy_expert(sql, file)

        # TODO Удалить запись
        # delete_query = """Delete from data_for_later where id = 7"""
        # cursor.execute(delete_query)
        # connection.commit()
        # count = cursor.rowcount
        # print(count, "Запись успешно удалена")

        # TODO Получить список таблиц в базе
        # cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        # for i in cursor:
        #     print(i)


    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

# table_crud()


# TODO запись в файл
# with open(file_base, 'w', newline='', encoding='cp1251') as file:
#     writer = csv.writer(file, delimiter=';')
#     writer.writerow(['Название компании', 'ИНН', 'КПП', 'ОГРН', 'Телефон', 'Email', 'Регистрация от',
#                      'Регистрация по', 'Адрес компании', 'Руководитель'
#                      ])
#     try:
#         for item in self.collection_list_data:
#             writer.writerow(
#                 [item['name_company'], item['inn_company'], item['kpp_company'], item['ogrn_company'],
#                  item['tel_company'], item['mail_company'], item['registration_date_start'],
#                  item['registration_date_end'], item['adress_company'], item['boss_company'],
#                  ])
#     except Exception:
#         pass
#
#     count += 1
#
#     cprint(f'ИП: {self.count_ip}', color='yellow')
#     cprint(f' Всего записей: {count}', color='green')


# ----------------------------------------------------------

# count_b = 1
# try:
#
#     self.collection_list_data.append(
#         {
#             'name_company': str(self.item['name_company']),
#             'inn_company': str(self.item['inn_company']),
#             'kpp_company': str(self.item['kpp_company']),
#             'ogrn_company': str(self.item['ogrn_company']),
#             'registration_date_start': str(self.item['registration_date_start']),
#             'registration_date_end': str(self.item['registration_date_end']),
#             'adress_company': str(self.item['adress_company']),
#             'boss_company': str(self.item['boss_company']),
#             'mail_company': str(self.item['mail_company']),
#             'tel_company': str(self.item['tel_company']),
#         }
#     )
# except:
#     logger.info(f'<ошибка общая> {self.item["pre_links"]}')
#     logger.warning(f'<ошибка общая> {self.item["pre_links"]}')
# for self.item in self.collection_list_data:

# try:
# #     # TODO запись в базу данных 'database_parse'
#     connection = psycopg2.connect(user="postgres",
#                                   password="Vfrcvfrc1",
#                                   host="127.0.0.1",
#                                   port="5432",
#                                   database="database_parse")
#
#     cursor = connection.cursor()
#     count = 1
#     for item in all_links:
#         cursor.execute("INSERT INTO lids (name_company, inn_company,  mail_company, tel_company, kpp_company, ogrn_company, registration_date_start, registration_date_end,"
#                        "adress_company, boss_company,) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                        (self.item['name_company'], self.item['inn_company'], self.item['mail_company'], self.item['tel_company'],
#                         self.item['kpp_company'], self.item['ogrn_company'], self.item['registration_date_start'], self.item['registration_date_end'], self.item['adress_company'],
#                         self.item['boss_company']))
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
