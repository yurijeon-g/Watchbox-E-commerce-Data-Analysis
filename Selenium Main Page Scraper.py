import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

options = webdriver.ChromeOptions()
# Using selenium webdriver to automate scrolling down the page
driver = webdriver.Chrome(chrome_options=options, executable_path='C:/Users/Yuri/Downloads/linkedin-jobs-scraper-main/chromedriver.exe')
driver.get("https://www.thewatchbox.com/sg/en/watches/shop/all-watches/")

# Automatically scrolling down the page and clicking the "View More" button
SCROLL_PAUSE_TIME = 3
while True:
    driver.execute_script("window.scrollBy(0, 30);")
    time.sleep(SCROLL_PAUSE_TIME)
    try:
        view_more_button = WebDriverWait(driver, 200).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='grid-more-button']//div[@class='btn col-12 blackbgbtn']"))
        )
        view_more_button.click()
    except:
        break

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

products = soup.find_all("div", class_=lambda x: x and x.startswith("grid product-tiles"))

product_data = []
# Extracting product information from the page

for product in products:
        product_dict = {}

        product_name = product.find("span", class_="grid__name")
        if product_name:
            product_dict["Product name"] = product_name.text.strip()
        else:
            product_dict["Product name"] = None

        product_id = product.find("span", class_="grid__id")
        if product_id:
            product_dict["Product id"] = product_id.text.strip()
        else:
            product_dict["Product id"] = None

        brand = product.find("div", class_="grid__brand")
        if brand:
            product_dict["Brand"] = brand.text.strip()
        else:
            product_dict["Brand"] = None

        price = product.find("span", {"content": True})
        if price:
            product_dict["Price"] = price['content']
        else:
            product_dict["Price"] = None

        link = product.find("a", class_="link grid-carousel-link")
        if link:
            product_dict["Link"] = link['href']
        else:
            product_dict["Link"] = None

        year = product.find("div", class_="grid__year")
        if year:
            product_dict["year"] = year.text.strip()
        else:
            product_dict["year"] = None

        product_data.append(product_dict)

# Convert product data list to a pandas dataframe
df = pd.DataFrame(product_data)

# Export the dataframe as a csv file
df.to_csv("productdata14.csv", index=False)

# Closing the webdriver
driver.quit()


