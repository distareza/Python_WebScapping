from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import csv
import time

url = "https://www.alibaba.com/trade/search?fsb=y&IndexArea=product_en&CatId=&SearchText=paracord&viewtype=&tab="

alibaba_xpath = ["list-no-v2-main", "organic-offer-wrapper"]


def getHtmlContent(url):
    # https://www.geeksforgeeks.org/driving-headless-chrome-with-python/
    options = Options()
    options.headless = True

    # https://chromedriver.chromium.org/downloads
    chrome_drive_path = "C:/opt/chromedriver_win32/chromedriver.exe"
    selenium_service = Service(executable_path=chrome_drive_path)
    driver = webdriver.Chrome(options=options, service=selenium_service)
    driver.get(url)

    timeout = 5
    try_count = 1
    while True:
        try:
            # https://stackoverflow.com/questions/47790010/how-to-use-expected-conditions-to-check-for-an-element-in-python-selenium
            # https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
            WebDriverWait(driver, timeout).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//body'))
                and
                expected_conditions.any_of(
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, f'//div[contains( @class, "{alibaba_xpath[0]}")]')),
                    expected_conditions.presence_of_element_located(
                        (By.XPATH, f'//div[contains( @class, "{alibaba_xpath[1]}")]'))
                )
            )
            break
        except TimeoutException as te:
            try_count += 1
            if try_count > 10:
                print(f"Could not retrieve {url}")
                exit(1)
            else:
                print(f"Timeout, try {try_count} time")
                time.sleep(5)

    html = driver.page_source

    # for  debug purpose
    with open("alibaba.html", "w", encoding="UTF-8") as html_file:
        html_file.write(html)

    return html


html = getHtmlContent(url)
# html = open('alibaba.html', "r", encoding="UTF-8").read()

web_content = BeautifulSoup(html, 'html.parser')

data = []

for i in range(2):
    class_xpath = alibaba_xpath[i]
    if web_content.select(f"div.{class_xpath}"):
        for div in web_content.select(f"div.{class_xpath}"):

            product_name = ""
            product_price = ""
            if div.select(f"div.{class_xpath} h2.elements-title-normal__outter"):
                product_name = div.select(f"div.{class_xpath} h2.elements-title-normal__outter")[0].getText()
            try:
                product_price = div.select(f"div.{class_xpath} span.elements-offer-price-normal__price")[0].getText()
            except:
                pass

            print(f"{product_name}, {product_price}")
            data.append([product_name, product_price])
        break

with open("alibaba_stats.csv", "w", encoding="UTF8", newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["product name", "price"])
    for row in data:
        writer.writerow(row)
