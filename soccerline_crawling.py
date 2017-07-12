from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time

driver = webdriver.Chrome('D:/chromedriver')
pageCount = 0
index = 0
data = [None] * 5000

f = open("싸줄.txt",'w', encoding="UTF8")

def getLinks(url):
    global pageCount
    global data
    global index

    pageCount += 1

    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    bsObj = BeautifulSoup(html, "html.parser")

    table = bsObj.find("div",{"id":"boardListContainer"}).find("table")

    for tr in table.tbody.findAll("tr"):
        td = tr.findAll("td")[0].get_text()
        if td != "[공지]":
            data[index] = td
            index+=1

    count = int(bsObj.find("div", {"class": "paging"}).strong.get_text())

    if count == 200:
        getContent(data)
    else:
        currentLink = "http://soccerline.kr/board?categoryDepth01=5&page="+str(pageCount)
        getLinks(currentLink)

def getContent(data):
    print(len(data))
    for page in data:
        print(str(page))
        if page is not None:
            absoluteLink = "http://soccerline.kr/board/"+str(page)
            driver.get(absoluteLink)
            time.sleep(3)
            html = driver.page_source
            bsObj = BeautifulSoup(html, 'html.parser')
            try:
                txtTitle = bsObj.find("div",{"class":"titBox"}).h2.get_text()
                txtContent = bsObj.find("div",{"class":"txtBox"}).get_text()
            except AttributeError as e:
                print(str(e))
            else:
                txtTitle = re.sub('신고*', '', txtTitle)
                print(txtTitle + "\n" + txtContent)
                f.write(txtTitle + "\n" + txtContent)
        else:
            pass

if __name__ == '__main__':
    url = "http://soccerline.kr/board?categoryDepth01=5"
    getLinks(url)
    driver.close()
    f.close()