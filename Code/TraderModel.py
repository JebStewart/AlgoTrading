import xgboost 
import pandas as pd
import yfinance as yf
import pickle
from datetime import datetime, timedelta, date
from StockBotLogger import Log

class ModelTools:
    def __init__(self):
        self.model_loc = r'/home/jeb/TraderBotLogs/testmodel.dat'
        self.my_model = pickle.load(open(self.model_loc, 'rb'))
        self.FE = FeatureEngineerer()
        self.L = Log()

    def get_model_inputs(self, symbol, _date):
        """ Current features --> ['Volume', 'Dividends', 'Stock Splits', 'Pct_Change', 'Three_Day_Movement', 'Five_Day_Movement']"""
        if _date.weekday() ==0:
            _date = _date - timedelta(days=2)
        tckr = yf.Ticker(symbol)
        result = pd.DataFrame(tckr.history(start=_date-timedelta(days=1), end = _date))
        if result.empty:
            print('No info for this day.')
            return pd.DataFrame()
        result = result.iloc[-1]
        running_result = pd.DataFrame(tckr.history(start=_date-timedelta(days=5), end = _date))
        running_result['Date'] = running_result.index
        running_result['Date'] = running_result['Date'].dt.date
        model_inputs = pd.DataFrame()
        model_inputs['Date'] = [_date]
        try:
            model_inputs['Volume'] = [int(result['Volume'])]
        except:
            print('NaNs in inputs')
            return pd.DataFrame()
        model_inputs['Dividends'] = [int(result['Dividends'])]
        model_inputs['Stock Splits'] = [int(result['Stock Splits'])]
        model_inputs['Pct_Change'] = [self.FE.daily_pct_change(result)]
        model_inputs['Three_Day_Movement'] =[self.FE.prior_trend(running_result, _date, 3)]
        model_inputs['Five_Day_Movement'] =[self.FE.prior_trend(running_result, _date, 5)]
        return model_inputs
    
    def make_prediction(self, symbol, _date):
        """Returns True for whether or not a stock should be bought."""
        inputs = self.get_model_inputs(symbol, _date)
        if not inputs.empty:
            inputs.drop('Date', inplace=True, axis=1)
            results = self.my_model.predict(inputs)
            if results == 1:
                return True
            else:
                return False
        self.L.add_line(f'No valid model inputs found for {symbol}', symbol)
        return False

class FeatureEngineerer:
    def __init__(self):
        pass
    
    def daily_pct_change(self, x):
        return (float(x['Close'])-float(x['Open']))/float(x['Open'])
    
    def prior_trend(self, _df, start_date, num_of_days):
        pct_changes = []
        for i in range(num_of_days):
            temp = _df[_df['Date']==start_date-timedelta(days=i)]
            if not temp.empty:
                pct_changes.append(self.daily_pct_change(temp))
        return sum(pct_changes)/num_of_days
        
if __name__ == '__main__':
    #Testing section
    mt = ModelTools()
    print(mt.get_model_inputs('TSLA', date(2020, 9, 28)))
    #print(mt.make_prediction('TSLA', date(2020, 9, 28)))
