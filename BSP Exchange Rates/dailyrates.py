import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

bsp_url = 'https://www.bsp.gov.ph/SitePages/Statistics/ExchangeRate.aspx'
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(bsp_url)
time.sleep(2)

date_today = datetime.date.today()
date_today = date_today.strftime("%B %d, %Y")
bsp_date = driver.find_element(By.ID, "date").text
if bsp_date == date_today:
    table = driver.find_element(By.ID, "tb1")
    table2 = driver.find_element(By.ID, "tb2")
    rows = table.find_elements(By.TAG_NAME, "tr")
    rows2 = table2.find_elements(By.TAG_NAME, "tr")
    exrate = []
    for row in rows:
        row_data = row.find_elements(By.TAG_NAME, "td")
        if len(row_data) > 1:
            if row_data[2].text in symbol_rates:
                exrate_data = {"Country": row_data[0].text, "Unit": row_data[1].text, "Symbol": row_data[2].text,
                           "PHP Equivalent": float(row_data[5].text)}
                exrate.append(exrate_data)
    for row2 in rows2:
        row2_data = row2.find_elements(By.TAG_NAME, "td")
        if len(row2_data) > 1:
            if row2_data[2].text in symbol_rates:
                exrate_data = {"Country": row2_data[0].text, "Unit": row2_data[1].text, "Symbol": row2_data[2].text,
                           "PHP Equivalent": float(row2_data[5].text)}
                exrate.append(exrate_data)
    exratefile = f"dailyrate {date_today}.xlsx"
    df = pd.DataFrame(exrate)
    df.to_excel(exratefile)
else:
    print('no daily rates for today')