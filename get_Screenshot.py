from selenium import webdriver

driver =   webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1/bin/phantomjs')
driver.get("http://www.naver.com")
driver.get_screenshot_as_file('naver.png')
driver.close()