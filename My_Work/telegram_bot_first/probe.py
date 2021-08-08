# -*- coding: utf-8 -*-
import re

import clipboard as clipboard
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from My_Work.My_first.Banks.auth_data import summ, days
import time
import random


#  переход по вкладкам driver.switch_to.window(tabs[0])

def login(summ):
    global soup
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--start-maximized")
    # options.add_argument("--start-minimizeWindow")
    browser = webdriver.Chrome('chromedriver', options=options)
    browser.get('https://fintender.ru/bankovskaya-garantiya-na-ispolnenie-kontrakta-dogovora')
    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("no-sandbox")
    # options.add_argument("--start-maximized")

    # -------------------------------------

    time.sleep(random.randrange(6))

    xpath_1 = "//input[@id='input-57']"
    username_input = browser.find_element_by_xpath(xpath_1)
    username_input.send_keys(Keys.BACKSPACE * 12)
    username_input.send_keys(summ)

    xpath_2 = "//input[@id='input-63']"
    username_input_2 = username_input.find_element_by_xpath(xpath_2)

    username_input_2.send_keys(Keys.BACKSPACE * 5)
    username_input_2.send_keys(days)
    time.sleep(1)
    # xpath_3 ="/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[2]/div[1]/div[1]"
    xpath_4 = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[2]/div[1]/div[2]"
    username_input_3 = username_input.find_element_by_xpath(xpath_4)
    chain = ActionChains(browser)
    chain.click(on_element=username_input_3).click(on_element=username_input_3).click(on_element=username_input_3). \
        key_down(Keys.CONTROL).send_keys('c').perform()
    # Получаем буфер обмена
    text = clipboard.paste()
    get_note = re.findall('\d+', str(text))
    note = re.sub(r"['|\"|,|\s|\]|\[|\b|(|)\.|\r]", "", str(get_note))
    print(note)

    # chain.drag_and_drop(xpath_3, xpath_4).perform()
    # chain.click_and_hold(on_element=xpath_3).click(Keys.).perform()
    # print(username_input_3)
    # xpath_3 = "//*[@class='result-value']/text()"
    # xpath_3 ='//*[@id="app"]/div/div/div/div/div[2]/form/div/div[2]/div/div[2]'
    # username_input_3 = username_input_2.find_element_by_xpath(xpath_3)
    # username_input_3 = username_input_2.find_elements_by_xpath(xpath_3)
    # print(*username_input_3)

    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(str(username_input_3))
    # time.sleep(1)
    # actions = ActionChains(browser)
    # time.sleep(0.6)
    # actions.click_and_hold('win').click(Keys.ARROW_RIGHT).perform()
    # actions.key_down(Keys.PAGE_DOWN, username_input_3).perform()

    # with mss.mss() as sct:
    #     # Get information of monitor 3 - позиционирует по своим правилам не по винде
    #     monitor_number = 1
    #     mon = sct.monitors[monitor_number]
    #
    #     # The screen part to capture
    #     time.sleep(5)
    #     monitor = {
    #         "top": mon["top"] + 890,  # 100px from the top
    #         "left": mon["left"] + 90,  # 100px from the left
    #         "width": 290,
    #         "height": 85,
    #         "mon": monitor_number,
    #     }
    #     filename = "image.png".format(**monitor)
    #
    #     # Grab the data
    #     sct_img = sct.grab(monitor)
    #
    #     # Save to the picture file
    #     mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
    #     # print(filename)
    # time.sleep(3)
    # img = cv2.imread(filename)
    # text = pytesseract.image_to_string(img)
    # get_note = re.findall('\d+', str(text))
    # note = re.sub(r"['|\"|,|\s|\]|\[|\b|(|)\.|\r]", "", str(get_note))
    # print(note)
    # print(get_note)
    time.sleep(20000)

    browser.close()
    browser.quit()


login(summ)
