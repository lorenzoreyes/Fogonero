import yahoo_fin.stock_info as yf
import yfinance as yahoo 
import pandas as pd
import ftplib
import io
import re
import datetime
from pytickersymbols import PyTickerSymbols #https://pypi.org/project/pytickersymbols/


# functions to get info about each market and their current stock tickets
# markets to operate: USA (Nasdaq & SP500), England, China, Japan, Canada, Brazil, Australia
# the handlers will result with only list containing respective tickets

def tickers_nasdaq():

    '''Downloads list of tickers currently listed in the NASDAQ'''

    ftp = ftplib.FTP("ftp.nasdaqtrader.com")
    ftp.login()
    ftp.cwd("SymbolDirectory")

    r = io.BytesIO()
    ftp.retrbinary('RETR nasdaqlisted.txt', r.write)

    info = r.getvalue().decode()
    splits = info.split("|")

    tickers = [x for x in splits if "N\r\n" in x]
    tickers = [x.strip("N\r\n") for x in tickers if 'File' not in x]

    tickers = sorted(list(set(tickers)))

    ftp.close()    

    return tickers

def sp500():
    USA = pd.read_html("https://topforeignstocks.com/indices/components-of-the-sp-500-index/")[0]
    USA = list(USA.Ticker.values)
    return USA

def top50liquid():
    USD = pd.read_excel("tickersBA.xlsx")
    USD = list(USD['Ticker'].values)
    USD = [U + '.BA' for U in USD]
    volume = yahoo.download(USD,period="80d")['Volume'].fillna(method='ffill')
    votal = pd.DataFrame(index=volume.index)
    votal['totav'] = volume.T.sum()
    percentage = volume.div(votal['totav'], axis=0)
    ordered = pd.DataFrame(percentage.sum().T,columns=['percentage'],index=percentage.columns)
    ordered = ordered / ordered.sum() # ensure you round to 100%
    orderedalph = ordered.sort_values('percentage',axis=0,ascending=False)    
    liquid = orderedalph.cumsum()    
    lista = list(liquid.head(50).index)
    lista = [i.replace('.BA','') for i in lista] 
    return lista

def nikkei_tickets():
    nikkei = pd.read_html("https://topforeignstocks.com/indices/the-components-of-the-nikkei-225-index/")[0]
    nikkei['tickets'] = [t + '.T' for t in nikkei.Code.astype(str)]
    nikkei = list(nikkei.tickets.values)
    return nikkei

def shanghai_tickets():
    shanghai = pd.read_html("https://topforeignstocks.com/indices/components-of-the-shanghai-composite-index/")[0]
    shanghai['tickets'] = [ss + '.SS' for ss in shanghai['Company Code'].astype(str)]
    shanghai = list(shanghai.tickets.values)
    return shanghai 

def bovespa_tickets():
    bovespa = pd.read_html("https://topforeignstocks.com/indices/components-of-the-bovespa-index/")[0]
    bovespa = list(bovespa.Ticker.values)
    return bovespa

def canada_tickets():
    canada = pd.read_html("https://topforeignstocks.com/indices/the-components-of-the-sptsx-composite-index/")[0]
    canada = list(canada.Ticker.values)
    return canada

def england_tickets():
    england = pd.read_html("https://topforeignstocks.com/indices/components-of-the-ftse-100-index/")[0]
    england = list(england.Ticker.values)
    return england

def australia_tickets():
    australia = pd.read_html("https://topforeignstocks.com/indices/components-of-the-s-p-asx-all-australian-200-index/")[0]
    aussie = list(australia['Ticker'].values)
    return aussie
