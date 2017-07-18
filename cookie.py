from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1/bin/phantomjs')
driver.get("http://naver.com")
driver.implicitly_wait(1)

#delete_cookie, add_cookie, delete_all_cokies
print(driver.get_cookies())