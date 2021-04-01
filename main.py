import yfinance as yahoo
import pandas as pd
import datetime as dt
import numpy as np
import OptimizerAndRisk 

df = OptimizerAndRisk.df
portfolio = OptimizerAndRisk.portfolio

portfolioAdj = pd.DataFrame(index=portfolio.index)
portfolioAdj['SharpeRatio'] = OptimizerAndRisk.AdjustRisk(portfolio['SharpeRatio'])
portfolioAdj['SortinoRatio'] = OptimizerAndRisk.AdjustRisk(portfolio['SortinoRatio'])
portfolioAdj['SharpeUnbound'] = OptimizerAndRisk.AdjustRisk(portfolio['SharpeUnbound'])
portfolioAdj['MinVaR'] = OptimizerAndRisk.AdjustRisk(portfolio['MinVaR'])
portfolioAdj['BenchmarkEWAP'] = 1.0 / len(df.columns) # Equally-Weighted-Portfolio-Average

Series = pd.DataFrame()
Series['SortinoRatio'] =((df * portfolioAdj['SortinoRatio'].values).T.sum()).values
Series['SharpeRatio'] = ((df * portfolioAdj['SharpeRatio'].values).T.sum()).values
Series['SharpeUnbound'] = ((df * portfolioAdj['SharpeUnbound'].values).T.sum()).values
Series['MinVaR'] =      ((df * portfolioAdj['MinVaR'].values).T.sum()).values
Series['BenchmarkEWAP'] = df.T.mean().values
Series = Series.iloc[1:,:]

# SafeGuard Nans
pct = Series.pct_change()
pct = pct.iloc[1:,:] 
portfolioAdj = portfolioAdj.fillna(0)

#profitability = pd.DataFrame(Series.pct_change().sum().values,columns=['Profit'],index=Series.columns)
#profitability = profitability.sort_values('Profit',axis=0,ascending=False)

statistics_portfolios = pct.describe(percentiles=[0.01, 0.05, 0.10]).T
statistics_portfolios['mad'] = pct.mad()
statistics_portfolios['skew'] = pct.skew()
statistics_portfolios['kurtosis'] = pct.kurtosis()
statistics_portfolios['annualizedStd'] = statistics_portfolios['std'] * np.sqrt(len(Series))
statistics_portfolios['annualizedMean'] = statistics_portfolios['mean'] * len(Series)
statistics_portfolios['compensation'] = statistics_portfolios['annualizedMean'] / statistics_portfolios['annualizedStd']
statistics_portfolios = statistics_portfolios.sort_values(by='compensation',ascending=False)

# Compensation is a bare metric return / volatility (sharpe ratio in a nutshell).
# Choose the best return but also at the best risk available.

winner = str(statistics_portfolios.index[0])

#winner = str(profitability.index[0]) 
#winner

# Download the respectives Cedears with '.BA' of their yahoo tickets
# if you are working with US stocks grab last price of american

LastPrice = OptimizerAndRisk.market
if LastPrice == '2':
    BA = list(portfolioAdj.index) 
    BA = [B + '.BA' for B in BA]
    df = yahoo.download(BA,period="2d",interval="1m")['Adj Close'].fillna(method="ffill")
else:
    pass

last = pd.DataFrame(index=df.columns)
last['precio'] = df.tail(1).T.values



#if ('Yes'==str(input("Save recommendation? (Yes/No) "))):
if ("" == str(input("CALCULATIONS DONE SUCCESSFULLY. Press [Enter] to build portfolios."))):
    for i in range(int(input("how many portfolios you want? "))):
        client = input('enter the name of your client: ',)
        name = str(client) + str(' ') +str(dt.date.today()) + str('.xlsx')
        path = './excel/' + name
        best = pd.DataFrame(index=df.columns)
        best['capital'] = float(input(f"How much {client} will invest? "))
        best['price'] = df.tail(1).T.values
        best['weights'] = portfolioAdj[f'{winner}'].values 
        best['cash'] = (best['capital'] * best['weights'])
        best['nominal'] =  best['cash'] // best['price'] 
        best['invested'] = best['price'] * best['nominal']
        best['percentage'] = best['invested'] / sum(best['invested'])
        best['total'] = sum(best['invested'])
        best['liquid'] = best['capital'] - best['total']
        best = best[best.weights!=0].dropna() # remove all stocks that you do not invest in
        #best.to_csv(path)
        writer = pd.ExcelWriter(path, engine='xlsxwriter')
        best.to_excel(writer,sheet_name=f'{winner}')
        portfolioAdj.to_excel(writer, sheet_name='portfolioWeights')
        statistics_portfolios.to_excel(writer, sheet_name='descriptiveStatistics')   
        writer.save()

