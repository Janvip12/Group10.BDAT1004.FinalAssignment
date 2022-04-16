# basic Flask application
import requests
import time
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import json
from datetime import datetime, timedelta
from collections import OrderedDict

app = Flask(__name__)

client = MongoClient('mongodb+srv://jesse:database@cluster0.luq43.mongodb.net/myFirstDatabase?ssl=true')
db = client.get_database('myFirstDatabase')
result = db.currency.delete_many({})

r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json")
if r.status_code == 200:
    data = r.json()
    db.currency.insert_one(data)   
else:
    exit()

records = db.currency
cad = list(records.find({}))[0].get('usd').get('cad')
eur = list(records.find({}))[0].get('usd').get('eur')
gbp = list(records.find({}))[0].get('usd').get('gbp')
jpy = list(records.find({}))[0].get('usd').get('jpy')
aud = list(records.find({}))[0].get('usd').get('aud')
chf = list(records.find({}))[0].get('usd').get('chf')
hkd = list(records.find({}))[0].get('usd').get('hkd')
nzd = list(records.find({}))[0].get('usd').get('nzd')
cny = list(records.find({}))[0].get('usd').get('cny')
inr = list(records.find({}))[0].get('usd').get('inr')

result = db.crypto.delete_many({})
c = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/btc.json")
if c.status_code == 200:
    cryp = c.json()
    db.crypto.insert_one(cryp)  
else:
    exit()

records2 = db.crypto
eth = list(records2.find({}))[0].get('btc').get('eth')
usdt= list(records2.find({}))[0].get('btc').get('usdt')
bnb = list(records2.find({}))[0].get('btc').get('bnb')
xrp = list(records2.find({}))[0].get('btc').get('xrp')
usdc= list(records2.find({}))[0].get('btc').get('usdc')
sol = list(records2.find({}))[0].get('btc').get('sol')
luna= list(records2.find({}))[0].get('btc').get('luna')
ada = list(records2.find({}))[0].get('btc').get('ada')
avax= list(records2.find({}))[0].get('btc').get('avax')
doge= list(records2.find({}))[0].get('btc').get('doge')

# 7 days historical ccy
date = list(records.find({}))[0].get('date') 
datetime = datetime.strptime(date, '%Y-%m-%d').date()
result = db.weekly.delete_many({})
result = db.weekly_crp.delete_many({})
for x in range(7):
    str_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/" + str(datetime) + "/currencies/usd.json"
    w = requests.get(str_url)
    if w.status_code == 200:
        week = w.json()
        db.weekly.insert_one(week)
    else:
        exit()
    str2_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/" + str(datetime) + "/currencies/btc.json"
    q = requests.get(str2_url)
    if q.status_code == 200:
        week_crp = q.json()
        db.weekly_crp.insert_one(week_crp)
    else:
        exit()
    datetime = datetime - timedelta(1)


# Retrieve CCY Records from the Mongo DB Database - 7 Days data
client = MongoClient('mongodb+srv://jesse:database@cluster0.luq43.mongodb.net/myFirstDatabase?ssl=true')
db = client.get_database('myFirstDatabase')
records = db.weekly
ccy_list = {}
for x in range(14):
    val= list(records.find({}))[x].get('usd').get('cad')
    dt = list(records.find({}))[x].get('date')
    ccy_list[dt] = val
ccy_list_sort = OrderedDict(sorted(ccy_list.items()))

# Retrieve CRP Records from the Mongo DB Database - 7 Days data
client = MongoClient('mongodb+srv://jesse:database@cluster0.luq43.mongodb.net/myFirstDatabase?ssl=true')
db = client.get_database('myFirstDatabase')
records = db.weekly_crp
crp_list = {}
for x in range(14):
    val= list(records.find({}))[x].get('btc').get('eth')
    dt = list(records.find({}))[x].get('date')
    crp_list[dt] = val
crp_list_sort = OrderedDict(sorted(crp_list.items()))

@app.route('/')
def index():
    data = {'Euro' : eur, 'CAD' : cad, 'Pounds' : gbp, 'Japanese Yen' : jpy, 'Australian Dollar' : aud, 'Swiss Franc' : chf, 
            'Hong Kong Dollar' : hkd, 'New Zealand Dollar' : nzd, 'Chinese Yuan' : cny, 'Indian Rupee' : inr} 
    return render_template('index.html', data=data)

@app.route('/cryptos/table')
def crypto_table():
    data = {'Ethereum' : eth, 'Tether' : usdt, 'Binance' : bnb, 'Ripple' : xrp, 'USD Coin' : usdc, 'Solana' : sol, 
            'Terra' : luna, 'Cardano' : ada, 'Avalanche' : avax, 'Dogecoin' : doge}
    return render_template('crypto.html', data=data)

@app.route('/oneweek/ccy')
def oneweek():
    return render_template('one_week_ccy.html',data=ccy_list_sort)

@app.route('/oneweek/crp')
def oneweek_crp():
    return render_template('one_week_crp.html',data=crp_list_sort)


if __name__ == "__main__":    
    app.run(debug=True, threaded=True)

