# -*- coding: cp949 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import xlsxwriter

driver = webdriver.Chrome('D:/chromedriver')

driver.get('http://keps.energy.or.kr/beps/ST/MD/efficiencySearch.do?modelCode=all')

driver.find_elements_by_css_selector('ul.tabs-menu>li>a')[3].click()

select = Select(driver.find_element_by_id('newList'))

select.select_by_visible_text("물-물지열열펌프유니트")

driver.find_element_by_id('newSearch').click()

time.sleep(3)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

page = soup.find(id='sp_1_JQ_Pager3').text

tr_list = []

#int(page)
for i in range(0, int(page)):
    driver.find_element_by_id('next_JQ_Pager3').click()
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id="JQ_list3")
    tr_list += table.tbody.find_all('tr', class_='ui-widget-content jqgrow ui-row-ltr')

workbook = xlsxwriter.Workbook('물_물지열열펌프유니트.xlsx')
worksheet = workbook.add_worksheet()

for rdx, tr in enumerate(tr_list):
    td_list = tr.find_all('td')
    for ddx, td in enumerate(td_list):
        worksheet.write(rdx, ddx, td.text)

workbook.close()