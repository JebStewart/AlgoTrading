#ATRaC - Automatically Trades Rarely and Carefully (Work in progress)

#This is the actual script I will set on a cron job to execute everything together.

import pandas as pd 
import yfinance as yf
from datetime import date, timedelta
import robin_stocks as chirp
import pyotp

class ATRaC:
    def __init__(self):
        self.un = input('USERNAME:')
        self.pw = input('PASSWORD:')
        self.my_portfolio = chirp.build_holdings()
    
    def _login(self):
        chirp.login(self.un, self.pw)

    def buy_stock(self, symbol, value):
        #chirp.order_buy_fractional_by_price(symbol, value)
        print('Placeholder so I do not accidentally use this.')

    def sell_stock(self, symbol):
        """"Sell all of a stock """
        amount_to_sell = self.get_equity(symbol)
        chirp.order_sell_fractional_by_price(symbol, amount_to_sell)

    def get_equity(self, symbol):
        self.update_portfolio()
        return float(self.my_portfolio[symbol]['equity'])
    
    def update_portfolio(self):
        self.my_portfolio = chirp.build_holdings()


if __name__ == '__main__':
    #Get the daily date
    #go through all the symbols and get inputs for model
    #make predictions for what should be purchased
    #check to see if anything is ready to sell
    #sell everything mature
    #buy based on predictions
    #shoot me an email containing the portfolios current value and buy sell log