import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import  Options
import pandas as pd
import string
from time import sleep
from NotifyMe import Notifier

class SymbolScraper:
    def __init__(self, headless = False):
        self.first_page = r'http://www.eoddata.com/symbols.aspx'
        self.DRIVER_PATH =r'/home/jeb/DataScience/AlgoTrading/FirefoxDriver/geckodriver'
        self.driver = webdriver.Firefox(executable_path=self.DRIVER_PATH)
        self.options = Options()
        if headless:
            self.options.headless = True

    def get_all_symbols(self):
        symbols = []
        self.driver.get(self.first_page)
        for letter in string.ascii_uppercase: 
            row = self.driver.find_elements_by_xpath('//tr/td/a')
            for j in row:
                my_text = j.text
                my_text.replace(' ', '')
                if len(my_text) > 0 and my_text[0] == letter:
                    symbols.append(my_text)
            self.go_to_next_page(letter)
        return ', '.join(symbols)
    
    def go_to_next_page(self, letter):
        #find button
        #click on button
        sleep(30)
    



if __name__ == '__main__':
    ss = SymbolScraper()
    n = Notifier
    symbols = ss.get_all_symbols()
    print(symbol)
   
   #n.notify('Done aggregating symbols')