# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests

html = requests.get('http://www.cnbeta.com/')
html.encoding = 'utf-8'
soup = BeautifulSoup(html.text, 'lxml')
for i in soup.find_all('div', class_='title'):
    print('http://www.cnbeta.com' + i.a['href'])
    print(i.a.string.lstrip('[图][视频][动图]'))
