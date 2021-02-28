from bs4 import BeautifulSoup
import requests
import time
from pprint import pprint
from selenium import webdriver
# *******************************CONSTANTS*******************************************
WEB_DRIVER_PATH = "C:\devlopment\chromedriver_win32\chromedriver.exe"

# ********************************** headers ****************************************
headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}
# ********************************** requests ***************************************
response = requests.get(
    url="https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
    headers=headers
)

# ***************************** making soup *****************************************
zillow_wpg = response.text
soup = BeautifulSoup(zillow_wpg, 'html.parser')
# print(soup.prettify())

# ***************************** FINDING TAGS *****************************************
all_prices = []
price_tags = soup.select('.list-card-price')
for price in price_tags:
    if '+' in price.text:
        all_prices.append(price.getText().split('+')[0])

    elif '/' in price.text:
        all_prices.append(price.getText().split('/')[0])

    elif ' ' in price.text:
        all_prices.append(price.getText().split(' ')[0])

    else:
        all_prices.append(price.getText())
pprint(all_prices)


all_links = []
all_links_tags = soup.select('.list-card-top a')
for link in all_links_tags:
    href = link['href']
    if 'https' not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)
pprint(all_links)

all_address = []
all_adresss_tags = soup.select(".list-card-addr")
for address in all_adresss_tags:
    all_address.append(address.getText())
pprint(all_address)

# ********************************** using selenium **************************************
driver = webdriver.Chrome(executable_path=WEB_DRIVER_PATH)



for n in range(len(all_links)):

    driver.get(url=
               'https://docs.google.com/forms/d/e/1FAIpQLSfGUW7G9PdbWja91lMSFMFtFY8SJHzyidOIQoBuDFM6sOrW8w/viewform?usp=sf_link'
               )

    time.sleep(2)

    address_ans = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_ans = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_ans = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    submit_button = driver.find_element_by_xpath(
                                                 '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div'
    )

    address_ans.send_keys(all_address[n])
    price_ans.send_keys(all_prices[n])
    link_ans.send_keys(all_links[n])
    submit_button.click()
    time.sleep(2)

