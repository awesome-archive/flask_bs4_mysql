# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import time
import MySQLdb

db = MySQLdb('localhost','web','webpass','hotweb')
response = requests.get("http://www.v2ex.com")
soup = BeautifulSoup(response.text,'lxml')
for i in soup.findAll('span', class_='item_title'):
    #print(i.string)
    #print('https://www.v2ex.com'+i.a['href'])
    db.cursor.execute("insert into hot_v2ex(title,url) values(%s,%s) , (i.string,'https://www.v2ex.com'+i.a['href']))
db.commit()
        abc(1,3,3,3)
