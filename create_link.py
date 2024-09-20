import requests
from bs4 import BeautifulSoup
import random
import time 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_useragent():
    return random.choice(_useragent_list)

_useragent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
    ]

url='https://www.google.com/search?q=realestateinvesting+reddit&tbs=cdr:1,cd_min:1/6/2023,cd_max:1/7/2023&as_sitesearch=reddit.com/r/realestateinvesting/&start=10'

# to use browser in background without displayingo on screen

# Initialize the WebDriver 
driver = webdriver.Chrome()

# Open page
driver.get(url)
time.sleep(2)
response=driver.page_source
            
soup=BeautifulSoup(response,'html5lib')
result_block = soup.find_all("div", attrs={"class": "g"})
print(len(result_block))
for result in result_block:
    link = result.find("a", href=True)['href']
    print(f'Link: {link}')

time.sleep(5)
driver.close()
