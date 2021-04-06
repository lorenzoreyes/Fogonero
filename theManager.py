# We want to iterate excels saved & perform task
# designed in TrackUpdate.py Grab an input int 
# of excel to perform task (monitor, update, withdraw, etc)
# from the command line.

import pandas as pd, numpy as np, glob
import yfinance as yahoo, datetime as dt
import trackCLI as tracker
import os

file = []
clientDict = {}
# want to generate a dictionary key:val ID:name to pick file

for filename in glob.iglob('excel/*'):
  file.append(filename)
  clientDict = dict(map(reversed, enumerate(file)))  
  clientDict = dict((v,k) for k,v in clientDict.items())

clientDict = pd.DataFrame(clientDict.items(), columns=['IDs','Excels'])
print(clientDict)

request = int(input("Type the ID of your Client: "))


data = pd.read_excel(clientDict['Excels'][request])

print(f"What task do you want to do to {clientDict.Excels[request]} ?:\n(1) Monitor Portfolio? To watch performance.\n(2) Do a Deposit or Withdraw? Specify the ammount of capital to change.\n(3) Update risk? By adding new information.\nOptional (4) BackToBasics save task.\n")
action = int(input("Type your Task: ..."))
if action == 1:
  data = tracker.PortfolioMonitor(data)
elif action == 2:
  data = tracker.DepositOrWithdraw(data)
elif action == 3:
  data = tracker.portfolioRiskUpdated(data)


print(data)

if ('Yes'==str(input("Save recommendation? (Yes/No) "))):
  client = input(f'Keep same name of your {clientDict.Excels[request]}: ',)
  name = str(client) + str(' ') + str(dt.date.today()) + str('.csv')
  path = './excel/' + name
  data.to_csv(f'{path}')
# listaExcels = pd.DataFrame(clientDict.items(),columns=['clientID','Excels'])
# listaExcels.to_csv('listadoExcels.csv')
