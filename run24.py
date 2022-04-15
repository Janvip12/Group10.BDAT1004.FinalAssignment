import requests
import time
from pymongo import MongoClient

while True:
    client = MongoClient('mongodb+srv://jesse:database@cluster0.luq43.mongodb.net/myFirstDatabase?ssl=true')
    db = client.get_database('myFirstDatabase')
    result = db.currency.delete_many({})
    r = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json")
    data = r.json()
    db.currency.insert_one(data)   

    result = db.crypto.delete_many({})    
    c = requests.get("https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/btc.json")
    cryp = c.json()
    db.crypto.insert_one(cryp)  
    
    date = list(records.find({}))[0].get('date') 
    datetime = datetime.strptime(date, '%Y-%m-%d').date()
    result = db.weekly.delete_many({})
    result = db.weekly_crp.delete_many({})
    for x in range(7):
        str_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/" + str(datetime) + "/currencies/usd.json"
        w = requests.get(str_url)
        week = w.json()
        db.weekly.insert_one(week)
        str2_url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/" + str(datetime) + "/currencies/btc.json"
        q = requests.get(str2_url)
        week_crp = q.json()
        db.weekly_crp.insert_one(week_crp)
        datetime = datetime - timedelta(1)
        time.sleep(86400)
