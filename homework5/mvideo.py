from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from db import save_goods_to_db

chrome_options = Options()
import time
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

time.sleep(15)

assert "М.Видео" in driver.title

actions = ActionChains(driver)

def load_page_by_scroll():
    footer_bottom = driver.find_elements_by_class_name('footer-bottom')[0]
    actions.move_to_element(footer_bottom)
    actions.perform()

load_page_by_scroll()

galleries = driver.find_elements_by_xpath("//div[@class='gallery-layout']")
button = galleries[1].find_elements_by_xpath(".//a[@class='next-btn sel-hits-button-next']")[0]
actions.move_to_element(button)\
    .click(button).pause(0.5)\
    .click(button).pause(0.5)\
    .click(button).pause(0.5)\
    .click(button).pause(1).perform()

nodes = galleries[1].find_elements_by_xpath(".//div[@class='c-product-tile sel-product-tile-main ']")

result_goods = []
for node in nodes:
    price_nodes = node.find_elements_by_xpath(".//div[@class='c-pdp-price__current']")
    price = None
    if len(price_nodes) != 0:
        price = re.sub(r'[^\d]+', '', price_nodes[0].text)

    title_nodes = node.find_elements_by_xpath('.//h4')
    title = None

    if len(title_nodes) != 0:
        title = title_nodes[0].get_attribute('title')

    result_goods.append({
        'title': title,
        'price': price
    })

save_goods_to_db(result_goods)