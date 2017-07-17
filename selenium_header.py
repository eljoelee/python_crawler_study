from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def init_header(*args, **kwargs):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
               'Connection': 'keep-alive'}
    for key, value in headers.items():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'

    driver =   webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1/bin/phantomjs')
    driver.set_window_size(1400,1000)

    return driver

if __name__ == '__main__':
    service_args = [
        '--proxy=127.0.0.1:9999',
        '--proxy-type=http',
        '--ignore-ssl-errors=true'
    ]

    driver = init_header(service_args=service_args)
    driver.get('https://search.naver.com/search.naver?where=news&sm=tab_jum&ie=utf8&query=Nell')
    time.sleep(2)

    for dt in driver.find_elements(By.XPATH, "//ul[@class='type01']//li//dl//dt//a"):
        print(dt.text)

    driver.close()