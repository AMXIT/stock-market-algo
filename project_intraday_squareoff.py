# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 12:37:55 2022

@author: Amritansh S
"""

#imported every thing
import pandas as pd
from datetime import datetime
import requests
import numpy as np
from smartapi import SmartConnect
import smartapi.smartExceptions
import time 
import sys
import pyotp


# TELEGRAM
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
def telegram(message):
    bot_token = '?'
    bot_chatID = '?'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '*&parse_mode=Markdownv2&text=' + message
    
    response = requests.get(send_text)
    
    return response.json()



print("imported everything")
telegram("squareoff code")
#create object of call
API_KEY = '?'
obj=SmartConnect(api_key=API_KEY)


#username_password
USER_NAME = '?'
PWD = '?'
TOTP_COUPON='?'
TOTP = pyotp.TOTP(TOTP_COUPON)
TOTP=TOTP.now()
#login api call
data = obj.generateSession(USER_NAME,PWD,TOTP)
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)

#print(userProfile)
print("logged in successfully")

#geting data from website to table formate in code
def intializeSymbolTokenMap():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    global token_df
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry'])
    token_df = token_df.astype({'strike': float})
intializeSymbolTokenMap()   
#print(token_df)

print("importing tokens")
#get token after passing info
def getTokenInfo (df,exch_seg, instrumenttype,symbol,strike_price,pe_ce):
    strike_price = strike_price*100
    if exch_seg == 'NSE':
        eq_df = df[(df['exch_seg'] == 'NSE') & (df['symbol'].str.contains('EQ')) ]
        return eq_df[eq_df['name'] == symbol]
    elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
    elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
        return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

#getting open position data intraday
        
for i in obj.position()['data']:
    if i['producttype']=="INTRADAY":
 
        print(i['symboltoken'],i['tradingsymbol'],i['exchange'])
  
        print(i['netqty'])
        telegram("{} {}".format(i['tradingsymbol'],i['netqty']))
        
        A=str(abs(int(i['netqty'])))
        
        #if Qty +ve place sell order
        
        if int(i['netqty'])>0:
            print("selling")
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": i['tradingsymbol'],
                "symboltoken": i['symboltoken'],
                "transactiontype": "SELL",
                "exchange": i['exchange'],
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": "350",
                "squareoff": "351",
                "stoploss": "355",
                "quantity": A,
                "triggerprice": "365"
            }
            a=obj.placeOrder(orderparams)
            print(a)
        
        
         #if Qty -ve place buy order
         
        elif int(i['netqty'])<0:
            print("buying")
            orderparams = {
                "variety": "NORMAL",
                "tradingsymbol": i['tradingsymbol'],
                "symboltoken": i['symboltoken'],
                "transactiontype": "BUY",
                "exchange": i['exchange'],
                "ordertype": "MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": "350",
                "squareoff": "351",
                "stoploss": "355",
                "quantity": A,
                "triggerprice": "365"
            }
            a=obj.placeOrder(orderparams)
            print(a)
            
            
#cancelling open orders intraday

for x in range(len(obj.orderBook()['data'])):
    time.sleep(1)
    if obj.orderBook()['data'][x]['producttype']=='INTRADAY':
        time.sleep(1)
        print(obj.orderBook()['data'][x]['tradingsymbol'])
        time.sleep(1)
        obj.cancelOrder(obj.orderBook()['data'][i]['orderid'],'STOPLOSS')

telegram("done")
