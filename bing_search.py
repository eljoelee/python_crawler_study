from selenium import webdriver
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import time
import os

count = 30

keyword = input("dogs : ")

directory = "/media/eljoelee/HDD2/train/input/dogs/"+keyword

if not os.path.exists(directory):
    os.makedirs(directory)

driver = webdriver.Firefox()
driver.get("http://www.bing.com/images/search?FORM=HDRSC2&q="+keyword)
time.sleep(3)

html = driver.page_source
bsObj = BeautifulSoup(html, "html.parser")

imageLocation = bsObj.find("div", {"id":"mmComponent_images_1"}).findAll(src=True)

print(imageLocation)

for img in imageLocation:
    fileName = directory + "/" + keyword + str(count) + ".jpg"
    urlretrieve(img['src'], fileName)
    count += 1

driver.close()