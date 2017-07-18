from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time

def getLinks(url):
    global pageCount, data, index

    pageCount += 1

    driver.get(url)
    time.sleep(2)

    # find_element_by_id("boardListContainer").find_elements_by_css_selector("table > tbody > tr")
    trList = driver.find_elements(By.XPATH, "//div[@id='boardListContainer']//table//tbody//tr")

    for tr in trList :
        td = tr.find_elements(By.TAG_NAME, "td")[0].text

        # Unit Testing
        assert td is not None

        if td != "[공지]":
            data[index] = td
            index+=1

    # bsObj.find("div", {"class": "paging"}).strong.get_text())
    count = int(driver.find_element(By.XPATH, "//div[@class='paging']//strong").text)

    if count == 1:
        getContent(data)
    else:
        currentLink = "http://soccerline.kr/board?categoryDepth01=5&page="+str(pageCount)
        getLinks(currentLink)

def getContent(data):
    for page in data:
        print(str(page))

        # Unit Testing
        assert page is not None

        if page is not None:
            absoluteLink = "http://soccerline.kr/board/"+str(page)
            driver.get(absoluteLink)
            time.sleep(3)
            try:
                # bsObj.find("div",{"class":"titBox"}).h2.get_text()
                txtTitle = driver.find_element(By.XPATH, "//div[@class='titBox']//h2").text

                # bsObj.find("div",{"class":"txtBox"}).get_text()
                txtContent = driver.find_element(By.XPATH, "//div[@class='txtBox']").text
            except AttributeError as e:
                print(str(e))
            else:
                txtTitle = re.sub('신고*', '', txtTitle)
                print(txtTitle + "\n" + txtContent)
                f.write(txtTitle + "\n" + txtContent)
        else:
            pass

if __name__ == '__main__':
    driver = webdriver.Chrome('D:/chromedriver')

    pageCount = 0
    index = 0
    data = [None] * 5000

    f = open("싸줄.txt", 'w', encoding="UTF8")

    url = "http://soccerline.kr/board?categoryDepth01=5"

    getLinks(url)

    driver.close()
    f.close()