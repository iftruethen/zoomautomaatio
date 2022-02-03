from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import string
import time

# def get_random_string(length):
#     letters = string.ascii_lowercase
#     result_str = ''.join(random.choice(letters) for i in range(length))
#     return result_str

class Hakija():
    def hae(self):
        url="tähän verkkosivun url" 
        driver = webdriver.Firefox()
        driver.get(url)
        # assert "Python" in driver.title
        elem = driver.find_element_by_partial_link_text('Kirjaudu')
        elem.click()
        time.sleep(2)
        elem = driver.find_element_by_partial_link_text('Login')
        elem.click()
        elem = driver.find_element_by_id("username")
        elem.clear()
        elem.send_keys("tähän käyttäjätunnus")
        elem = driver.find_element_by_id("password")
        elem.clear()
        elem.send_keys("tähän salasana")
        elem.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.get(url)
        time.sleep(5)
        elem = driver.find_element_by_xpath('//button[text()="Join Meeting"]')
        elem.click()
        time.sleep(2)
        i=driver.current_url
        code=""
        for j in i:
            if i in "123456789":
                code=code+i
        print(code)