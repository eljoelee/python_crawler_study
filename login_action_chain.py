from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time

driver = webdriver.Chrome('D:/chromedriver')
driver.get("url")

inputId = driver.find_element(By.XPATH, "//input[@name='id']")
inputPw = driver.find_element(By.XPATH, "//input[@name='pw']")

'''
inputId.send_keys("ID")
inputPw.send_keys("PW")
driver.find_element(By.XPATH, "//input[@type='submit']").click()
'''

actions = ActionChains(driver).click(inputId).send_keys("ID").click(inputPw).send_keys("PW").send_keys(Keys.RETURN)

actions.perform()

time.sleep(3)

driver.close()