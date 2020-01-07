from selenium import webdriver

from selenium .webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

portfolios = ['VCB', 'FPT', 'CTG', 'HPG', 'FLC']

driver = webdriver.Chrome('C:\ChromeDriver\chromedriver')

def load_page(ticker, page, fromDate, toDate):
    stock_url = 'http://ra.vcsc.com.vn/Stock?lang=en-US&page={}&ticker={}&from={}&to={}'.format(page, ticker,fromDate, toDate)
    driver.get(stock_url)

def stock_crawling(ticker, pageNumber):
    load_page(ticker, pageNumber ,'2019-01-05', '2020-01-06')
    stock_data = driver.find_elements(By.TAG_NAME, 'td')

    date_list = []
    open_list = []
    high_list = []
    low_list = []
    close_list = []

    for index, stock in enumerate(stock_data):
        if index % 14 == 0:
            date_list.append(stock.text)
        elif index % 14 == 2:
            open_list.append(stock.text)
        elif index % 14 == 3:
            high_list.append(stock.text)
        elif index % 14 == 4:
            low_list.append(stock.text)
        elif index % 14 == 5:
            close_list.append(stock.text)
        else:
            pass

    stock_df = pd.DataFrame(
        {'Date': date_list, 'Open': open_list, 'High': high_list, 'Low': low_list, 'Close': close_list})
    stock_df['Ticker'] = ticker
    return stock_df

stock_df = pd.DataFrame(columns = ['Date', 'Ticker' , 'Open', 'High', 'Low', 'Close'])

for ticker in portfolios:
    load_page(ticker, 1, '2019-01-05', '2020-01-06')
    page_count = len(driver.find_elements_by_class_name('number_paging')) + 1

    for i in range(page_count):
        print('Get {}, page number {}'.format(ticker, str(i + 1)))
        crawled_data = stock_crawling(ticker, i + 1)
        stock_df = stock_df.append(crawled_data, ignore_index=True, sort= False)
        print('{}, page number {} done!'.format(ticker, str(i + 1)))

    print('{} has been crawled successfully'.format(ticker))

print('Portfolio has been crawled!')
stock_df.to_csv('data.csv', index=False)
