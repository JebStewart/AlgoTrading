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
        self.home_url = r'https://robinhood.com/'
        self.driver = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.options = Options()
        self.symbol_by_list = {}
        self.list_by_symbol = {}
        
        self._login()
        if headless:
            self.options.headless = True
    
    def _login(self):
        self.driver.get(self.home_url + 'login')
        email = self.driver.find_element_by_name('username')
        email.send_keys(self.un)
        password = self.driver.find_element_by_name('password')
        password.send_keys(self.pw)
        sign_in = self.driver.find_elements_by_xpath('//footer/div/button')[0]
        sign_in.click()
        self._AUTHENTIFICATION()
        print('Successfully Logged In.')
        return True

    def _AUTHENTIFICATION(self):
        text_me_button = self.driver.find_elements_by_xpath('//footer/div/button')[0]
        text_me_button.click()
        code = input('Please enter verification code.')
        code_input = self.driver.find_element_by_name('response')
        code_input.send_keys(code)
        confirm_button = self.driver.find_elements_by_xpath('//footer/div/button')[1]
        confirm_button.click()
        return True

    def _load_list_page(self, list_name):
        search_bar = self.driver.find_element_by_id('downshift-10-input')
        search_bar.send_keys(list_name)
        list_button = self.driver.find_element_id('downshift-10-item-6')
        list_button.click()
        #go through auto populate and click first one (of lists)

    def get_lists(self, symbol):
        symbols = []
        url = self.base_stock_url + symbol
        url = r'https://robinhood.com/lists/robinhood/3abb2fa2-5599-4357-97ae-e9a113bba139'
        self.driver.get(url)
        #row = self.driver.find_elements_by_xpath('//a/div/span') # Switch to list getter pattern
        row = self.driver.find_elements_by_class_name('css-lvdcxym')
        for i in row:
            print(i)
        self.list_by_symbol[symbol] = []

    def get_symbols(self, list_name):
        pass
#May need to do the more complicated way of search and click :(

if __name__ == '__main__':
    rhs = RHScraper()
    #rhs.get_lists('TSLA')
    #rhs._load_list_page('Technology')
    rhs._load_list_page()







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