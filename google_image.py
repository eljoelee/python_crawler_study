# -*- coding: utf-8 -*-
from selenium import webdriver
import base64
from bs4 import BeautifulSoup
import time
import re
import os

'''
우분투에서 텐서플로우 이미지 학습용으로 구글 이미지 추출...하려 했으나
구글은 이미지 제한적으로 20개까지 추출만 가능..인지 내 실력이 부족한 것인지 모름
그래서 bing.com 이미지 추출로 넘어감.
'''

count = 0

keyword = input("dogs : ")

directory = "/media/eljoelee/HDD2/train/input/dogs/"+keyword

if not os.path.exists(directory):
    os.makedirs(directory)

driver = webdriver.Firefox()
driver.get("https://www.google.co.kr/search?q="+keyword+"&tbm=isch")
time.sleep(3)

html = driver.page_source
bsObj = BeautifulSoup(html, "html.parser")

imageLocation = bsObj.find("div", {"id":"rg"}).findAll("img")

for b64ToImg in imageLocation:
    if count < 20:
        fileName = directory + "/" + keyword + str(count) + ".jpg"
        try:
            if b64ToImg.attrs['src'] is not None:
                if re.search('^data:image/.+;base64,', b64ToImg.attrs['src']):
                    image = re.sub('^data:image/.+;base64,', '', b64ToImg.attrs['src'])

            with open(fileName, "wb") as f:
                f.write(base64.b64decode(image))
                count += 1
        except:
            print("error : " + image)

f.close()
driver.close()