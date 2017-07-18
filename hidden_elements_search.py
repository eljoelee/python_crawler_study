from selenium import webdriver
from selenium.webdriver.common.by import By

driver =   webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1/bin/phantomjs')
driver.get("http://www.naver.com")

links = driver.find_elements(By.XPATH, "//a")

for link in links:
    if not link.is_displayed():
        print("The link "+link.get_attribute("href")+" is a hidden link")

fields = driver.find_elements(By.XPATH, "//input")

for field in fields:
    if not field.is_displayed():
        print("Do not change value of "+field.get_attribute("name"))