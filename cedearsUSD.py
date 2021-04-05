import pandas as pd, yfinance as yahoo
import matplotlib.pyplot as plt

time, duration = "1y", "60m"

test = pd.read_excel('./excel/Cedears ETF 100k 2021-04-03.xlsx')
test = test[test.nominal!=0] # take-out stocks that you do not invest in

lista = list(test['Unnamed: 0'].values)
listb = [i.replace('.BA','') for i in lista]

data = yahoo.download(listb,period=time,interval=duration)["Adj Close"].fillna(method="ffill")
cartera = (data * test.nominal.values).T.sum()
cartera.plot(figsize=(20,6),grid=True,lw=2.0)

stocks = ['AAPL.BA', 'BBD.BA', 'MELI.BA', 'KO.BA', 'INTC.BA', 'VALE.BA',
       'TSLA.BA', 'WFC.BA', 'XOM.BA', 'AMZN.BA', 'BABA.BA', 'T.BA', 'MSFT.BA',
       'GE.BA', 'WMT.BA', 'HMY.BA', 'PFE.BA', 'ERJ.BA', 'AUY.BA', 'X.BA']

ratios = [10,144,1,9,1,1,1,1,5,5,60,10,2,3,15,2,5,6,3,5]

cedears = yahoo.download(stocks, period=time, interval=duration)['Adj Close'].fillna(method='ffill')

cedears = cedears * ratios  # get stocks prices according to what you have to paid

topba = [s.replace('.BA', 'BA') for s in stocks]

cedears.columns = topba

forex = [i.replace('.BA','') for i in stocks]

df = yahoo.download(forex,period=time, interval=duration)['Adj Close'].fillna(method='ffill')
df = df.tail(len(cedears))

tc = cedears.div(df.values)
tc.columns = topba
mediaced = pd.DataFrame(index=tc.index)
mediaced['CableCedears'] = tc.T.median()

cartera = cartera.tail(len(mediaced))

# Global dataframe
performance = pd.DataFrame(cartera.values,columns=['ETFinUSD'],index=cartera.index)
performance['MEPExchange'] = mediaced['CableCedears'].values
performance['ETFCedear'] = performance['ETFinUSD'].values * performance['MEPExchange'].values
#performance.pct_change().cumsum().plot(figsize=(20,6),grid=True)


# actual ETF in Pesos
etf = yahoo.download(lista,period="1y",interval="60m")["Adj Close"].fillna(method="ffill")
etf = (etf * test.nominal.values).T.sum()

figb = plt.figure(figsize=(20,8))
ax1 = figb.add_subplot(111)
etf.pct_change().cumsum().plot(ax=ax1, lw=3)
ax1.grid()
ax1.set_title('Cedears ETF in Pesos')
plt.show()




fig = plt.figure(figsize=(20,8))
ax1 = fig.add_subplot(111, ylabel='USD-CEDEARS-MEP')
performance.pct_change().cumsum().plot(ax=ax1, lw=3)
ax1.grid()
ax1.set_title('SP500, MEP-Rate & CEDEARs')
plt.show()


# Pie-Chart of Weights
labels = list(test['Unnamed: 0'].values)
sizes = (test.percentage.values)
fig3, ax3 = plt.subplots(figsize=(5,5))
ax3.pie(sizes, labels=labels,autopct='%1.1f%%',
       shadow=True, startangle=90)
ax3.axis('equal')

plt.show()