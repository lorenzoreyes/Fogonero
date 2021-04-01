import yfinance as yahoo
import pandas as pd
import numpy as np
import scipy.optimize as sco
from scipy import stats
import scrappy 

print("Type the market to operate:\n(1) SP500,\n(2) CEDEARs,\n(3) FTSE,\n(4) Nikkei225,\n(5) SHANGHAI,\n(6) AUSTRALIA,\n(7) CANADA,\n(8) BOVESPA")
market = str(input("Which market do you wish to operate?... "))
if market == '1':
    lista = scrappy.sp500()
    freeRisk = '^GSPC'
elif market == '2':
    lista = scrappy.top50liquid()
    freeRisk = "^GSPC"
elif market == '3':
    lista = scrappy.england_tickets()
    freeRisk = '^FTSE'
elif market == '4': 
    lista = scrappy.nikkei_tickets()
    freeRisk = '^N225'
elif market =='5':
    lista = scrappy.shanghai_tickets()
    riskfree = "000001.SS"
elif market == '6':
    lista = scrappy.australia_tickets()
    freeRisk = '^AXJO'
elif market == '7':
    lista = scrappy.canada_tickets()
    freeRisk = '^GSPTSE'
elif market == '8':
    lista = scrappy.bovespa_tickets()
    freeRisk = '^BVSP'

def top50(lista):
    lista = lista
    df = yahoo.download(lista,period="1y")["Adj Close"].fillna(method="ffill")
    #df = df.dropna(axis=1) # remove recently added stocks to avoid nans
    pct = df.pct_change()#.dropna()df = df.dropna(axis=1) # remove recently added stocks to avoid nans #(how='all')
    mean = pd.DataFrame(pct.mean(),columns=['Mean'],index=pct.columns)
    riskpct = mean.mean()
    mean_rf = mean - riskpct.mean()
    std = pd.DataFrame(pct.std(),columns=['Std'],index=pct.columns)
    sharpe_ratio = pd.DataFrame(mean_rf['Mean']/(std['Std']), columns=['SharpeRatio'],index=pct.columns)
    orderedsharpe = sharpe_ratio.sort_values('SharpeRatio', axis=0, ascending=False)
    lista = list(orderedsharpe.head(50).index.values)
    return lista

if market != '2':
    lista = top50(lista)
# As an alternative of market index you can use df.T.mean() as a EWAP Equally Weighted Average Portfolio

df = yahoo.download(lista,period="1y",interval="60m")["Adj Close"].fillna(method="ffill")
#df = df.dropna(axis=1) # remove recently added stocks due nans values axis=1
riskfree = yahoo.download(f"{freeRisk}", period="1y",interval="60m")['Adj Close'].fillna(method='ffill')
pct = df.pct_change().dropna() #(how='all')
riskpct = riskfree.pct_change().dropna()
mean = pd.DataFrame(pct.mean(),columns=['Mean'],index=pct.columns)
mean_rf = mean - riskpct.mean()
std = pd.DataFrame(pct.std(),columns=['Std'],index=pct.columns)
numerator = pct.sub(riskpct,axis=0)
downside_risk = ((numerator[numerator<0].fillna(0))**2).mean()
noa = len(df.columns)
weigths = np.random.random(noa)
weigths /= np.sum(weigths)
observations = len(df.index)
mean_returns = df.pct_change().mean()
cov = df.pct_change().cov()
alpha = 0.1
rf = riskpct.mean()
num_portfolios = 1000

Upbound = 0.075

# Sharpe Unbound
sharpe = pd.DataFrame(mean_rf['Mean']/(std['Std']), columns=['SharpeRatio'],index=pct.columns)
sharpe = sharpe.sort_values('SharpeRatio', axis=0, ascending=False)
sharpe[sharpe.SharpeRatio<0.0] = 0.0
#sharpe = sharpe[sharpe.head(25)>0].fillna(0)
sharpe = sharpe / sharpe.sum()
sharpe[sharpe.SharpeRatio>=Upbound] = Upbound
sharpe = sharpe / sharpe.sum()
sharpe = sharpe.sort_values('SharpeRatio',axis=0,ascending=False)
sharpe = sharpe.sort_index(axis=0,ascending=True)

# Sortino Ratio
sortino_ratio = pd.DataFrame(mean_rf['Mean'].to_numpy()/downside_risk**(1/2),columns=['SortinoRatio'])
sortino_ratio = sortino_ratio.sort_values('SortinoRatio',axis=0,ascending=False)
sortino_ratio[sortino_ratio.SortinoRatio<0.0] = 0.0
#sortino_ratio = sortino_ratio[sortino_ratio.head(25)>0].fillna(0)
sortino_ratio = sortino_ratio / sortino_ratio.sum()
sortino_ratio = sortino_ratio.sort_index(axis=0,ascending=True)
sortino_ratio[sortino_ratio.SortinoRatio>=Upbound] = Upbound
sortino_ratio = sortino_ratio / sortino_ratio.sum()
sortino_ratio = sortino_ratio.sort_values('SortinoRatio',axis=0,ascending=False)
sortino_ratio = sortino_ratio.sort_index(axis=0,ascending=True)



