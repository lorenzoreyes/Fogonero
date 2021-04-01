import yfinance as yahoo
import pandas as pd 
import matplotlib.pyplot as plt

time,duration = "60d","5m"

cryptos =['ADA-USD', 'ATOM1-USD', 'BAT-USD', 'BTC-USD', 'DASH-USD', 'DCR-USD', 'DGB-USD', 'DOGE-USD', 'DOT1-USD',
          'EOS-USD', 'ETH-USD','BNB-USD','SOL1-USD','TRX-USD','ZIL-USD',
         'LINK-USD', 'LTC-USD', 'MIOTA-USD', 'NANO-USD', 'NEO-USD', 'OMG-USD','XEM-USD', 'XLM-USD', 'XRP-USD', 'ZRX-USD']



cryptos = yahoo.download(tickers=cryptos, period=time,interval=duration)['Adj Close'].fillna(method='ffill')
cryptos.columns = [i.replace('-USD','') for i in cryptos.columns]
# to work on sma
#asset = str(input('crypto to work on: '))
#asset = pd.DataFrame(cryptos[f'{asset}'].values,columns=[f'{asset}'],index=cryptos.index)
#asset['SMA'] = asset.rolling(round(len(asset)*0.03),min_periods=1).mean()
#asset.plot(figsize=(20,6),grid=True,lw=2.0)

fig = plt.figure(figsize=(20,8))
ax1 = fig.add_subplot(111)
cryptos.pct_change().cumsum().plot(ax=ax1, lw=2., legend=True)
ax1.grid()
plt.show()

#metals = ['GC=F', 'SI=F', 'PA=F', 'PL=F']

#markets = ['^DJI', '^GSPC', '^IXIC', '^RUA', '^FTSE', '^GDAXI', '^FCHI', '^N225', '^HSI']

#equities = yahoo.download(tickers="AMD T AMZN GOOGL FB TSLA DIS ADBE BABA AAPL BA BAC C CSCO CMCSA XOM JNJ INTC V MSFT NFLX NVDA MA WFC PG", period="2y", interval="60m")['Adj Close']
