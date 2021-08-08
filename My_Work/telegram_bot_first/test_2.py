import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from My_Work.My_first.Banks.auth_data import username
import time
import random

HOST = 'https://scb-private.fintender.ru'

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;'
              'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/89.0.4389.86 YaBrowser/21.3.0.663 Yowser/2.5 Safari/537.36'
}

link = 'https://scb-private.fintender.ru/bg/Agent/ClientRequest/Details?id=1947180'


def login(username):
    global soup
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--start-maximized")
    # options.add_argument("--start-minimizeWindow")
    browser = webdriver.Chrome('chromedriver', options=options)
    browser.get('https://scb-private.fintender.ru/home/User/Login')

    # options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    # options.add_argument("no-sandbox")
    # options.add_argument("--start-maximized")

    # -------------------------------------

    time.sleep(random.randrange(6))
    # chain = ActionChains(browser)
    xpath_1 = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/form[1]/div[1]/div[1]"
    username_input = browser.find_element_by_xpath(xpath_1)
    username_input.click()

    # xpath_2 = "//input[@id='input-63']"
    # username_input_2 = username_input.find_element_by_xpath(xpath_2)
    #
    # username_input_2.send_keys(Keys.BACKSPACE * 5)
    # username_input_2.send_keys(password)
    # xpath_3 ="//*[@class='result-value']"
    # chain = ActionChains(browser)

    # xpath_3 = "//*[@class='result-value']/text()"
    # xpath_3 ='//*[@id="app"]/div/div/div/div/div[2]/form/div/div[2]/div/div[2]'
    # username_input_3 = username_input_2.find_element_by_xpath(xpath_3)
    # username_input_3 = username_input_2.find_elements_by_xpath(xpath_3)
    # print(*username_input_3)
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(str(username_input_3))
    time.sleep(1)
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


login(username)

get_site_winner_protokol = requests.get(url=link, headers=HEADERS)

soup_winner_protokol = BeautifulSoup(get_site_winner_protokol.text, 'lxml')

print(soup_winner_protokol)

# pre = soup_winner_protokol.find('div', id='CustomerRequestData_ComissionSum')
# print(pre)
