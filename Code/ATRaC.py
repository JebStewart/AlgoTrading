#ATRaC - Automatically Trades Rarely and Carefully (Name work in progress)

#This is the actual script I will set on a cron job to execute everything together.
#Set to run before market open on the day of the purchases you want to make, 
# i.e. run at 7 am of tuesday, collect inputs from monday, then at open on tuesday 
# make sales and purchases

import pandas as pd 
import yfinance as yf
from datetime import date, timedelta
import robin_stocks as chirp
import pyotp
from NotifyMe import Notifier
from TraderModel import ModelTools
from PortfolioTracker import Portfolio
from StockBotLogger import Log

class ATRaC:
    def __init__(self):
        self.login_df= pd.read_pickle()
        self.un = self.login_df['Username'].iloc[0]
        self.pw = self.login_df['Password'].iloc[0]
        self._login()
        self.my_portfolio = Portfolio()
        self.mt = ModelTools()
        self.L = Log()
    
    def _login(self):
        chirp.login(self.un, self.pw)

    def amount_to_buy(self):
        """
        Current Rules:
        1. Never buy more than 10% of total accound value
        2. If there isn't 10% of total available, spend roughly what is left.
        3. If less than a dollar is left of buying power, return 0
        """
        buying_power = float(chirp.load_account_profile()['portfolio_cash'])
        if buying_power<1:
            return 0
        total_equity = float(chirp.load_portfolio_profile()['equity'])
        ten_percent_of_portfolio = (buying_power+total_equity)*.1
        if ten_percent_of_portfolio<buying_power:
            return ten_percent_of_portfolio
        else:
            return buying_power*.9


    def buy_stock(self, symbol):
        value = self.amount_to_buy()
        if value==0:
            self.L.add_line(f'Not enough money to buy {symbol}, purchase not made.')
        else:
            chirp.order_buy_fractional_by_price(symbol, value)
            self.L.add_line('', symbol, 'BOUGHT', value)
            self.my_portfolio.add_to_portfolio(symbol)

    def sell_stock(self, symbol):
        """"Sell all of a stock """
        amount_to_sell = self.get_equity(symbol)
        chirp.order_sell_fractional_by_price(symbol, amount_to_sell)
        self.L.add_line('', symbol, 'SOLD', amount_to_sell)

    def get_equity(self, symbol):
        self.update_portfolio()
        return float(self.my_portfolio[symbol]['equity'])
    
    def update_portfolio(self):
        self.my_portfolio = chirp.build_holdings()
    
    def stocks_to_sell(self):
        port = self.my_portfolio.portfolio_contents()
        today = date.today()
        sell_me = []
        if today.weekday() not in [5, 6]:
            for i in list(port['Symbol'].unique()):
                bought_date = port[port['Symbol'] == i]['Date_Bought'].iloc[0]
                if bought_date+timedelta(days=2)<today:
                    sell_me.append(i)
        return sell_me



if __name__ == '__main__':
    #Get tools set up
    A = ATRaC()
    N = Notifier()
    today = date.today()
    all_symbols = ['ACB', 'F', 'GE', 'DIS', 'AAL', 'GPRO', 'DAL', 'MSFT', 'CCL', 'AAPL', 'FIT', 'SNAP', 'PLUG', 
                   'BAC', 'BA', 'NCLH', 'INO', 'UAL', 'UBER', 'CGC', 'TSLA', 'AMD', 'CRON', 'RCL', 'TWTR', 
                   'GRPN', 'FB', 'SBUX', 'MRO', 'ZNGA', 'BABA', 'T', 'KO', 'APHA', 'USO', 'XOM', 'AMZN', 'MFA', 
                   'JBLU', 'NIO', 'MRNA', 'LUV', 'GM', 'GILD', 'MGM', 'SAVE', 'NFLX', 'NRZ', 'SPCE', 'LK', 
                   'VSLR', 'AMC', 'PENN', 'VOO', 'TLRY', 'HAL', 'NOK', 'NVDA', 'CPRX', 'LYFT', 'SQ', 'SPY', 
                   'V', 'NKE', 'SIRI', 'UCO', 'WORK', 'CPE', 'BYND', 'KOS', 'ET', 'OXY', 'PFE', 'ZM', 'CRBP', 
                   'SPHD', 'FCEL', 'VKTX', 'JPM', 'NTDOY', 'NYMT', 'BP', 'ATVI', 'CSCO', 'WFC', 'WMT', 'GOOGL', 
                   'INTC', 'GLUU', 'AUY', 'VTI', 'ERI', 'TXMD', 'SNE', 'PTON', 'ROKU', 'JNJ', 'IVR', 'MU']
    #TODO figure out which symbols I want this to work with/ add more in from robinhood
    stocks_to_buy = []
    for symbol in all_symbols:
        prediction = A.mt.make_prediction(symbol, date.today())
        if prediction:
            stocks_to_buy.append(symbol)
    sell_list = A.stocks_to_sell()
    for symbol in sell_list:
        A.sell_stock(symbol)
    for symbol in stocks_to_buy:
        A.buy_stock(symbol)
    sell_msg = ', '.join(sell_list)
    buy_msg = ', '.join(stocks_to_buy)
    N.notify(f'Good morning Jeb, I have successfully run my prediction algorithm for today. \n Stocks bought: \n {buy_msg} \n Stocks sold: \n {sell_msg}')
