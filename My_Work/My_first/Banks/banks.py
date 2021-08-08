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


class Banks:
    start_date_pre = datetime.date.today().strftime('%d.%m.%Y')
    start_date = start_date_pre.replace("'", " ").replace(" ", "")

    def __init__(self, bank_url, name, username=None, password=None, start_date=start_date):
        self.name = name
        self.bank_url = bank_url
        self.username = username
        self.password = password
        self.start_date = start_date


class AuthentificationBanks(Banks):

    # def authentification(self):
    #     self.browser.get(self.bank_url)
    #     username_pre = self.browser.find_element_by_id(self.authentification_loginelement_by_id)
    #     time.sleep(1)
    #     username_pre.send_keys(self.username)
    #     time.sleep(2)
    #     password_pre = self.browser.find_element_by_id(self.authentification_password_element_by_id)
    #     password_pre.send_keys(self.password)
    #     time.sleep(2)
    #     password_pre.send_keys(Keys.ENTER)
    #     time.sleep(1)

    def way_to_calc(self):
        self.browser.find_element_by_xpath(self.way_to_calc_first_step_element_by_xpath).click()
        time.sleep(3)
        self.browser.find_element_by_xpath(self.way_to_calc_second_step_element_by_xpath).click()

    def filling_inn(self):
        inn_pre = self.browser.find_element_by_xpath(self.filling_fields_inn_element_by_xpath)
        inn_pre.send_keys(inn)
        time.sleep(2)
        inn_pre.send_keys(Keys.ENTER)
        time.sleep(2)

    def filling_tender_number(self):
        inn_pre = self.browser.find_element_by_xpath(self.filling_fields_tender_number_element_by_xpath)
        inn_pre.send_keys(tender_number)
        time.sleep(2)
        inn_pre.send_keys(Keys.ENTER)
        time.sleep(2)

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.send_keys(Keys.BACKSPACE * 12)
        time.sleep(1)
        sum_bg_pre.send_keys(sum_bg)
        time.sleep(1)

    def filling_summ_contract(self):
        sum_contract_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_contract_element_by_xpath)
        sum_contract_pre.send_keys(Keys.BACKSPACE * 12)
        time.sleep(1)
        sum_contract_pre.send_keys(sum_contract)
        time.sleep(1)

    def filling_dates_calendar(self):
        start_date_pre = self.browser.find_element_by_xpath(self.filling_dates_calendar_start_element_by_xpath)
        # alfabank_start_date.clear()
        start_date_pre.click()
        time.sleep(0.5)
        start_date_pre.send_keys(self.start_date)
        time.sleep(1)
        start_date_pre.send_keys(Keys.ENTER)
        time.sleep(1)
        end__date_pre = self.browser.find_element_by_xpath(self.filling_dates_calendar_end_element_by_xpath)
        end__date_pre.click()
        # time.sleep(1)
        end__date_pre.send_keys(end_date)  # end__date =  переменную ждем
        time.sleep(0.5)
        end__date_pre.send_keys(Keys.ENTER)

        # self.browser.find_element_by_xpath(self.filling_dates_calendar_move_element_by_xpath)

    def price_bg_getting(self):
        price_bg_pre = self.browser.find_element_by_xpath(self.price_bg_getting_element_by_xpath)
        time.sleep(2)
        action = ActionChains(self.browser)
        action.click(on_element=price_bg_pre).click(on_element=price_bg_pre).click(on_element=price_bg_pre). \
            key_down(Keys.CONTROL).send_keys('c').perform()
        # # Получаем буфер обмена
        text_price_bg = clipboard.paste()
        get_note = re.findall('\d+', str(text_price_bg))
        note = re.sub(r"['|\"|\s|\]|\[|\b|(|)|\t|\r]", "", str(get_note))
        price_bg = note.replace(",", "", 1)
        print(price_bg, self.name)

        self.browser.close()
        self.browser.quit()


class AlfaBank(AuthentificationBanks):
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

    # @time_track
    def main(self):
        self.authentification()
        time.sleep(1)
        self.way_to_calc()
        time.sleep(1)
        self.filling_inn()
        time.sleep(1)
        self.filling_summ_bg()
        time.sleep(1)
        self.filling_dates_calendar()
        time.sleep(3)
        self.price_bg_getting()


