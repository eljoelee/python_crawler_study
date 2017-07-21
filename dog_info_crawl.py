from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

def getLink(url):
    dogName = []

    driver.get(url)
    time.sleep(2)

    names = driver.find_elements(By.XPATH, "//div[@class='appcenter gic']//a[@class='klitem']")

    for name in names:
        dogName.append(name.get_attribute('title'))

    getInfo(dogName)

def getInfo(dogName):
    for query in dogName:
        url = "https://www.google.co.kr/search?q="+query
        driver.get(url)
        time.sleep(3)

        try:
            dogInfo = driver.find_element(By.XPATH, "//div[@class='_RBg']").text
        except NoSuchElementException as e:
            print(str(e))
        else:
            if '수명' in dogInfo:
                print(query + '\n' + dogInfo + '\n')

if __name__ == '__main__':

    driver = webdriver.Chrome('D:/chromedriver')

    url = "https://www.google.co.kr/search?q=개종류"

    getLink(url)

    driver.close()