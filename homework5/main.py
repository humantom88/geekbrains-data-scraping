from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from db import save_mails_to_db

driver = webdriver.Chrome()
driver.get('https://mail.ru/')

assert "Mail.ru" in driver.title

def login():
    try:
        elem = driver.find_element_by_id('mailbox:login')
        elem.send_keys('study.ai_172@mail.ru')
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        elem = driver.find_element_by_id('mailbox:password')
        elem.send_keys('NextPassword172')
        elem.send_keys(Keys.RETURN)
        time.sleep(5)

        return True
    except:
        return False

def load_articles_by_scroll():
    last_element = None
    while True:
        time.sleep(1)
        articles = driver.find_elements_by_class_name('llc')
        actions = ActionChains(driver)
        if last_element != articles[-1]:
            last_element = articles[-1]
            actions.move_to_element(last_element)
            actions.perform()
        else:
            break

def get_title_from_mail_node(node):
    title_span_node = node.find_elements_by_xpath('.//span[@class="ll-crpt"]')[0]
    return title_span_node.get_attribute('title')

def get_subject_from_mail_node(node):
    subject_node = node.find_elements_by_xpath('.//span[@class="ll-sj__normal"]')[0]
    return subject_node.text

def get_datetime_from_mail_node(node):
    date_node = node.find_elements_by_xpath('.//div[@class="llc__item llc__item_date"]')[0]
    return date_node.get_attribute('title')

def get_data_from_mails(mails):
    result_mails = []
    for mail in mails:
        mail = {
            'href': mail.get_attribute('href'),
            'title': get_title_from_mail_node(mail),
            'datetime': get_datetime_from_mail_node(mail),
            'content': None
        }
        result_mails.append(mail)

    return result_mails

login()
load_articles_by_scroll()

mail_nodes = driver.find_elements_by_xpath("//a[@class='llc js-tooltip-direction_letter-bottom js-letter-list-item llc_pony-mode llc_normal']")
result_info = get_data_from_mails(mail_nodes)

for mail in result_info:
    if mail['href'] is not None:
        try:
            driver.get(mail['href'])
            time.sleep(2)
            body = driver.find_elements_by_xpath('//div[@class="letter__body"]')[0]
            mail['content'] = body.text
            del(mail['href'])
            driver.back()
            time.sleep(1)
        except:
            pass

save_mails_to_db(result_info)