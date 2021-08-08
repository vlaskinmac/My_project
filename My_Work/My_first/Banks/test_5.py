# -*- coding: utf-8 -*-
import datetime
import json
import re
from multiprocessing import Process, Pool
from threading import Thread
from multiprocessing import Queue
import clipboard as clipboard
import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import auth_data
import time
from PIL import Image
import requests
from bs4 import BeautifulSoup
import logging
# from datetime import datetime
from My_Work.My_first.Banks.decorators import time_track

tender_number = '0372100048821000241'
sum_contract = '500000001'
inn = '0263024026'
sum_bg = '3500000'  # на вход
end_date = '31.12.2021'  # на вход


# logging.basicConfig(level=logging.DEBUG,format='(%(funcName)-10s) %(message)s',)


class AlfaBank(Thread):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)

    authentification_first_element_by_id = 'clientRegistration'
    authentification_loginelement_by_id = 'login'
    authentification_password_element_by_id = 'pass'

    way_to_calc_first_step_element_by_xpath = '//*[@id="main-menu"]/ul/li[7]/a'
    way_to_calc_second_step_element_by_xpath = '//*[@id="s2id_autogen4"]/a'

    filling_fields_inn_element_by_xpath = '//*[@id="select2-drop"]/div/input'

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = '//*[@id="panel-calc-bg"]/form/div/div[1]/div/div[2]/div[6]/div[2]/' \
                                             'div[2]/input'

    filling_dates_calendar_start_element_by_xpath = '//*[@id="panel-calc-bg"]/form/div/div[1]/div/div[2]/div[6]/div[3]/div[2]/' \
                                                    'div[2]/input'
    filling_dates_calendar_end_element_by_xpath = '//*[@id="panel-calc-bg"]/form/div/div[1]/div/div[2]/' \
                                                  'div[6]/div[3]/div[2]/div[4]/input'
    filling_dates_calendar_move_element_by_xpath = None
    # filling_dates_absolute_value_element_by_xpath = # end__date

    price_bg_getting_element_by_xpath = '//*[@id="content-wrapper"]/div/div[2]/div[2]/div[2]/div/div[1]/div[1]'

    def __init__(self, bank_url, username=None, password=None):
        super().__init__()

        self.bank_url = bank_url
        self.username = username
        self.password = password

    def authentification(self):
        self.browser.get(self.bank_url)
        self.browser.find_element_by_id(self.authentification_first_element_by_id).click()
        time.sleep(1)
        username_pre = self.browser.find_element_by_id(self.authentification_loginelement_by_id)
        username_pre.send_keys(self.username)
        time.sleep(1)
        password_pre = self.browser.find_element_by_id(self.authentification_password_element_by_id)
        password_pre.send_keys(self.password)
        time.sleep(1)
        password_pre.send_keys(Keys.ENTER)
        time.sleep(1)

    def main(self):
        # p = Process(target=self.authentification)
        # p.start()
        # p.join()
        self.authentification()


class LocoBank(Thread):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)

    authentification_first_element_by_id = None
    authentification_loginelement_by_id = 'username-email'
    authentification_password_element_by_id = 'password'

    way_to_calc_first_step_element_by_xpath = '//*[@id="GridTable"]/div/div[2]/table/tbody/tr[1]/td[4]/a'
    way_to_calc_second_step_element_by_xpath = None

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = '//*[@id="Step1_1"]/div[1]/div[2]/div[2]/div[1]/div[6]'

    filling_dates_calendar_start_element_by_xpath = '//*[@id="LimitFrom"]'
    filling_dates_calendar_end_element_by_xpath = '//*[@id="LimitTo"]'

    filling_dates_calendar_move_element_by_xpath = None
    # filling_dates_absolute_value_element_by_xpath = # end__date

    price_bg_getting_element_by_xpath = '//*[@id="Comission-sale"]'

    random_place = '//*[@id="Balances"]/div[1]/h1'
    copy_place = '//*[@id="ContractPurpose"]'

    def __init__(self, bank_url, username=None, password=None):
        super().__init__()

        self.bank_url = bank_url
        self.username = username
        self.password = password

    def authentification(self):
        self.browser.get(self.bank_url)
        username_pre = self.browser.find_element_by_id(self.authentification_loginelement_by_id)
        time.sleep(1)
        username_pre.send_keys(self.username)
        time.sleep(2)
        password_pre = self.browser.find_element_by_id(self.authentification_password_element_by_id)
        password_pre.send_keys(self.password)
        time.sleep(2)
        password_pre.send_keys(Keys.ENTER)
        time.sleep(1)

    def main(self):
        # p = Process(target=self.authentification)
        # p.start()
        # p.join()
        self.authentification()


