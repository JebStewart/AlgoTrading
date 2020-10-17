import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import  Options
import pandas as pd
import string
from time import sleep
from NotifyMe import Notifier

class RHScraper:
    def __init__(self, headless = False):
        self.DRIVER_PATH =r'/home/jeb/DataScience/AlgoTrading/FirefoxDriver/geckodriver'
        self.base_stock_url = r'https://robinhood.com/stocks/'
        self.driver = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.symbol_by_list = {}
        self.list_by_symbol = {}
        if headless:
            self.options.headless = True

    def get_tags(self, symbol):
        symbols = []
        url = self.base_stock_url + symbol
        self.driver.get(url)
        row = self.driver.find_elements_by_xpath('//a/div/span') # Switch to list getter pattern
        print(row)
        self.list_by_symbol[symbol] = []

    def get_symbols(self, tag):
        pass
#May need to do the more complicated way of search and click :(

if __name__ == '__main__':
    rhs = RHScraper()
    rhs.get_tags('TSLA')






# lists = ['100 Most Popular',
#          'Top Movers',
#          'Cannabis',
#          'Healthcare Supplies',
#          'Index ETFs',
#          'Technology',
#          'Pharma',
#          'Consumer Goods',
#          'Food & Drink',
#          'Energy & Water',
#          'Finance',
#          'Tech, Mediam & Telecom',
#          'Healthcare',
#          'ETFs',
#          'Energy',
#          'Entertainment',
#          'Agriculture',
#          'Business',
#          'Real Estate',
#          'Healthcare Services',
#          'Apparel & Accessories',
#          'Automotive',
#          'Banking',]