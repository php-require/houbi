import time
start_time = time.time()
from huobi.client.market import MarketClient
from huobi.constant import *
from huobi.utils import *
from huobi.client.generic import GenericClient
import pandas as pd
import numpy as np
market_client = MarketClient(init_log=True)
interval = CandlestickInterval.MIN5
interval_4h = CandlestickInterval.HOUR4
interval_1h = CandlestickInterval.MIN60
from statsmodels.tsa.stattools import adfuller

# base = ['btcusdt', 'ethusdt','bchusdt','xrpusdt','eosusdt','ltcusdt','trxusdt']   

# couple currency
LogInfo.output("---- Supported currency ----")
generic_client = GenericClient()
list_obj = generic_client.get_exchange_currencies()
base = []
for currency in list_obj:
   base.append(currency + 'usdt')
 
base.pop(0)
arr = base[:10]
print(arr)
 

# convert candlestick
def huobi_to_pandas(candlestick):
  data = {
    'timestamp': candlestick.id,
    'open': candlestick.open,
    'high': candlestick.high,
    'low': candlestick.low,
    'close': candlestick.close,
    'volume': candlestick.vol,
   # 'amount': candlestick.amount
  }
  return pd.Series(data) 


#f1
def klines4h(symbol):
 
  try:
    list_obj = market_client.get_candlestick(symbol, interval_4h, 180)
  except BaseException:
      list_obj = False
  finally:
      if list_obj:
        df = pd.DataFrame([huobi_to_pandas(elem) for elem in list_obj])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit = 's')
        df.drop(columns = ['Open', 'High', 'Low', 'Volume'], axis = 1, inplace=True)
        df = df.astype(float)
        return df

#f2
def klines1h(symbol):
  try:
    list_obj = market_client.get_candlestick(symbol, interval_1h, 720)
  except BaseException:
      list_obj = False
  finally:
      if list_obj:
        df = pd.DataFrame([huobi_to_pandas(elem) for elem in list_obj])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = df.set_index('Time')
        df.index = pd.to_datetime(df.index, unit = 's')
        df.drop(columns = ['Open', 'High', 'Low', 'Volume'], axis = 1, inplace=True)
        df = df.astype(float)
        return df


   
res = []
for i in arr:
  for j in arr[arr.index(i)+1:]:
    print(j)
    try:
      spreadcheck = adfuller((klines4h(i)['Close']/klines4h(j)['Close']).dropna(), autolag='AIC')
    except BaseException:
      spreadcheck = False
    finally:  
      if spreadcheck:
      
        if spreadcheck[1] < 0.001:
            res.append([i, j, spreadcheck[0], spreadcheck[1]])

def PValue(inputList):
        return inputList[3]
res = sorted(res, key=PValue)
print(res)
ans = []
for i in res:
  if adfuller((klines1h(i[0])['Close']/klines1h(i[1])['Close']), autolag='AIC')[1] < 0.001:
    ans.append(i)
ans    
print("--- %s seconds ---" % (time.time() - start_time))