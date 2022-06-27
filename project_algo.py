# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:34:03 2022

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

#SENDING TELEGRAM MESSAGE USING BOT
    
telegram("imported everything")

#create object of call
API_KEY = '?'
obj=SmartConnect(api_key=API_KEY)


#username_password

USER_NAME = '?'
PWD = '?'

#login api call
data = obj.generateSession(USER_NAME,PWD)
refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)


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


# entery when right time
        
    
while(True):
    now = datetime.now()
    
    current_time = now.strftime("%H:%M:%S")
    
    start = '09:18:20'
    
    end = '23:59:40'
    
    
    if current_time > start and current_time < end:
        
        
        print('in')
        telegram("in time")
        
        print(current_time)

        print("finding spot banknifty price")
        
        
        #getting ltp of banknify 
        
        sym='BANKNIFTY'
        
        tok='26009'
        ltpfinder=obj.ltpData('NSE',sym,tok)


        dataa=ltpfinder['data']
        print(ltpfinder)
        ltp_spot=(int(dataa['ltp']/100)*100)
        print(ltp_spot)
    

        print("found ltp spot price")
        
        
        #atm call and put
        i=0
        ce=ltp_spot-100
        
        pe=ltp_spot+100
    
        #getting tokeno and other info of the ce of that ltp one thing
        
        tokeninfce=getTokenInfo (token_df,'NFO','OPTIDX','BANKNIFTY',ce,'CE').iloc[i]
        
        celtp_data=obj.ltpData('NFO',tokeninfce['symbol'],tokeninfce['token'])
        
        celtp=celtp_data['data']
        
        while True:
            global c
            try:
                print(i)
                tokeninfce=getTokenInfo (token_df,'NFO','OPTIDX','BANKNIFTY',ce,'CE').iloc[i]
                celtp_data=obj.ltpData('NFO',tokeninfce['symbol'],tokeninfce['token'])
        
                celtp=celtp_data['data']
        
                ce_ltp=celtp['ltp']
                c=i
                break
            except:
                i+=1
                print(i)
                continue
                
        #getting ltp of the ce
        
    
        celtp_data=obj.ltpData('NFO',tokeninfce['symbol'],tokeninfce['token'])
        
        celtp=celtp_data['data']
        
        ce_ltp=celtp['ltp']
        print(ce_ltp)  
        
        print("atm call ltp found")
        
        tokeninfpe=getTokenInfo (token_df,'NFO','OPTIDX','BANKNIFTY',pe,'PE').iloc[i]
        peltp_data=obj.ltpData('NFO',tokeninfpe['symbol'],tokeninfpe['token'])
        
        peltp=peltp_data['data']
        
        while True:
            global p
            try:
                print(i)
                tokeninfpe=getTokenInfo (token_df,'NFO','OPTIDX','BANKNIFTY',pe,'PE').iloc[i]
                peltp_data=obj.ltpData('NFO',tokeninfpe['symbol'],tokeninfpe['token'])
        
                peltp=peltp_data['data']
        
                pe_ltp=peltp['ltp']
                p=i
                break
            except:
                i+=1
                print(i)
                continue
  
    
        peltp_data=obj.ltpData('NFO',tokeninfpe['symbol'],tokeninfpe['token'])
        
        peltp=peltp_data['data']
        
        pe_ltp=peltp['ltp']
            
        
        print("atm put ltp found")
       
        
        # finding strike ce
        
        while(ce_ltp>135):
            
            
            ce+=100
            
            #print(ce_ltp)
            #print(ce)
            
            tokeninfce=getTokenInfo (token_df,'NFO','OPTIDX','BANKNIFTY',ce,'CE').iloc[c]
            
            celtp_data=obj.ltpData('NFO',tokeninfce['symbol'],tokeninfce['token'])
            celtp=celtp_data['data']
            ce_ltp=celtp['ltp']
        
            
            
            #getting ltp of the ce
            
            
        #sl price set
        
        ce_sl=(ce_ltp/10)*2.5+ce_ltp
        ce_sl=round(ce_sl, 1)
        print(ce_ltp)
        telegram("ce found")
 
        
        print(datetime.now())    
        print("found call to short")   
        
        
        # finding strike pe   
        
        while(pe_ltp>135):
            
            
            pe-=100
            
            #print(pe_ltp)
            #print(pe)
            
            tokeninfpe=getTokenInfo (token_df,'NFO','OPTIDX','BANKNIFTY',pe,'PE').iloc[p]
            
            peltp_data=obj.ltpData('NFO',tokeninfpe['symbol'],tokeninfpe['token'])
            peltp=peltp_data['data']
            pe_ltp=peltp['ltp']
        
            
            
            #getting ltp of the ce
            
        # sl price for pe
        
        pe_sl=(pe_ltp/10)*2.5+pe_ltp
        pe_sl=round(pe_sl, 1)
        print(pe_ltp)
        print("found put to short") 
        telegram("pe found")
       
        #placing order ce
        
        print(datetime.now())
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol":tokeninfce['symbol'] ,
            "symboltoken": tokeninfce['token'],
            "transactiontype": "SELL",
            "exchange": "NFO",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": "0",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": "25"
        }
        ce_orderid = obj.placeOrder(orderparams)


        print("shorted call")
        telegram("ce shorted")

       

        #placing order pe

        print(datetime.now())
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol":tokeninfpe['symbol'] ,
            "symboltoken": tokeninfpe['token'],
            "transactiontype": "SELL",
            "exchange": "NFO",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": "0",
            "squareoff": "0",
            "stoploss": "0",
            "quantity": "25"
        }
        pe_orderid = obj.placeOrder(orderparams)
        

        print("shorted put")
        telegram("pe shorted")
        
        #placing order ce stoploss
        orderparams = {
                "variety": "STOPLOSS",
                "tradingsymbol":tokeninfce['symbol'] ,
                "symboltoken": tokeninfce['token'],
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "STOPLOSS_MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": ce_sl,
                "squareoff": "0",
                "stoploss": "0",
                "quantity": "25",
                "triggerprice": ce_sl
        }
        ce_sl_orderid = obj.placeOrder(orderparams)
        
        
        print("call sl placed")
        telegram("call sl placed")

       

        #placing order pe stoploss
        

        orderparams = {
                "variety": "STOPLOSS",
                "tradingsymbol":tokeninfpe['symbol'] ,
                "symboltoken": tokeninfpe['token'],
                "transactiontype": "BUY",
                "exchange": "NFO",
                "ordertype": "STOPLOSS_MARKET",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": pe_sl,
                "squareoff": "0",
                "stoploss": "0",
                "quantity": "25",
                "triggerprice": pe_sl
        }
        pe_sl_orderid = obj.placeOrder(orderparams)
        
        print("put sl placed")
        telegram("pe sl placed")
        
    
        
        #modying sl to correct sl (slippages)
        time.sleep(20)
        
        order_book=obj.orderBook()
        

        
        len_of_orderbook=len(order_book['data'])

        for i in range(len_of_orderbook):
            if order_book['data'][i]['orderid']==ce_orderid:
                
                print(order_book['data'][i]['averageprice'])
                ce_ltp=order_book['data'][i]['averageprice']
                ce_sl=(ce_ltp/10)*2.5+ce_ltp
                ce_sl=round(ce_sl, 1)
                
            else:
                continue

        for i in range(len_of_orderbook):
            if order_book['data'][i]['orderid']==pe_orderid:
                
                print(order_book['data'][i]['averageprice'])
                pe_ltp=order_book['data'][i]['averageprice']
                pe_sl=(pe_ltp/10)*2.5+pe_ltp
                pe_sl=round(pe_sl, 1)
                
            else:
                continue

        orderparams = {
                
                "variety":"STOPLOSS",
                "ordertype":"STOPLOSS_MARKET",
                "orderid": pe_sl_orderid,
                "producttype":"INTRADAY",
                "transactiontype": "BUY",
                "duration":"DAY",
                "price":"160",
                "quantity":"25",
                "tradingsymbol":tokeninfpe['symbol'],
                "symboltoken":tokeninfpe['token'],
                "exchange":"NFO",
                "triggerprice":pe_sl
        }
        obj.modifyOrder(orderparams)
        

        orderparams = {
                
                "variety":"STOPLOSS",
                "ordertype":"STOPLOSS_MARKET",
                "orderid": ce_sl_orderid,
                "producttype":"INTRADAY",
                "transactiontype": "BUY",
                "duration":"DAY",
                "price":"160",
                "quantity":"25",
                "tradingsymbol":tokeninfce['symbol'],
                "symboltoken":tokeninfce['token'],
                "exchange":"NFO",
                "triggerprice":ce_sl
        }
        obj.modifyOrder(orderparams)
            
                
       
        print(" All Done!!")

        print(datetime.now())
        print (ce_sl_orderid)
        
        bkup_ce_ltp=ce_ltp

        bkup_pe_ltp=pe_ltp
        
        print("started sl system")
        
        # sl modification code
        while True:
            now = datetime.now()
            telegram("high broken")
            
            current_time = now.strftime("%H:%M:%S")
            
            order_book=obj.orderBook()
            
            len_of_orderbook=len(order_book['data'])
            
            
            i=0
            
            print("found len and i=0")
            
            #finding sl order
            
            while i<len_of_orderbook:
                global sl_pe
                global sl_ce
                print("in loop to find order id")
                time.sleep(2)
                if order_book['data'][i]['orderid']==pe_sl_orderid:
                    sl_pe=order_book['data'][i]['status']
                    i+=1
                    print("found one order")
                elif order_book['data'][i]['orderid']==ce_sl_orderid:
                    sl_ce=order_book['data'][i]['status']
                    i+=1
                    print("found second order")
                else:
                    i+=1
                    print("not this one")


            #if pe sl hit modify ce sl to cost
            
            if sl_pe=="complete":
                orderparams = {
                    "variety":"STOPLOSS",
                    "orderid": ce_sl_orderid,
                    "ordertype":"STOPLOSS_MARKET",
                    "producttype":"INTRADAY",
                    "duration":"DAY",
                    "price":"160",
                    "quantity":"25",
                    "tradingsymbol":tokeninfce['symbol'],
                    "symboltoken":tokeninfce['token'],
                    "exchange":"NFO",
                    "triggerprice": bkup_ce_ltp
                }
                obj.modifyOrder(orderparams)
                print("pe sl hit and modified")
                telegram("pe sl hit and modified")
                sys.exit()
                
            #if ce sl hit modify pe sl to cost
            
            elif sl_ce=='complete':
                orderparams = {
                    "variety":"STOPLOSS",
                    "orderid": pe_sl_orderid,
                    "ordertype":"STOPLOSS_MARKET",
                    "producttype":"INTRADAY",
                    "duration":"DAY",
                    "price":"160",
                    "quantity":"25",
                    "tradingsymbol":tokeninfpe['symbol'],
                    "symboltoken":tokeninfpe['token'],
                    "exchange":"NFO",
                    "triggerprice":bkup_pe_ltp 
                }
                obj.modifyOrder(orderparams)
                telegram("ce sl hit and modified")
                print("ce sl hit and modified")
                sys.exit()
                
            
            #if time greater than 3:13:30 all the positions will exit
            
            elif current_time > '15:13:30':
                print("exit all positions")
                obj.cancelOrder(pe_sl_orderid,'STOPLOSS')
                obj.cancelOrder(ce_sl_orderid,'STOPLOSS')
                orderparams = {
                        "variety": "NORMAL",
                        "tradingsymbol":tokeninfpe['symbol'] ,
                        "symboltoken": tokeninfpe['token'],
                        "transactiontype": "BUY",
                        "exchange": "NFO",
                        "ordertype": "MARKET",
                        "producttype": "INTRADAY",
                        "duration": "DAY",
                        "price": "0",
                        "squareoff": "0",
                        "stoploss": "0",
                        "quantity": "25"
                }
                obj.placeOrder(orderparams)
                orderparams = {
                        "variety": "NORMAL",
                        "tradingsymbol":tokeninfce['symbol'] ,
                        "symboltoken": tokeninfce['token'],
                        "transactiontype": "BUY",
                        "exchange": "NFO",
                        "ordertype": "MARKET",
                        "producttype": "INTRADAY",
                        "duration": "DAY",
                        "price": "0",
                        "squareoff": "0",
                        "stoploss": "0",
                        "quantity": "25"
                }
                obj.placeOrder(orderparams)
                telegram("exit time")
                
                
                
               
                sys.exit()
            else:
                if sl_pe=='rejected':
                    
                    print("rejected")
                    telegram("rejected")
                    sys.exit()

                time.sleep(15)
                print("no sl hit")
      
        
    
       
        
    else:
        print("not in time")
        time.sleep(10)
        continue    
