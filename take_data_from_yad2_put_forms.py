from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
import time

option = ChromeOptions()
option.add_experimental_option("detach", True)
service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(options=option, service=service)


def get_data_from_yad2():

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/114.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8"
    }

    response = requests.get("https://www.yad2.co.il/realestate/rent?topArea=2&area=4&city=7900&rooms=-1-3",
                            headers=headers)
    yad2_page = response.text
    soup = BeautifulSoup(yad2_page, "html.parser")
    # Find the direction
    directions_html = soup.find_all(name="span", class_="subtitle")
    directions = [direction.text for direction in directions_html]
    # Find the price
    price_html = soup.select("div.feeditem.table div.price")
    price = [price.text.strip() for price in price_html]
    # Find the square meters
    meters_2_html = soup.select("div.feeditem.table div.data.SquareMeter-item span.val")
    meters_2 = [meter.text for meter in meters_2_html]

    return directions, price, meters_2


def put_in_google_forms(direction, price, m2):

    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSd0iwMOgNqzRvxLKx6uHsc49FXpCdo1wpgidm2yrtsJG75Khw/"
               "viewform?usp=sf_link")

    put_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]'
                                                 '/div/div[1]/input')
    put_address.send_keys(direction)
    put_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/'
                                              'div[2]/div/div[1]/div/div[1]/input')
    put_price.send_keys(price)
    put_m2 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/'
                                           'div[1]/input')
    put_m2.send_keys(m2)
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()


def main():
    directions_price_meters2_tuple = get_data_from_yad2()
    index = 0
    for _ in directions_price_meters2_tuple[0]:
        direction = directions_price_meters2_tuple[0][index]
        price = directions_price_meters2_tuple[1][index]
        meter2 = directions_price_meters2_tuple[2][index]
        put_in_google_forms(direction, price, meter2)
        index += 1
        time.sleep(1)


main()