class RealistBank(Thread):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)

    authentification_first_element_by_id = None
    authentification_loginelement_by_id = 'username'
    authentification_password_element_by_id = 'password'

    way_to_calc_first_step_element_by_xpath = '/html/body/div[5]/div/div[2]/div[1]/div/div[2]/div/a[2]'
    way_to_calc_second_step_element_by_xpath = '//*[@id="product_id"]'
    way_to_calc_three_step_element_by_xpath = '//*[@id="type_bank_guarantee"]'
    # way_to_calc_four_step_element_by_xpath = '//*[@id="close_popover"]'

    filling_fields_inn_element_by_xpath = '//*[@id="new_ticket_stage_0_form"]/div/div/div[2]/div/div[3]/div/input'

    filling_fields_tender_number_element_by_xpath = '//*[@id="auction_number"]'

    filling_fields_sum_bg_element_by_xpath = '//*[@id="bg_sum"]'
    filling_fields_sum_bg_way_element_by_xpath = '//*[@id="bg_reason"]'

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = '//*[@id="bg_end_at"]'
    filling_dates_calendar_move_element_by_xpath = '//*[@id="enter_data"]'

    ''' filling_dates_absolute_value_element_by_xpath = # end__date--------------------------------------------'''

    price_bg_getting_element_by_xpath = '/html/body/div[5]/div/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/span/span'
    price_bg_getting_move_element_by_xpath = '/html/body/div[5]/div/div[2]/div[2]/div/div/div/a[3]'

    random_place = None
    copy_place = None

    def __init__(self, bank_url, username=None, password=None):
        super().__init__()

        self.bank_url = bank_url
        self.username = username
        self.password = password

    def authentification(self):
        self.browser.get(self.bank_url)
        username_pre = self.browser.find_element_by_id(self.authentification_loginelement_by_id)
        time.sleep(1)
        username_pre.send_keys(self.username)
        time.sleep(2)
        password_pre = self.browser.find_element_by_id(self.authentification_password_element_by_id)
        password_pre.send_keys(self.password)
        time.sleep(2)
        password_pre.send_keys(Keys.ENTER)
        time.sleep(1)

    def main(self):
        # p = Process(target=self.authentification)
        # p.start()
        # p.join()
        self.authentification()


class BcsBank(Thread):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    authentification_first_element_by_id = None
    authentification_loginelement_by_id = 'signin_user'
    authentification_password_element_by_id = 'signin_pass'

    way_to_calc_first_step_element_by_xpath = '//*[@id="signin"]/a/div'
    way_to_calc_second_step_element_by_xpath = '//*[@id="bgtc"]/div[1]/fieldset[1]/div/table/tbody/tr[1]/td[2]/label'

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = '//*[@id="amount"]'

    filling_dates_start_element_by_xpath = '//*[@id="bgtc"]/div[1]/fieldset[4]/table/tbody/tr/td[1]/div/input'
    filling_dates_end_element_by_xpath = '//*[@id="bgtc"]/div[1]/fieldset[4]/table/tbody/tr/td[2]/div/input'
    filling_dates_calendar_move_element_by_xpath = '//*[@id="calculate"]'

    # filling_dates_absolute_value_element_by_xpath = # end__date

    price_bg_getting_element_by_xpath = '//*[@id="commissionAmount"]'

    random_place = None
    copy_place = None

    def __init__(self, bank_url, username=None, password=None):
        super().__init__()

        self.bank_url = bank_url
        self.username = username
        self.password = password

    def authentification(self):
        self.browser.get(self.bank_url)
        username_pre = self.browser.find_element_by_id(self.authentification_loginelement_by_id)
        time.sleep(1)
        username_pre.send_keys(self.username)
        time.sleep(2)
        password_pre = self.browser.find_element_by_id(self.authentification_password_element_by_id)
        password_pre.send_keys(self.password)
        time.sleep(2)
        password_pre.send_keys(Keys.ENTER)
        time.sleep(1)

    def main(self):
        # p = Process(target=self.authentification)
        # p.start()
        # p.join()
        self.authentification()


alfabank = AlfaBank(bank_url=auth_data.alfabank['url'],
                    username=auth_data.alfabank['username'],
                    password=auth_data.alfabank['password'])

