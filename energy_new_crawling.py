# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import sys

news = set()

html_header = '''
<html>
<body>
<table border=1>
<tr>
    <td>제목</td>
    <td>링크</td>
</tr>
'''

html_footer = '''
</tr>
</table>
</body>
</html>
'''

now = time.localtime()

keyword = input("검색할 키워드 입력 : ")
page_count = int(input("페이지수 : "))

file_name = "%04d_%02d_%02d_기사.html"%(now.tm_year, now.tm_mon, now.tm_mday)
f = open(file_name, 'w', encoding='UTF8')
f.write(html_header)

driver = webdriver.Chrome('D:/chromedriver')

def getLinks(pageUrl):
    driver.get(pageUrl)
    time.sleep(3)
    html = driver.page_source
    bsObj = BeautifulSoup(html, "html.parser")

    for dl in bsObj.find("ul", {"class":"type01"}).findAll("dl"):
        updateTime = dl.find("dd",{"class":"txt_inline"}).get_text()
        if re.search("[0-9]+(분 전|시간 전)+", updateTime):
            if 'href' in dl.dt.a.attrs:
                if '#' not in dl.dt.a.attrs['href']:
                    if dl.dt.a.get_text() not in news:
                        news.add(dl.dt.a.get_text())
                        f.write("<tr>")
                        f.write("<td>"+dl.dt.a.get_text()+"</td>")
                        f.write("<td><a href='"+dl.dt.a.attrs['href']+"'>기사 링크</a></td>")
                        f.write("</tr>")

    count = int(bsObj.find("div", {"class":"paging"}).strong.get_text())

    if count == page_count:
        driver.close()
        f.write(html_footer)
        f.close()
        sys.exit(1)

    driver.find_element_by_css_selector('.paging>.next').click()
    getLinks(driver.current_url) 

getLinks("https://search.naver.com/search.naver?where=news&sm=tab_jum&ie=utf8&query="+keyword)