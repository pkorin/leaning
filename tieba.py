import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from config import *
import pymongo

client = pymongo.MongoClient(mongo_url)
db = client[mongo_db]
key_word = '碧蓝幻想'
brower = webdriver.Chrome()
wait = WebDriverWait(brower,100)

def get_source(key_word):
    try:
        brower.get('https://tieba.baidu.com')
        inputword = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#wd1")))
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#tb_header_search_form > span.search_btn_wrap.search_btn_enter_ba_wrap > a")))
        inputword.send_keys(key_word)
        button.click()
    except TimeoutException:
        get_source(key_word)

def next_page():
    try:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#frs_list_pager > a.next.pagination-item")))
        get_page_source()
        button.click()
    except TimeoutException:
        next_page()

def get_page_source():
    #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.wrap1 > div")))
    doc = pq(brower.page_source)
    items = doc(".threadlist_bright .j_thread_list").items()
    for item in items:
        zidian = {
            'title':item.find('.threadlist_title').text(),
            'name':item.find('.frs-author-name-wrap').text(),
            'first':item.find('.threadlist_abs').text()
        }
        print(zidian)
        save_to_mongo(zidian)

def save_to_mongo(zidian):
    db[mongo_table].insert(zidian)

def main():
    get_source(key_word)
    for i in range(10):
        time.sleep(2)
        next_page()
        print(i)
    #brower.close()

if __name__ == '__main__':
    main()