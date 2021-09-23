from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

driver.get("https://www.youtube.com/")

time.sleep(3)
search = driver.find_element_by_name("search_query")
search.send_keys('사랑노래')
time.sleep(1)
search.send_keys(Keys.ENTER)
