from selenium import webdriver

import asyncio
from selenium .webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
from itertools import cycle
import time

driver = webdriver.Chrome('C:\ChromeDriver\chromedriver')

async def load_tvsi(ticker):
    stock_url = 'https://finance.tvsi.com.vn/Enterprises/FinancialStatements?symbol={}'.format(ticker)
    driver.get(stock_url)
    driver.find_element_by_id('a_change_en').click()
    await asyncio.sleep(5)


def get_bs():
    fin_tr = driver.find_elements_by_xpath('//*[@id="table_bcdkt"]/tbody//tr')

    heading = fin_tr[0].find_elements_by_tag_name('td')

    title_array = []

    for header in heading:
        title_array.append(header.text)

    row_data = []
    for index, row in enumerate(fin_tr):
        row_array = []
        if (index > 0):
            for row_fin in row.find_elements_by_tag_name('td'):
                row_array.append(row_fin.text)
            row_data.extend([row_array])
    row_data = np.array(row_data)

    data = pd.DataFrame(data=row_data, columns=title_array)
    data.replace('', np.nan, inplace = True)
    data.dropna(how='all', axis=0, inplace = True)
    data.dropna(how = 'all', axis = 1, inplace = True)
    data.to_csv('BalanceSheet.csv')
    driver.close()

async def load_is():
    driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[2]').click()
    await asyncio.sleep(5)

def get_is():
    asyncio.run(load_is())

    fin_tr = driver.find_elements_by_xpath('//*[@id="table_bckqkd"]/tbody//tr')

    heading = fin_tr[0].find_elements_by_tag_name('td')

    title_array = []

    for header in heading:
        title_array.append(header.text)

    row_data = []
    for index, row in enumerate(fin_tr):
        row_array = []
        if (index > 0):
            for row_fin in row.find_elements_by_tag_name('td'):
                row_array.append(row_fin.text)
            row_data.extend([row_array])
    row_data = np.array(row_data)

    data = pd.DataFrame(data=row_data, columns=title_array)
    data.replace('', np.nan, inplace = True)
    data.dropna(how='all', axis=0, inplace = True)
    data.dropna(how = 'all', axis = 1, inplace = True)
    data.to_csv('IncomeStatement.csv')
    driver.close()

async def load_cf():
    driver.find_element_by_xpath('//*[@id="analyze"]/div[4]/ul/li[3]').click()
    await asyncio.sleep(5)

def get_cf():
    asyncio.run(load_cf())
    fin_tr = driver.find_elements_by_xpath('//*[@id="table_lctttructiep"]/tbody//tr')

    heading = fin_tr[0].find_elements_by_tag_name('td')

    title_array = []

    for header in heading:
        title_array.append(header.text)

    row_data = []
    for index, row in enumerate(fin_tr):
        row_array = []
        if (index > 0):
            for row_fin in row.find_elements_by_tag_name('td'):
                row_array.append(row_fin.text)
            row_data.extend([row_array])
    row_data = np.array(row_data)

    data = pd.DataFrame(data=row_data, columns=title_array)
    data.replace('', np.nan, inplace=True)
    data.dropna(how='all', axis=0, inplace=True)
    data.dropna(how='all', axis=1, inplace=True)
    data.to_csv('Cashflow.csv')
    driver.close()


asyncio.run(load_tvsi('HPG'))
get_bs()
get_is()
get_cf()