class LocoBank(AuthentificationBanks):
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

    def way_to_calc(self):
        self.browser.find_element_by_xpath(self.way_to_calc_first_step_element_by_xpath).click()
        time.sleep(2)

    def filling_summ_bg(self):
        copy_place_sum_bg = self.browser.find_element_by_xpath(self.copy_place)
        copy_place_sum_bg.clear()
        time.sleep(1)
        copy_place_sum_bg.send_keys(sum_bg)
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        action = ActionChains(self.browser)
        action.click(on_element=copy_place_sum_bg).click(on_element=copy_place_sum_bg). \
            click(on_element=copy_place_sum_bg).key_down(Keys.CONTROL).send_keys('c').perform()
        time.sleep(1)
        action.click(on_element=sum_bg_pre).click(on_element=sum_bg_pre). \
            click(on_element=sum_bg_pre).key_down(Keys.CONTROL).send_keys('v').perform()
        time.sleep(1)
        self.browser.find_element_by_xpath(self.random_place).click()

    # @time_track
    def main(self):
        self.authentification()
        time.sleep(1)
        self.way_to_calc()
        time.sleep(1)
        self.filling_dates_calendar()
        time.sleep(1)
        self.filling_summ_bg()
        time.sleep(3)
        self.price_bg_getting()


