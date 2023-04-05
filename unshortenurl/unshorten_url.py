from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
 
from selenium.webdriver.common.by import By

#the web that helps us to unshorten our url
driver.get("https://unshorten.it/")

#locating element in html
email = driver.find_element(By.ID, "short-url")

#type in the shorten url that want to expand
email.send_keys('https://reurl.cc/QL2RAO')

button = driver.find_element(By.ID, "unshorten-button")
button.submit()

time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')
print(soup.find('p',{'class':"data"}).text)

driver.close()
