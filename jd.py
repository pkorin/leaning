import requests
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from selenium.webdriver.common.by import By
from jd_config import *
import pymongo

client = pymongo.MongoClient(mongo_url)
db = client[mongo_db]
key_word = 'mp3'
brower = webdriver.Chrome()
wait = WebDriverWait(brower,100)

def get_source(key_word):
    try:
        brower.get('https://jd.com')
        inputword = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#key")))
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button > i")))
        inputword.send_keys(key_word)
        button.click()
    except TimeoutException:
        get_source(key_word)

def next_page():
    try:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_bottomPage > span.p-num > a.pn-next > em")))
        get_page_source()
        button.click()
    except TimeoutException:
        next_page()

def get_page_source():
    #wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.wrap1 > div")))
    doc = pq(brower.page_source)
    items = doc(".gl-warp .gl-item").items()
    for item in items:
        zidian = {
            'title':item.find('.p-name').text(),
            'name':item.find('.curr-shop').text(),
            'img':item.find('.p-img').attr('src')
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