class RealistBank(AuthentificationBanks):
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

    def way_to_calc(self):
        self.browser.find_element_by_xpath(self.way_to_calc_first_step_element_by_xpath).click()
        time.sleep(2)
        self.browser.find_element_by_xpath(self.way_to_calc_second_step_element_by_xpath).click()
        action = ActionChains(self.browser)
        time.sleep(0.5)
        action.key_down(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

        self.browser.find_element_by_xpath(self.way_to_calc_three_step_element_by_xpath).click()
        time.sleep(2)
        action.key_down(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

        # self.browser.find_element_by_xpath(self.way_to_calc_four_step_element_by_xpath).click()
        # time.sleep(1)

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.clear()
        time.sleep(1)
        sum_bg_pre.send_keys(sum_bg)
        time.sleep(2)
        self.browser.find_element_by_xpath(self.filling_fields_sum_bg_way_element_by_xpath).click()
        time.sleep(2)
        action = ActionChains(self.browser)
        action.key_down(Keys.ARROW_DOWN).key_down(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    def filling_dates_calendar(self):
        end_date_pre = self.browser.find_element_by_xpath(self.filling_dates_calendar_end_element_by_xpath)
        end_date_pre.click()
        # time.sleep(1)
        end_date_pre.send_keys(end_date)  # end__date =  переменную ждем
        time.sleep(2)
        self.browser.find_element_by_xpath(self.filling_dates_calendar_move_element_by_xpath).click()

    def price_bg_getting(self):
        # time.sleep(33)
        self.browser.implicitly_wait(65)
        price_bg_pre = self.browser.find_element_by_xpath(self.price_bg_getting_element_by_xpath)
        time.sleep(2)
        action = ActionChains(self.browser)
        action.click(on_element=price_bg_pre).click(on_element=price_bg_pre). \
            click(on_element=price_bg_pre).key_down(Keys.CONTROL).send_keys('c').perform()
        # # Получаем буфер обмена
        time.sleep(3)
        self.browser.find_element_by_xpath(self.price_bg_getting_move_element_by_xpath).click()
        text_price_bg = clipboard.paste()
        get_note = re.findall('\d+', str(text_price_bg))
        note = re.sub(r"['|\"|\s|\]|\[|\b|(|)|\t|\r]", "", str(get_note))
        price_bg = note.replace(",", "", 1)
        print(price_bg, self.name)

        self.browser.close()
        self.browser.quit()

    # @time_track
    def main(self):
        self.authentification()
        self.way_to_calc()
        self.filling_inn()
        self.filling_tender_number()
        self.filling_summ_bg()
        self.filling_dates_calendar()
        self.price_bg_getting()


class BcsBank(AuthentificationBanks):
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

    def filling_dates_calendar(self):
        start_date_pre = self.browser.find_element_by_xpath(self.filling_dates_start_element_by_xpath)
        # alfabank_start_date.clear()
        start_date_pre.click()
        time.sleep(0.5)
        start_date_pre.send_keys(self.start_date)
        time.sleep(1)
        start_date_pre.send_keys(Keys.ENTER)
        time.sleep(1)
        end__date_pre = self.browser.find_element_by_xpath(self.filling_dates_end_element_by_xpath)
        end__date_pre.click()
        # time.sleep(1)
        end__date_pre.send_keys(end_date)  # end__date =  переменную ждем
        time.sleep(1)
        self.browser.find_element_by_xpath(self.filling_dates_calendar_move_element_by_xpath).click()

    @time_track
    def main(self):
        self.authentification()
        self.browser.implicitly_wait(65)
        self.way_to_calc()
        self.filling_summ_bg()
        self.filling_dates_calendar()
        self.price_bg_getting()


class UralsibBank(AuthentificationBanks):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    authentification_first_element_by_id = None
    authentification_loginelement_by_id = 'id_username'
    authentification_password_element_by_id = 'id_password'

    way_to_calc_first_step_element_by_xpath = '/html/body/div[1]/aside/section/ul/li[5]/a/span[1]'
    way_to_calc_second_step_element_by_xpath = None
    way_to_calc_three_step_element_by_xpath = None
    # way_to_calc_four_step_element_by_xpath = '//*[@id="close_popover"]'

    filling_fields_inn_element_by_xpath = '//*[@id="calculator_form"]/div/div[2]/div[1]/span/span[1]/span'

    filling_fields_tender_number_element_by_xpath = '//*[@id="id_tender_number"]'

    filling_fields_sum_bg_element_by_xpath = '//*[@id="id_summBg"]'
    filling_fields_sum_bg_way_element_by_xpath = None

    filling_fields_sum_contract_element_by_xpath = '//*[@id="id_contract_sum"]'

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = None
    filling_dates_period_end_element_by_xpath = '//*[@id="id_duration"]'

    ''' filling_dates_absolute_value_element_by_xpath = # end__date--------------------------------------------'''

    price_bg_getting_element_by_xpath = '//*[@id="block_calculator_results"]/form/div/div[2]/div/div[1]/div/span'
    price_bg_getting_move_element_by_xpath = None

    random_place = None
    copy_place = None

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

    def way_to_calc(self):
        self.browser.find_element_by_xpath(self.way_to_calc_first_step_element_by_xpath).click()

    def filling_inn(self):
        self.browser.find_element_by_xpath(self.filling_fields_inn_element_by_xpath).click()
        action = ActionChains(self.browser)
        time.sleep(1)
        action.key_down(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()

    def filling_dates_period(self):
        start_date_pre = datetime.datetime.now()
        end_date_pre = datetime.datetime.strptime(end_date, '%d.%m.%Y')
        period_pre = end_date_pre - start_date_pre
        period = str(period_pre.days)

        period_value = self.browser.find_element_by_xpath(self.filling_dates_period_end_element_by_xpath)
        time.sleep(1)
        period_value.send_keys(Keys.BACKSPACE * 12)
        period_value.click()
        period_value.send_keys(period)
        time.sleep(2)
        period_value.send_keys(Keys.ENTER)

    # @time_track
    def main(self):
        self.authentification()
        self.way_to_calc()
        self.filling_inn()
        self.filling_tender_number()
        self.filling_summ_bg()
        self.filling_summ_contract()
        self.filling_dates_period()
        self.price_bg_getting()


class NotAuthentificationBanks(AuthentificationBanks):
    start_date_pre = datetime.datetime.now()
    end_date_pre = datetime.datetime.strptime(end_date, '%d.%m.%Y')
    period_pre = end_date_pre - start_date_pre
    period = str(period_pre.days)

    def authentification(self):
        self.browser.get(self.bank_url)

    def filling_dates_period(self):
        period_value = self.browser.find_element_by_xpath(self.filling_dates_period_end_element_by_xpath)
        time.sleep(1)
        period_value.send_keys(Keys.BACKSPACE * 12)
        period_value.click()
        period_value.send_keys(self.period)
        time.sleep(2)
        period_value.send_keys(Keys.ENTER)

        # self.browser.find_element_by_xpath(self.filling_dates_period_move_end_element_by_xpath).click()

    def filling_dates_period_with_start_date(self):
        start_date_pre = datetime.datetime.now()
        end_date_pre = datetime.datetime.strptime(end_date, '%d.%m.%Y')
        period_pre = end_date_pre - start_date_pre
        period = str(period_pre.days)

        start_date_pre = self.browser.find_element_by_xpath(
            self.filling_dates_period_with_start_date_start_element_by_xpath)
        start_date_pre.clear()
        start_date_pre.click()
        time.sleep(0.5)

        period_value = self.browser.find_element_by_xpath(self.filling_dates_period_with_start_end_element_by_xpath)
        time.sleep(1)
        period_value.send_keys(Keys.BACKSPACE * 12)
        period_value.click()
        period_value.send_keys(period)
        time.sleep(2)
        period_value.send_keys(Keys.ENTER)

        # self.browser.find_element_by_xpath(self.filling_dates_period_with_start_move_end_element_by_xpath)


class SovcomBank(NotAuthentificationBanks):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    way_to_calc_first_step_element_by_xpath = None
    way_to_calc_second_step_element_by_xpath = None

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = "//input[@id='input-57']"

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = None
    filling_dates_calendar_move_element_by_xpath = None

    filling_dates_period_start_element_by_xpath = None
    filling_dates_period_end_element_by_xpath = '//*[@id="input-63"]'
    filling_dates_period_move_end_element_by_xpath = None

    filling_dates_period_with_start_date_start_element_by_xpath = None
    filling_dates_period_with_start_end_element_by_xpath = None
    filling_dates_period_with_start_move_end_element_by_xpath = None

    price_bg_getting_element_by_xpath = '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/' \
                                        'form[1]/div[1]/div[2]/div[1]/div[2]'

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.send_keys(Keys.BACKSPACE * 12)
        sum_bg_pre.send_keys(sum_bg)

    # @time_track
    def main(self):
        self.authentification()
        self.filling_summ_bg()
        self.filling_dates_period()
        self.price_bg_getting()


class DerzhavaBank(NotAuthentificationBanks):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    way_to_calc_first_step_element_by_xpath = '//*[@id="index"]/div[8]/div[2]/ul/li[1]/ul/a[2]/li/img'
    way_to_calc_second_step_element_by_xpath = None

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = '//*[@id="sum"]'

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = None
    filling_dates_calendar_move_element_by_xpath = None

    filling_dates_period_start_element_by_xpath = None
    filling_dates_period_end_element_by_xpath = '//*[@id="days"]'
    filling_dates_period_move_end_element_by_xpath = '//*[@id="calculate"]'

    filling_dates_period_with_start_date_start_element_by_xpath = None
    filling_dates_period_with_start_end_element_by_xpath = None
    filling_dates_period_with_start_move_end_element_by_xpath = None

    price_bg_getting_element_by_xpath = '//*[@id="resultmess"]/span/img'

    def way_to_calc(self):
        self.browser.find_element_by_xpath(self.way_to_calc_first_step_element_by_xpath).click()

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.send_keys(Keys.BACKSPACE * 12)
        sum_bg_pre.send_keys(sum_bg)

    def filling_dates_period(self):
        start_date_pre = datetime.datetime.now()
        end_date_pre = datetime.datetime.strptime(end_date, '%d.%m.%Y')
        period_pre = end_date_pre - start_date_pre
        period = str(period_pre.days)

        period_value = self.browser.find_element_by_xpath(self.filling_dates_period_end_element_by_xpath)
        time.sleep(1)
        period_value.send_keys(Keys.BACKSPACE * 12)
        period_value.click()
        period_value.send_keys(period)
        time.sleep(2)
        period_value.send_keys(Keys.ENTER)

        self.browser.find_element_by_xpath(self.filling_dates_period_move_end_element_by_xpath).click()

    def price_bg_getting(self):
        self.browser.implicitly_wait(4)
        body = self.browser.find_element_by_class_name("summ").find_element_by_tag_name("img").get_attribute("src")
        self.browser.get(body)
        time.sleep(5)
        self.browser.save_screenshot("screenshot.png")
        filename_screen = 'screenshot.png'

        img = Image.open(filename_screen)
        box = (537, 618, 710, 645)
        area = img.crop(box)
        area.save('saved_image.png', 'PNG')
        filename = 'saved_image.png'

        time.sleep(5)
        img = cv2.imread(filename)
        text = pytesseract.image_to_string(img)
        get_note = re.findall('\d+', str(text))
        note_pre = re.sub(r"['|\"|,|\s|\]|\[|\b|(|)\.|\r]", "", str(get_note))
        res_note = note_pre[: -1]
        print(res_note, self.name)

        self.browser.close()
        self.browser.quit()

    # @time_track
    def main(self):
        self.authentification()
        self.way_to_calc()
        self.filling_summ_bg()
        self.filling_dates_period()
        time.sleep(3)
        self.price_bg_getting()


class AbsolutBank(NotAuthentificationBanks):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    way_to_calc_first_step_element_by_xpath = None
    way_to_calc_second_step_element_by_xpath = None

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = "//*[@id='formDeposit_RUB']/div[1]/div[1]/ul/li[1]/div/div[2]/input[2]"

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = None
    filling_dates_calendar_move_element_by_xpath = None

    filling_dates_period_start_element_by_xpath = None
    filling_dates_period_end_element_by_xpath = '//*[@id="formDeposit_RUB"]/div[1]/div[1]/ul/li[2]/div/div[2]/input[2]'
    filling_dates_period_move_end_element_by_xpath = None

    filling_dates_period_with_start_date_start_element_by_xpath = None
    filling_dates_period_with_start_end_element_by_xpath = None
    filling_dates_period_with_start_move_end_element_by_xpath = None

    price_bg_getting_element_by_xpath = '//*[@id="mothly_paid"]'

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.send_keys(Keys.BACKSPACE * 12)
        sum_bg_pre.send_keys(sum_bg)

    # @time_track
    def main(self):
        self.authentification()
        self.filling_summ_bg()
        self.filling_dates_period()
        self.price_bg_getting()


class OtcritieBank(NotAuthentificationBanks):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    way_to_calc_first_step_element_by_xpath = None
    way_to_calc_second_step_element_by_xpath = None

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = '//*[@id="id_summ"]'

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = None
    filling_dates_calendar_move_element_by_xpath = None

    filling_dates_period_start_element_by_xpath = None
    filling_dates_period_end_element_by_xpath = '//*[@id="id_duration"]'
    filling_dates_period_move_end_element_by_xpath = None

    filling_dates_period_with_start_date_start_element_by_xpath = None
    filling_dates_period_with_start_end_element_by_xpath = None
    filling_dates_period_with_start_move_end_element_by_xpath = None

    price_bg_getting_element_by_xpath = '/html/body/div[1]/div[3]/div/div[2]/div/div/form/div[4]/div/div[1]'

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.send_keys(Keys.BACKSPACE * 12)
        sum_bg_pre.send_keys(sum_bg)

    # @time_track
    def main(self):
        self.authentification()
        self.filling_summ_bg()
        self.filling_dates_period()
        self.price_bg_getting()


class MtsBank(NotAuthentificationBanks):
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome('chromedriver', options=options)
    way_to_calc_first_step_element_by_xpath = None
    way_to_calc_second_step_element_by_xpath = None

    filling_fields_inn_element_by_xpath = None

    filling_fields_tender_number_element_by_xpath = None

    filling_fields_sum_bg_element_by_xpath = '//*[@id="id_summ"]'

    filling_dates_calendar_start_element_by_xpath = None
    filling_dates_calendar_end_element_by_xpath = None
    filling_dates_calendar_move_element_by_xpath = None

    filling_dates_period_start_element_by_xpath = None
    filling_dates_period_end_element_by_xpath = '//*[@id="id_duration"]'
    filling_dates_period_move_end_element_by_xpath = None

    filling_dates_period_with_start_date_start_element_by_xpath = None
    filling_dates_period_with_start_end_element_by_xpath = None
    filling_dates_period_with_start_move_end_element_by_xpath = None

    price_bg_getting_element_by_xpath = '/html/body/div[2]/div[3]/div/div/div/div[2]/div/div[1]'

    def filling_summ_bg(self):
        sum_bg_pre = self.browser.find_element_by_xpath(self.filling_fields_sum_bg_element_by_xpath)
        sum_bg_pre.send_keys(Keys.BACKSPACE * 12)
        sum_bg_pre.send_keys(sum_bg)

    # @time_track
    def main(self):
        self.authentification()
        self.filling_summ_bg()
        self.filling_dates_period()
        self.price_bg_getting()


# --------------------------
#
class GoofinBanks(NotAuthentificationBanks):
    """
    Почта Банк - 99,
    Сбербанк - 94,
    Банк-РГС - 92,
    Промсвязьбанк - 84

    """

    HEADERS = {
        'Accept': '*/*', 'Sec-Fetch-Site': 'same-origin', 'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
    }
    filename = '../../telegram_bot_first/ttt.txt'

    def getting_data(self):
        url_goodfin = f"https://goodfin.ru/calculator_get_results.php?fz=54&" \
                      f"product=62&cost={sum_bg}&days={self.period}&callback=calcSearchCallback"
        base_html_code = requests.get(url_goodfin, headers=self.HEADERS)
        soup = BeautifulSoup(base_html_code.text, 'lxml')
        # print(soup)
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(soup.text)
        with open(self.filename, 'r', encoding='utf-8') as file:
            self.text_var = file.read()

    def parse_data(self):
        parse_data_pre = self.text_var[self.text_var.find('({"82"') + 1:]
        parse_data = parse_data_pre[:-1]
        self.data_json = json.loads(parse_data)

    def print_data(self):
        print(self.data_json['99']['bank']['name'], self.data_json['99']['cost'], sep=': ')
        print(self.data_json['94']['bank']['name'], self.data_json['94']['cost'], sep=': ')
        print(self.data_json['92']['bank']['name'], self.data_json['92']['cost'], sep=': ')
        print(self.data_json['84']['bank']['name'], self.data_json['84']['cost'], sep=': ')

    def write_json(self):
        with open("../../telegram_bot_first/xxx.json", 'w', encoding='utf-8') as file:
            json.dump(self.data_json, file, indent=4, ensure_ascii=False)

        with open('../../telegram_bot_first/xxx.json', encoding='utf-8') as file:
            self.dict_file = json.load(file)

    # @time_track
    def main(self):
        self.getting_data()
        self.parse_data()
        self.print_data()


alfabank = AlfaBank(bank_url=auth_data.alfabank['url'], name='AlfaBank',
                    username=auth_data.alfabank['username'],
                    password=auth_data.alfabank['password'])

locobank = LocoBank(bank_url=auth_data.locobank['url'], name='LocoBank',
                    username=auth_data.locobank['username'],
                    password=auth_data.locobank['password'])

realistbank = RealistBank(bank_url=auth_data.realistbank['url'], name='RealistBank',
                          username=auth_data.realistbank['username'],
                          password=auth_data.realistbank['password'])

bcsbank = BcsBank(bank_url=auth_data.bcsbank['url'], name='BcsBank',
                  username=auth_data.bcsbank['username'],
                  password=auth_data.bcsbank['password'])

uralsibbank = UralsibBank(bank_url=auth_data.uralsibbank['url'], name='UralsibBank',
                          username=auth_data.uralsibbank['username'],
                          password=auth_data.uralsibbank['password'])

sovcombank = SovcomBank(bank_url=auth_data.sovcombank['url'], name='SovcomBank')

derzhavabank = DerzhavaBank(bank_url=auth_data.derzhavabank['url'], name='DerzhavaBank / AkBarsBank')

absolutbank = AbsolutBank(bank_url=auth_data.absolutbank['url'], name='AbsolutBank')

otcritiebank = OtcritieBank(bank_url=auth_data.otcritiebank['url'], name='OtcritieBank')

goofinbanks = GoofinBanks(bank_url=auth_data.goofinbanks['url'], name=None)

mtsbank = MtsBank(bank_url=auth_data.mtsbank['url'], name='MtsBank')

list_obgects = [alfabank.main, locobank.main, realistbank.main, bcsbank.main, sovcombank.main,
                derzhavabank.main, absolutbank.main, otcritiebank.main, mtsbank.main, goofinbanks.main,
                uralsibbank.main]


def main():
    object_thread = []
    for i in list_obgects:
        t = Thread(target=i)
        object_thread.append(t)
    for i in object_thread:
        i.start()


if __name__ == '__main__':
    main()