def calc_neg_sharpe(weights, mean_returns, cov, rf):
    portfolio_return = np.sum(mean_returns * weights) * observations
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov, weights))) * np.sqrt(observations)
    sharpe_ratio = (portfolio_return - rf) / portfolio_std
    return -sharpe_ratio

constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

def max_sharpe_ratio(mean_returns, cov, rf):
    num_assets = len(mean_returns)
    args = (mean_returns, cov, rf)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,Upbound)
    bounds = tuple(bound for asset in range(num_assets))
    result = sco.minimize(calc_neg_sharpe, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result

optimal_port_sharpe = max_sharpe_ratio(mean_returns, cov, rf)

optimo = pd.DataFrame(index=df.columns)
optimo['weights'] = optimal_sharpe = pd.DataFrame([round(x,4) for x in optimal_port_sharpe['x']],index=df.columns)

def calc_portfolio_VaR(weights, mean_returns, cov, alpha, observations):
    portfolio_return = np.sum(mean_returns * weights) * observations
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov, weights))) * np.sqrt(observations)
    portfolio_var = abs(portfolio_return - (portfolio_std * stats.norm.ppf(1 - alpha)))
    return portfolio_var

def min_VaR(mean_returns, cov, alpha, observations):
    num_assets = len(mean_returns)
    args = (mean_returns, cov, alpha, observations)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bound = (0.0,Upbound)
    bounds = tuple(bound for asset in range(num_assets))
    result = sco.minimize(calc_portfolio_VaR, num_assets*[1./num_assets,], args=args,
                        method='SLSQP', bounds=bounds, constraints=constraints)
    return result

min_port_VaR = min_VaR(mean_returns, cov, alpha, observations)

minimal_VaR = pd.DataFrame(index=df.columns)
minimal_VaR['weights'] = pd.DataFrame([round(x,4) for x in min_port_VaR['x']],index=df.columns)



portfolio = pd.DataFrame(index=df.columns)
portfolio['SharpeRatio'] = pd.DataFrame([round(x,4) for x in optimal_port_sharpe['x']],index=df.columns)
portfolio['MinVaR'] = pd.DataFrame([round(x,4) for x in min_port_VaR['x']],index=df.columns)
portfolio['SortinoRatio'] = sortino_ratio['SortinoRatio'].values
portfolio['SharpeUnbound'] = sharpe['SharpeRatio'].values
# Nota: Agregar simulador de portfolios de VaR

def AdjustRisk(portfolio):
  """Provide the stock list of your portfolio
     to update risk by Component-Value-at-Risk"""
  data = df 
  returns = data.pct_change()
  correlation = returns.corr() # correlation
  covariance = returns.cov()  # covariance
  instruments = pd.DataFrame(index= data.columns)
  #sample = np.random.random_sample(size=(len(data.columns),1)) 
  #sample /= np.sum(sample)
  #instruments['weigths'] = sample # secure allocation is equal 1
  instruments['weigths'] = 1/len(instruments.index) # secure equal allocation 
  instruments['deltas'] = (instruments.weigths * correlation).sum() # deltas as elasticity of the assets
  instruments['Stdev'] = returns.std()
  instruments['stress'] = (instruments.deltas * instruments.Stdev) * 3 # stress applied at 4 deviations
  instruments['portfolio_stress'] = instruments.stress.sum() # the stress of the portfolio
  risk = pd.DataFrame(index=data.columns)
  risk['numerator'] = (instruments.deltas.multiply(covariance)).sum()
  risk['denominator'] = data.pct_change().std() * (-2.365)
  risk['GradVaR'] = -risk.numerator / risk.denominator
  risk['CVaRj'] = risk.GradVaR * instruments.deltas # Component VaR of the Risk Factors j
  risk['thetai'] = (risk.CVaRj * correlation).sum() # Theta i of the instruments
  risk['CVaRi'] = risk.thetai * (1/len(data.columns)) # Component VaR of the Instruments i
  risk['totalCVaRi'] = risk.CVaRi.sum() #total CVaR of the portfolio
  risk['CVaRattribution'] = risk.CVaRi / risk.totalCVaRi # risk allocation by instrument in the portfolio
  riskadj = pd.DataFrame(index=data.columns)
  riskadj['base'] = instruments['weigths'].values
  riskadj['CVaRattribution'] = risk.CVaRattribution.sort_values(axis=0,ascending=False)
  riskadj['new'] = portfolio.values  # Choosing the option with the highest return
  riskadj['condition'] = (riskadj.base / riskadj.CVaRattribution)
  riskadj['newrisk'] = (riskadj.new / riskadj.CVaRattribution)
  riskadj['differences'] = (riskadj.newrisk - riskadj.condition)  # apply this result as a percentage to multiply new weights
  riskadj['adjustments'] = (riskadj.newrisk - riskadj.condition) / riskadj.condition #ALARM if its negative sum up the difference, 
                                              #if it is positive rest it, you need to have 0
  riskadj['suggested'] = riskadj.new * (1 + riskadj.adjustments)   
  riskadj['tototal'] = riskadj.suggested.sum()
  riskadj['MinCVaR'] = riskadj.suggested / riskadj.tototal
  return riskadj['MinCVaR']
