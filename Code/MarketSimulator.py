import pandas as pd
import yfinance as yf


class StockSimulator:
    def __init__(self, start_date, symbols, model):
        self._date = start_date
        self.end_date = date(2020, 9, 1)
        self.symbols = symbols
        self.money = MyMoney(1000)
        self._LOG = pd.DataFrame()
        self.TEMP_TRACKER_PRICE = []
        self.TEMP_TRACKER_DATE = []
        self.model = model
        self.input_symbols = ['Volume', 'Dividends', 'Stock Splits', 'Pct_Change', 'Three_Day_Movement', 'Five_Day_Movement']
        self.df = self.create_history_df()
    
    def create_history_df(self):
        start_date = self._date
        end_date =  self.end_date
        df = pd.DataFrame()
        for i in symbols:
            tckr = yf.Ticker(i)
            results = tckr.history(start=start_date, end = end_date)
            results['Symbol'] =[i]* int(results.shape[0])
            results.reset_index(inplace = True)
            df = df.append(results, ignore_index=True)
            print(i, 'dataframe added to base.')
        print('Complete')

        def daily_mean(x):
            values = [x['Open'], x['High'], x['Low'], x['Close']]
            return mean(values)
        def daily_stddev(x):
            values = [x['Open'], x['High'], x['Low'], x['Close']]
            return stdev(values)
        def daily_pct_change(x):
            return (x['Close']-x['Open'])/x['Open']
        def notable_change(x):
            return 1 if abs(x['Pct_Change']) > sym_std[x['Symbol']] else 0
        def prior_trend(x, num_of_days):
            _date =x['Date']
            _start = _date - timedelta(days=num_of_days)
            temp = df[df['Symbol'] == x['Symbol']]
            temp = temp[temp['Date'] <= _date]
            temp = temp[temp['Date']> _start]
            return temp['Pct_Change'].mean()

        df['Mean'] = df.apply(lambda x: daily_mean(x), axis=1)
        df['Std_Dev'] = df.apply(lambda x: daily_stddev(x), axis=1)
        df['Pct_Change'] = df.apply(lambda x: daily_pct_change(x), axis=1)
        sym_std = {}
        for i in symbols:
            temp = df[df['Symbol'] == i]
            sym_std[i] = temp['Pct_Change'].std()*2
            print(i, temp['Pct_Change'].std()*2)
        df['Notable_Change'] = df.apply(lambda x: notable_change(x), axis=1)
        df['Three_Day_Movement'] = df.apply(lambda x: prior_trend(x, 3), axis=1)
        df['Five_Day_Movement'] = df.apply(lambda x: prior_trend(x, 5), axis=1)
        df['Shifted_Notable_Change'] = df['Notable_Change'].shift(1)

        for i in symbols:
            #remove all the earliest dates to account for the shift
            temp = df[df['Symbol'] ==i]
            index = temp[temp['Date']==temp['Date'].iloc[0]].index
            df.drop(index, inplace=True)
        df['Date_Only'] = df['Date'].dt.date
        print('Feature Engineering Complete')
        self.df = df


    def collect_inputs(self): #SOMETHING WRONG HERE
        inputs = []
        for sym in self.symbols:
            temp = self.df[self.df['Symbol']==sym]
            temp = temp[temp['Date_Only']==self._date]
            temp = temp[self.input_symbols]
            inputs.append([sym,temp])
        return inputs

    def make_predictions(self, model_inputs):
        if model_inputs.empty:
            return False
        prediction = self.model.predict(model_inputs)
        if prediction != 0 and float(model_inputs['Pct_Change'])>0: 
            return True
        else:
            return False

    def transaction(self, symbol):
        amount = self.money.get_amount(self._date)
        if amount:
            print('Bought', symbol)
            self.money.add_to_portfolio(symbol, amount, self._date)

    def auto_sell(self):
        _keys = list(self.money.portfolio.keys())
        for i in _keys:
            if self.money.portfolio[i][1]+timedelta(days=2)<=self._date:
                if self._date in self.df['Date_Only'].unique():
                    date_bought = self.money.portfolio[i][1]
                    date_sold = self._date
                    temp = self.df[self.df['Symbol']==i]
                    buy_price = float(temp[temp['Date_Only']==date_bought]['Open'])
                    sell_price = float(temp[temp['Date_Only']==date_sold]['Open'])
                    change = (sell_price-buy_price)/buy_price
                    self.money.sell_from_portfolio(i, change)

    def RUN_SIM(self): #TODO this could use some serious cleanup for naming
        while self._date < self.end_date:
            if self._date in self.df['Date_Only'].unique():
                days_inputs = None
                days_inputs = self.collect_inputs()
                daily_predictions=[]
                for i in days_inputs:
                    daily_predictions.append([i[0], self.make_predictions(i[1])])
                for i in daily_predictions:
                    if i[1]:
                        self.transaction(i[0])
                self.auto_sell()
                print(self._date, self.money.total_portfolio(self._date))
                self.TEMP_TRACKER_PRICE.append(self.money.total_portfolio(self._date))
                self.TEMP_TRACKER_DATE.append(self._date)
            self._date  = self._date + timedelta(days=1)
