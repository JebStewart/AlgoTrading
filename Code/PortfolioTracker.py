import pandas as pd
from datetime import datetime, date

class Portfolio:
    def __init__(self):
        self.location = r'/home/jeb/TraderBotLogs/my_portfolio.pkl'
        self.portfolio = None


    def get_available_funds(self):
        return 0

    def add_to_portfolio(self, symbol):
        self.load_portfolio()
        if symbol not in list(self.portfolio['Symbol']):
            temp = pd.DataFrame()
            temp['Symbol'] = [symbol]
            temp['Date_Bought'] = [date.today()]
            self.portfolio = self.portfolio.append(temp)
            self.save_portfolio()

    def remove_from_portfolio(self, symbol):
        self.load_portfolio()
        self.portfolio.drop(self.portfolio[self.portfolio['Symbol']==symbol].index, inplace=True)
        self.save_portfolio()
    
    def save_portfolio(self):
        self.portfolio.to_pickle(self.location)

    def load_portfolio(self):
        self.portfolio = pd.read_pickle(self.location)

    def reset_portfolio():
        df = pd.DataFrame()
        df['Symbol'] = []
        df['Date_Bought'] = []
        df.to_pickle(self.location)

    def portfolio_contents(self):
        self.load_portfolio()
        return self.portfolio


if __name__ == '__main__':
    p = Portfolio()
    p.add_to_portfolio('TSLA')
    p.add_to_portfolio('TSLA')
    print(p.portfolio_contents())
    p.remove_from_portfolio('TSLA')
    print(p.portfolio_contents())
