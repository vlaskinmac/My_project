# -*- coding: utf-8 -*-
import random
import re
import time
from psycopg2 import Error
import csv
import psycopg2
import requests
from bs4 import BeautifulSoup
import mod_logger

logger = mod_logger.get_logger(__name__)
# logging.disable(logging.INFO)


HEADERS = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216'
                  ' YaBrowser/21.5.4.610 Yowser/2.5 Safari/537.36'
}


class CheckInnYa:
    catch_data = {}

    def __init__(self, pre_dict=None, name_winner_pre=None, inn_index=None, name_winner=None, catch_data=catch_data,
                 list_links=None, list_inn=None,
                 links=None):

        self.pre_dict = pre_dict
        self.links = links
        self.list_inn = list_inn
        self.list_links = list_links
        self.catch_data = catch_data
        self.inn_index = inn_index
        self.name_winner = name_winner
        self.name_winner_pre = name_winner_pre

    def check_base_info(self):
        logger.info(f" начало <get_first_links>")
        self.list_links = []
        try:
            inn_ooo_pre = re.findall(r'\W[\d+]{10}\W', str(self.inn_index), flags=re.I)
            self.inn_ooo = re.sub(r"[\t\s)\[\]'(\"\\]", '', str(inn_ooo_pre), flags=re.I)

            index_ooo_pre = re.findall(r'\W[\d+]{6}\W', str(self.inn_index), flags=re.I)
            self.index_ooo = re.sub(r"[\t\s)\[\]'(\"\\><-]", '', str(index_ooo_pre), flags=re.I)
            if re.findall(r'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', str(self.name_winner_pre)):
                if self.inn_ooo:
                    for item in self.inn_ooo.split(','):
                        print('inn_search----', item)

                elif self.index_ooo:
                    for item in self.index_ooo.split(','):
                        if len(str(item)) == 6:
                            index_search = f'инн ООО{self.name_winner} Юридический адрес {item},'
                            self.data_search = index_search
                            print('index_search----', self.data_search)
            else:
                inn_ip_pre = re.findall(r'\W[\d+]{12}\W', str(self.inn_index), flags=re.I)
                inn_ip = re.sub(r"[\t\s)\[\]'(\"]", '', str(inn_ip_pre), flags=re.I)
                if inn_ip:
                    for item in inn_ip.split(','):
                        inn_search = f'инн {item}'
                        self.data_search = inn_search
                        print('inn_ip_search----', self.data_search)

        except:
            pass
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

    def get_first_links(self):
        logger.info(f" начало <get_first_links>")
        self.list_links = []
        try:
            inn_ooo_pre = re.findall(r'\W[\d+]{10}\W', str(self.inn_index), flags=re.I)
            self.inn_ooo = re.sub(r"[\t\s)\[\]'(\"\\]", '', str(inn_ooo_pre), flags=re.I)

            index_ooo_pre = re.findall(r'\W[\d+]{6}\W', str(self.inn_index), flags=re.I)
            self.index_ooo = re.sub(r"[\t\s)\[\]'(\"\\><-]", '', str(index_ooo_pre), flags=re.I)
            if re.findall(r'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ', str(self.name_winner_pre)):
                if self.inn_ooo:
                    for item in self.inn_ooo.split(','):
                        inn_search = f'инн {item}'
                        self.data_search = inn_search
                        print('inn_search----', self.data_search)
                        self.url = f'https://www.google.com/search?q={self.data_search}&newwindow=1&' \
                                   f'ei=i1jsYNjsIISgjgaN5bmYBg&oq={self.data_search}'
                        try:
                            self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                            time.sleep(random.randint(1, 3))
                            if self.sourse_open.status_code != 200:
                                logger.info(f'<гугл не отвечает> {self.sourse_open}')
                                logger.warning(f'<гугл не отвечает> {self.sourse_open}')
                        except:
                            pass
                        self.soup = BeautifulSoup(self.sourse_open.text, 'lxml')
                        self.links_resurses = self.soup.find_all(class_='yuRUbf')
                        for link in self.links_resurses:
                            self.links = link.find('a').get('href')
                            self.list_links.append(self.links)
                            yield self.links
                elif self.index_ooo:
                    for item in self.index_ooo.split(','):
                        if len(str(item)) == 6:
                            index_search = f'инн ООО{self.name_winner} Юридический адрес {item},'
                            self.data_search = index_search
                            print('index_search----', self.data_search)
                            self.url = f'https://www.google.com/search?q={self.data_search}&newwindow=1&' \
                                       f'ei=i1jsYNjsIISgjgaN5bmYBg&oq={self.data_search}'
                            try:
                                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                                time.sleep(random.randint(1, 3))
                                if self.sourse_open.status_code != 200:
                                    logger.info(f'<гугл не отвечает> {self.sourse_open}')
                                    logger.warning(f'<гугл не отвечает> {self.sourse_open}')
                            except Exception as exc:
                                logger.info(f'<ошибка> {exc}')
                                logger.warning(f'<ошибка> {exc}')
                            self.soup = BeautifulSoup(self.sourse_open.text, 'lxml')
                            self.links_resurses = self.soup.find_all(class_='yuRUbf')
                            for link in self.links_resurses:
                                self.links = link.find('a').get('href')
                                self.list_links.append(self.links)
                                yield self.links
            else:
                inn_ip_pre = re.findall(r'\W[\d+]{12}\W', str(self.inn_index), flags=re.I)
                inn_ip = re.sub(r"[\t\s)\[\]'(\"]", '', str(inn_ip_pre), flags=re.I)
                if inn_ip:
                    for item in inn_ip.split(','):
                        inn_search = f'инн {item}'
                        self.data_search = inn_search
                        print('inn_ip_search----', self.data_search)
                        self.url = f'https://www.google.com/search?q={self.data_search}&newwindow=1&' \
                                   f'ei=i1jsYNjsIISgjgaN5bmYBg&oq={self.data_search}'
                        try:
                            self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                            time.sleep(random.randint(1, 3))
                            if self.sourse_open.status_code != 200:
                                logger.info(f'<гугл не отвечает> {self.sourse_open}')
                                logger.warning(f'<гугл не отвечает> {self.sourse_open}')
                        except Exception as exc:
                            logger.info(f'<ошибка> {exc}')
                            logger.warning(f'<ошибка> {exc}')
                        self.soup = BeautifulSoup(self.sourse_open.text, 'lxml')
                        self.links_resurses = self.soup.find_all(class_='yuRUbf')
                        for link in self.links_resurses:
                            self.links = link.find('a').get('href')
                            self.list_links.append(self.links)
                            yield self.links
        except:
            pass

    def parse_router_site(self):
        self.pre_dict = {}
        logger.info(f'<начало работы>--parse_router_site')

        try:
            for self.links in self.get_first_links():
                links_site_pars_pre_1 = re.compile(r"synapsenet.ru", flags=re.I)
                links_site_pars_pre_2 = re.compile(r"list-org.com", flags=re.I)
                links_site_pars_pre_3 = re.compile(r"zachestnyibiznes.ru", flags=re.I)
                links_site_pars_pre_4 = re.compile(r"upvacancy.ru", flags=re.I)
                links_site_pars_pre_5 = re.compile(r"checko.ru", flags=re.I)
                links_site_pars_pre_6 = re.compile(r"comfex.ru", flags=re.I)
                links_site_pars_pre_7 = re.compile(r"complan.pro", flags=re.I)
                links_site_pars_pre_8 = re.compile(r"kontragent.pro", flags=re.I)
                links_site_pars_pre_9 = re.compile(r"rusprofile.ru", flags=re.I)
                links_site_pars_pre_10 = re.compile(r"vypiska-nalog.com", flags=re.I)
                links_site_pars_pre_11 = re.compile(r"1cont.ru", flags=re.I)

                site_pars_1 = links_site_pars_pre_1.findall(str(self.links))
                if site_pars_1:
                    self.pre_dict['synapsenet'] = self.links
                    yield self.pre_dict['synapsenet'], site_pars_1
                site_pars_2 = links_site_pars_pre_2.findall(str(self.links))
                if site_pars_2:
                    self.pre_dict['list-org'] = self.links
                    yield self.pre_dict['list-org'], site_pars_2
                site_pars_3 = links_site_pars_pre_3.findall(str(self.links))
                if site_pars_3:
                    self.pre_dict['zachestnyibiznes'] = self.links
                    yield self.pre_dict['zachestnyibiznes'], site_pars_3
                site_pars_4 = links_site_pars_pre_4.findall(str(self.links))
                if site_pars_4:
                    self.pre_dict['upvacancy'] = self.links
                    yield self.pre_dict['upvacancy'], site_pars_4
                site_pars_5 = links_site_pars_pre_5.findall(str(self.links))
                if site_pars_5:
                    self.pre_dict['checko'] = self.links
                    yield self.pre_dict['checko'], site_pars_5
                site_pars_6 = links_site_pars_pre_6.findall(str(self.links))
                if site_pars_6:
                    self.pre_dict['comfex'] = self.links
                    yield self.pre_dict['comfex'], site_pars_6
                site_pars_7 = links_site_pars_pre_7.findall(str(self.links))
                if site_pars_7:
                    self.pre_dict['complan'] = self.links
                    yield self.pre_dict['complan'], site_pars_7
                site_pars_8 = links_site_pars_pre_8.findall(str(self.links))
                if site_pars_8:
                    self.pre_dict['kontragent'] = self.links
                    yield self.pre_dict['kontragent'], site_pars_8
                site_pars_9 = links_site_pars_pre_9.findall(str(self.links))
                if site_pars_9:
                    self.pre_dict['rusprofile'] = self.links
                    yield self.pre_dict['rusprofile'], site_pars_9
                site_pars_10 = links_site_pars_pre_10.findall(str(self.links))
                if site_pars_10:
                    self.pre_dict['vypiska'] = self.links
                    yield self.pre_dict['vypiska'], site_pars_10
                site_pars_11 = links_site_pars_pre_11.findall(str(self.links))
                if site_pars_11:
                    self.pre_dict['1cont'] = self.links
                    yield self.pre_dict['1cont'], site_pars_11
        except:
            logger.info(f'<ошибка получения ссылок> {self.pre_dict}')
            logger.warning(f'<ошибка получения ссылок> {self.pre_dict}')

    def checking_google(self):
        logger.info(f'<начало работы>--checking_google')
        try:
            for links, site_pars in self.parse_router_site():
                logger.info(f'<выбрана ссылка> {links}, -------- {site_pars}')
                if site_pars == ['synapsenet.ru']:
                    synapsenet = self.synapsenet_site(links)
                    if synapsenet != 1:
                        logger.info(f'<закончили> -- synapsenet')
                        return synapsenet
                # elif site_pars == ['list-org.com']:
                # list_org = self.list_org_site(links)
                #     if list_org != 1:
                #         logger.info(f'<закончили> -- list-org')
                #         return list_org
                #     else:
                #         continue
                elif site_pars == ['zachestnyibiznes.ru']:
                    zachestnyibiznes = self.zachestnyibiznes_site(links)
                    if zachestnyibiznes != 1:
                        logger.info(f'<закончили> -- zachestnyibiznes')
                        return zachestnyibiznes
                elif site_pars == ['upvacancy.ru']:
                    upvacancy = self.upvacancy_site(links)
                    if upvacancy != 1:
                        logger.info(f'<закончили> -- upvacancy')
                        return upvacancy
                elif site_pars == ['checko.ru']:
                    checko = self.checko_site(links)
                    if checko != 1:
                        logger.info(f'<закончили> -- checko_site')
                        return checko
                elif site_pars == ['comfex.ru']:
                    comfex = self.comfex_site(links)
                    if comfex != 1:
                        logger.info(f'<закончили> -- comfex')
                        return comfex
                elif site_pars == ['complan.pro']:
                    complan = self.complan_site(links)
                    if complan != 1:
                        logger.info(f'<закончили> -- complan')
                        return complan
                elif site_pars == ['kontragent.pro']:
                    kontragent = self.kontragent_site(links)
                    if kontragent != 1:
                        logger.info(f'<закончили> -- kontragent')
                        return kontragent
                # elif site_pars == ['rusprofile.ru']:
                # rusprofile = self.rusprofile_site(links)
                #     if rusprofile != 1:
                #         logger.info(f'<закончили> -- rusprofile')
                #         return rusprofile
                elif site_pars == ['vypiska-nalog.com']:
                    vypiska = self.vypiska_site(links)
                    if vypiska != 1:
                        logger.info(f'<закончили> -- vypiska')
                        return vypiska
                elif site_pars == ['1cont.ru']:
                    _1_cont = self._1_cont_site(links)
                    if _1_cont != 1:
                        logger.info(f'<закончили> -- _1_cont')
                        return _1_cont
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def rusprofile_site(self, *args):
        logger.info(f"<начало работы> rusprofile_site -- набор ссылок-- {args}")
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            self.soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = self.soup_4.find(itemprop='legalName').get_text(strip=True)
            self.boss_company = self.soup_4.find(class_='link-arrow gtm_main_fl').get_text(strip=True)
            self.adress_company = self.soup_4.find(itemprop='address').get_text(strip=True)
            self.inn_company = self.soup_4.find('span', id='clip_inn').get_text(strip=True)
            self.kpp_company = self.soup_4.find('span', id='clip_kpp').get_text(strip=True)
            self.ogrn_company = self.soup_4.find('span', id='clip_ogrn').get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)

            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')
            return 1

    def list_org_site(self, *args):
        logger.info(f"<начало работы> list_org_site -- набор ссылок-- {args}")
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            self.soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = self.soup_4.find_all('a', class_='upper')[0].get_text(strip=True)
            self.boss_company = self.soup_4.find_all(class_='upper')[1].get_text(strip=True)
            self.adress_company = self.soup_4.find_all(class_='upper')[2].get_text(strip=True)
            self.inn_company = self.soup_4.find_all(class_='c2m')[2].find_all('p')[0].get_text(strip=True)
            self.kpp_company = self.soup_4.find_all(class_='c2m')[2].find_all('p')[1].get_text(strip=True)
            self.ogrn_company = self.soup_4.find_all(class_='c2m')[2].find_all('p')[3].get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)

            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def kontragent_site(self, args):
        logger.info(f'<начало работы> kontragent_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            self.soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            check_fild = self.soup_4.find(id='overview').find_all('th')[0].get_text(strip=True)
            if not re.findall(r'Полное наименование', str(check_fild), flags=re.I):
                self.name_company = self.soup_4.find(id='overview').find_all('td')[1].get_text(strip=True)
                self.boss_company = self.soup_4.find(id='overview').find_all('td')[9].get_text(strip=True)
                self.adress_company = self.soup_4.find(id='overview').find_all('td')[8].get_text(strip=True)
            else:
                self.name_company = self.soup_4.find(id='overview').find_all('td')[0].get_text(strip=True)
                self.boss_company = self.soup_4.find(id='overview').find_all('td')[8].get_text(strip=True)
                self.adress_company = self.soup_4.find(id='overview').find_all('td')[7].get_text(strip=True)
            self.inn_company = self.soup_4.find(id='details').find_all('td')[1].get_text(strip=True)
            self.kpp_company = self.soup_4.find(id='details').find_all('td')[2].get_text(strip=True)
            self.ogrn_company = self.soup_4.find(id='details').find_all('td')[0].get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def checko_site(self, args):
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        logger.info(f'<начало работы> checko_site -- набор ссылок-- {self.url}-----------------------------')
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            name_company_pre = soup_4.find('p', class_='counterparty-full-name').get_text(strip=True)
            self.name_company_2 = str(name_company_pre).split(',')[0]
            self.name_company = f'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ {self.name_company_2}'
            self.boss_company = soup_4.find_all('a', class_='default-link')[5].get_text(strip=True)
            self.adress_company = soup_4.find(id='shortcut:contacts').find('td').get_text(strip=True)
            self.inn_company = soup_4.find(id='copy-details-inn').get_text(strip=True)
            self.kpp_company = soup_4.find(id='copy-details-kpp').get_text(strip=True)
            self.ogrn_company = soup_4.find(id='copy-details-ogrn').get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def upvacancy_site(self, *args):
        logger.info(f'<начало работы> upvacancy_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                time.sleep(random.randint(1, 3))
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            time.sleep(random.randint(1, 3))
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find('div', class_='uk-text-muted -mt-4 mb-4').get_text(strip=True)
            self.boss_company = soup_4.find(id='leaders').find_all('div')[1].find('div').get_text(strip=True)
            self.adress_company = soup_4.find(id='contacts').find('td').get_text(strip=True)
            self.inn_company = soup_4.find(id='details').find_all('td')[1].get_text(strip=True)
            self.kpp_company = soup_4.find(id='details').find_all('td')[2].get_text(strip=True)
            self.ogrn_company = soup_4.find(id='details').find_all('td')[0].get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def zachestnyibiznes_site(self, *args):
        logger.info(f'<начало работы> zachestnyibiznes_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:

            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find(class_='f-s-16 f-w-400 m-b-15').get_text(strip=True)[32: -42]
            try:
                self.boss_company = soup_4.find_all(class_='m-t-15')[5].find_all(target='_blank')[0].get_text(
                    strip=True)
            except:
                try:
                    self.boss_company = soup_4.find_all(class_='m-t-15')[7].find_all(target='_blank')[0].get_text(
                        strip=True)
                except:
                    self.boss_company = soup_4.find_all(class_='m-t-15')[8].find_all(target='_blank')[0].get_text(
                        strip=True)
                    try:
                        self.boss_company = soup_4.find_all(class_='m-t-15')[6].find_all(target='_blank')[0].get_text(
                            strip=True)
                    except Exception as exc:
                        logger.info(exc)

            self.adress_company = soup_4.find(itemprop='address').get_text(strip=True)[32:]
            self.inn_company = soup_4.find('span', id='inn').get_text(strip=True)
            self.kpp_company = soup_4.find('span', id='kpp').get_text(strip=True)
            self.ogrn_company = soup_4.find('span', id='ogrn').get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def vypiska_site(self, *args):
        logger.info(f'<начало работы> vypiska_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find('table', class_='table reee_table').find_all('td')[14].get_text(strip=True)
            self.boss_company = soup_4.find('table', class_='table reee_table').find_all('td')[12].get_text(strip=True)
            self.adress_company = soup_4.find('table', class_='table reee_table').find_all('td')[2].get_text(strip=True)
            self.inn_company = soup_4.find('table', class_='table reee_table').find_all('td')[6].get_text(strip=True)
            self.kpp_company = soup_4.find('table', class_='table reee_table').find_all('td')[7].get_text(strip=True)
            self.ogrn_company = soup_4.find('table', class_='table reee_table').find_all('td')[8].get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def _1_cont_site(self, *args):
        logger.info(f'<начало работы> _1_cont_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            self.url = self.pre_dict['1cont']
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find(itemprop='legalName').get_text(strip=True)
            self.boss_company = soup_4.find_all('p', class_='p contragent-card__main-info-ceo-name')[0].get_text(
                strip=True)
            self.adress_company = soup_4.find(itemprop='address').get_text(strip=True)
            self.inn_company = soup_4.find_all(class_='contragent-card__main-info-column-kv-row-value')[3].get_text(
                strip=True)
            self.kpp_company = soup_4.find_all(class_='contragent-card__main-info-column-kv-row-value')[4].get_text(
                strip=True)
            self.ogrn_company = soup_4.find_all(class_='contragent-card__main-info-column-kv-row-value')[2].get_text(
                strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def synapsenet_site(self, *args):
        logger.info(f'<начало работы> synapsenet_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find(id='org-full-header').find('h2').get_text(strip=True)
            self.boss_company = soup_4.find(class_='ofcd-supervisor').find_all('div')[1].get_text(strip=True)
            self.adress_company = soup_4.find_all(class_='ofc-block')[0].find('div').get_text(strip=True)
            self.inn_company = soup_4.find_all(class_='ofcd-requisites')[1].find_all('li')[1].get_text(strip=True)
            self.kpp_company = soup_4.find_all(class_='ofcd-requisites')[1].find_all('li')[2].get_text(strip=True)
            self.ogrn_company = soup_4.find_all(class_='ofcd-requisites')[1].find_all('li')[0].get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def comfex_site(self, *args):
        logger.info(f'<начало работы> comfex_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\"]", '', str(pre_dict_pre), flags=re.I)
        try:
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find('h2', itemprop='legalName').get_text(strip=True)
            self.boss_company = soup_4.find('div', class_='ml-4 uk-width-expand').find('a').get_text(strip=True)
            self.adress_company = soup_4.find('div', itemprop='address').get_text(strip=True)
            self.inn_company = soup_4.find('strong', id='copy-inn').get_text(strip=True)
            self.kpp_company = soup_4.find('span', id='copy-kpp').get_text(strip=True)
            self.ogrn_company = soup_4.find('strong', id='copy-ogrn').get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def complan_site(self, *args):
        logger.info(f'<начало работы> complan_site -- набор ссылок-- {args}')
        pre_dict_pre = args
        self.url = re.sub(r"[\t\s{})\[\]'(\",]", '', str(pre_dict_pre), flags=re.I)

        try:
            self.url = self.pre_dict['comfex']
            if not self.url:
                logger.info(f'<нет ссылки> {self.url}')
                logger.warning(f'<нет ссылки> {self.url}')
            try:
                self.sourse_open = requests.get(url=self.url, headers=HEADERS)
                time.sleep(random.randint(1, 3))
                if self.sourse_open.status_code != 200:
                    logger.info(f'<сайт не отвечает> {self.sourse_open}')
                    logger.warning(f'<сайт не отвечает> {self.sourse_open}')
            except Exception as exc:
                logger.info(f'<ошибка> {exc}')
                logger.warning(f'<ошибка> {exc}')
                return 1
            soup_4 = BeautifulSoup(self.sourse_open.text, 'lxml')
            self.name_company = soup_4.find(itemprop='legalName').get_text(strip=True)
            self.boss_company = soup_4.find('a', itemprop='name').get_text(strip=True)
            self.adress_company = soup_4.find('div', itemprop='address').get_text(strip=True)
            self.inn_company = soup_4.find(id='copy-inn').get_text(strip=True)
            self.kpp_company = soup_4.find(id='copy-kpp').get_text(strip=True)
            self.ogrn_company = soup_4.find(id='copy-ogrn').get_text(strip=True)

            name_ooo_pre = re.findall(r'[\w+]', str(self.name_company), flags=re.I)
            name_company_pick = re.sub(r"[\W*]", '', str(name_ooo_pre), flags=re.I)

            winner_ooo_pre = re.findall(r'[\w+]', str(self.name_winner_pre), flags=re.I)
            winner_company_pick = re.sub(r"[\W*]", '', str(winner_ooo_pre), flags=re.I)
            logger.info('----до сравнения названия--------')
            if name_company_pick == winner_company_pick:
                logger.info(f'<-------------определено название компании> - {self.name_company},'
                            f' <победитель с сайта> - {self.name_winner_pre}-----------------')
                self.catch_data['inn_company_base'] = self.inn_company
                self.catch_data['name_company_base'] = self.name_company.upper()
                print(self.catch_data['name_company_base'])
                print(self.boss_company)
                print(self.adress_company)
                print(self.catch_data['inn_company_base'])
                print(self.kpp_company)
                print(self.ogrn_company)
                res_name = self.catch_data['name_company_base']
                return res_name
            else:
                return 1
        except Exception as exc:
            logger.info(f'<ошибка> {exc}')
            logger.warning(f'<ошибка> {exc}')

    def parse_index_name(self, *args):
        logger.info(f" начало <parse_index_name>")
        self.inn_index, self.name_winner_pre = args
        name_winner_pre_2 = str(self.name_winner_pre).split('ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ')[1]
        self.name_winner = re.sub(r"[\t)(']", '', str(name_winner_pre_2), flags=re.I)

        # parse_router = self.parse_router_site()
        # return parse_router
        return self.checking_google()

        # for item in self.router_site():
        #     print(item)
        #     pass


check_inn_ya = CheckInnYa()

# if __name__ == '__main__':
#     check_inn_ya.parse_index_name()
