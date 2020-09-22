import pandas as pd
import yfinance as yf


class MyMoney:
    """
    This class serves to manage the portfolio/money aspect of the simulation.
    """
    def __init__(self, starting_funds):
        self.funds = starting_funds
        self.portfolio = {}
        self.chunk_pct = .2
    
    def add_to_portfolio(self, symbol, amount, date_added):
        if symbol not in self.portfolio.keys():
            self.portfolio[symbol] = [amount, date_added]
            self.funds = self.funds - amount
        else:
            self.portfolio[symbol] = [self.portfolio[symbol][0]+ amount, date_added]
            self.funds = self.funds - amount

    def sell_from_portfolio(self, symbol, pct_change):
        self.funds += (self.portfolio[symbol][0] + (self.portfolio[symbol][0]*pct_change))
        print('SOLD!', symbol)
        self.portfolio.pop(symbol)

    def total_portfolio(self, _date):
        total_amount = self.funds
        _keys = list(self.portfolio.keys())
        if len(_keys) == 0:
            return self.funds
        for i in _keys:
            date_bought = self.portfolio[i][1]
            date_sold = _date
            temp = df[df['Symbol']==i]
            buy_price = float(temp[temp['Date_Only']==date_bought]['Open'])
            sell_price = float(temp[temp['Date_Only']==date_sold]['Open'])
            pct_change = (sell_price-buy_price)/buy_price
            total_amount+= self.portfolio[i][0]+ (self.portfolio[i][0]*pct_change)
        return total_amount
    
    def get_amount(self, _date):
        want_to_spend = .2 * self.total_portfolio(_date)
        if want_to_spend< self.funds:
            return want_to_spend
        elif self.funds < want_to_spend and self.funds != 0:
            return self.funds
        else:
            return False