locobank = LocoBank(bank_url=auth_data.locobank['url'],
                    username=auth_data.locobank['username'],
                    password=auth_data.locobank['password'])

realistbank = RealistBank(bank_url=auth_data.realistbank['url'],
                          username=auth_data.realistbank['username'],
                          password=auth_data.realistbank['password'])

bcsbank = BcsBank(bank_url=auth_data.bcsbank['url'],
                  username=auth_data.bcsbank['username'],
                  password=auth_data.bcsbank['password'])

# def mmm():

# alfabank.main()
# locobank.main()
# realistbank.main()
# bcsbank.main()

# list_obgects = [alfabank.main(), locobank.main(), realistbank.main(), bcsbank.main()]
# object_thread = []
# for i in list_obgects:
#     t = Thread(target=i)
#     object_thread.append(t)
#     for i in object_thread:
#         i.start()
#     for i in object_thread:
#         i.join()

# a = Thread(target=alfabank.main)
# b = Thread(target=locobank.main)
# c = Thread(target=realistbank.main)
# d = Thread(target=bcsbank.main)
# a.start()
# b.start()
# c.start()
# d.start()
# time.sleep(6)
#
# a.terminate()
# a.join(1)
# b.terminate()
# b.join(1)
# d.terminate()
# d.join(1)
# c.terminate()
# c.join(1)
#
# a = Process(target=alfabank.main)
# b = Process(target=locobank.main)
# c = Process(target=realistbank.main)
# d = Process(target=bcsbank.main)
#
# a.start()
# b.start()
# c.start()
# d.start()
# time.sleep(6)
#
# a.terminate()
# a.join(1)
# b.terminate()
# b.join(1)
# d.terminate()
# d.join(1)
# c.terminate()
# c.join(1)
if __name__ == '__main__':
    list_obgects = [alfabank.main, locobank.main, realistbank.main, bcsbank.main]
    object_thread = []
    for i in list_obgects:
        t = Thread(target=i)
        object_thread.append(t)

    for i in object_thread:
        i.start()

    # a = Thread(target=alfabank.main)
    # b = Thread(target=locobank.main)
    # c = Thread(target=realistbank.main)
    # d = Thread(target=bcsbank.main)
    # a.start()
    # b.start()
    # c.start()
    # d.start()

    # mmm()
    # list_obgects = [alfabank.main(), locobank.main(), realistbank.main(), bcsbank.main()]
    # object_thread = []
    # for i in list_obgects:
    # t = Process(target=mmm)
    # t.start()
    # t.join()

    # for i in object_thread:
    #     i.start()
    # for i in object_thread:
    #     i.join()
    #
    # for i in range(4):
    #     t = Process(target=mmm, args=(i,))
    #     t.start()
    #     t.join()

    # def main(self):
    #     p = Process(target=self.authentification)
    #     p.start()
    #     p.join()
    # self.authentification()

    # list_obgects = [alfabank.main(), locobank.main(), realistbank.main(), bcsbank.main(), sovcombank.main(),
    #                 derzhavabank.main(), absolutbank.main(), otcritiebank.main(), mtsbank.main(), goofinbanks.main(),
    #                 uralsibbank.main()]
    # alfabank.main()
    # locobank.main()
    # realistbank.main()
    # bcsbank.main()
    # sovcombank.main()
    # derzhavabank.main()
    # absolutbank.main()
    # otcritiebank.main()
    # mtsbank.main()
    # goofinbanks.main()
    # uralsibbank.main()

    # list_obgects = [alfabank.main(), locobank.main(), realistbank.main(), bcsbank.main()]
    # object_thread = []
    # for i in list_obgects:
    #     t = Process(target=mmm(), args=(i,))
    #     object_thread.append(t)
    # # for r in object_thread:
    #     t.start()
    # for r in object_thread:
    #     r.join()

    # a = Thread(target=alfabank.main())
    #
    # b = Thread(target=locobank.main())

    # a = Process(target=alfabank.main())
    # #
    # b = Process(target=locobank.main())
    #
    # fishers = [a, b]
    # #
    # # c = Process(target=absolutbank.main())
    # p= Pool(processes=3)
    # p.map(mmm, range(3))
    # for fisher in fishers:
    #     fisher.start()
    # for fisher in fishers:
    #     fisher.join()

    # a.start()
    # b.start()
    # # c.start()
    # #
    # a.join()
    # b.join()
    # c.join()
