import pandas as pd
import numpy as np
import yfinance as yahoo

asset = str(input('instrument to deal: '))
df = pd.DataFrame(yahoo.download(asset,period="1y",interval="60m")['Adj Close'].fillna(method='ffill'))

df.columns = [i.replace('Adj Close', 'Price') for i in df.columns]
df['SMA'] = df['Price'].rolling(round(len(df)*0.03),min_periods=1).mean()
df['signal'] = np.where(df['SMA'] > df['Price'], 1.0,0.0)
df['positions'] = df['signal'].diff()
df = df.dropna()

df['capital'] = 10000.0
df['Entry'] = df.positions[df.positions>0.0] * (df['capital'] // df['Price']).fillna(method='ffill') # Quantity when strategy starts
df['Entry'] = df['Entry'].fillna(method='ffill')
df['Exit'] = 
df['nominal'] = 0.0
df['nominalValue'] = 0.0 
df['investment'] = df['capital'] + df['nominalValue']

# Libro de Ordenes
book =  
ordenes = bot['Last'] * bot['positions'] # get the moments when you enter and exit positions
precio_entrada = ordenes[ordenes>=1.0].dropna() # moments that you enter
precio_salida = ordenes[ordenes<=-1.0].dropna() # moments that you exit
book = pd.DataFrame(precio_entrada.head(len(precio_salida)), columns=['entrada']) # make an orderbook
book['salida'] = precio_salida.values * -1.0 # convert exit order into positive to make the proper profit calculus
book['resultado'] = book['salida'] - book['entrada'] # profit of operations

for i in range(len(df)):
    if  df['positions'][i] == 1.0: # buy
        df['capital'][i] -= (df['capital'][i-1] // df['Price'][i]) * df['Price'][i]
        df['nominal'][i] += df['capital'][i-1] // df['Price'][i]
    elif df['positions'][i] == 0.0: # sell
        df['capital'][i] += (df['capital'][i] // df['Price'][i]) * df['Price'][i]
        df['nominal'][i] -= df['nominal'][i-1]
    elif df['positions'][i] == 0.0: # copy same values unchanged
        df['capital'][i] = df['capital'][i-1]
        df['nominal'][i] = df['nominal'][i-1]

    df['nominalValue'][i] = df['nominalValue'][i] * df['Price'][i]
    df['investment'] = df['capital'] + df['nominalValue']    

