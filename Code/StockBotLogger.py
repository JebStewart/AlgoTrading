import pandas as pd
from datetime import datetime

class Log:
    def __init__(self):
        self.filepath = r'/home/jeb/TraderBotLogs/stock_bot_log.pkl'
    
    def add_line(self, text, symbol= None, bought_sold = None, amount = None):
        """
        text: [Str] message to store (errors, info, etc.)
        symbol: [Str] symbol of stock purchased or sold, default=None
        bought_sold: [Str] whether the stock was 'BOUGHT' or 'SOLD', default=None
        amount: [Float] value of stock bought or sold, default=None
        """
        df = self.load_log()
        new_line = pd.DataFrame()
        new_line['Datetime'] = [datetime.now()]
        new_line['Message'] =[text]
        new_line['Symbol'] = [symbol]
        new_line['Bought/Sold'] = [bought_sold]
        new_line['Amount'] =  [amount]
        df = df.append(new_line)
        self._save_log(df)

    def load_log(self):
        """Returns the existing log as a dataframe."""
        df = pd.read_pickle(self.filepath)
        return df

    def _save_log(self, df):
        """Overwrites old log with existing log."""
        df.to_pickle(self.filepath)

    def _RESET_LOG(self):
        """ Only for use before deploying the code."""
        answer = input('Are you sure you want to reset? Y/n ')
        if answer == 'Y':
            df =pd.DataFrame()
            df['Datetime'] = [datetime.now()]
            df['Message'] = ['Initialized Log']
            df['Symbol']=[None]
            df['Bought/Sold'] = [None]
            df['Amount'] = [None]
            df.to_pickle(self.filepath)



if __name__ == '__main__':
    Log()._RESET_LOG()