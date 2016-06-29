from . import main
from flask import render_template
from bs4 import BeautifulSoup
import MySQLdb
import MySQLdb.cursors
import requests


class Mysql_db(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'web', 'webpass', 'hotweb', use_unicode=True, charset="utf8",
                                    cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()


@main.route('/')
def index():
    db = Mysql_db()
    db.cursor.execute('SELECT * FROM hot_v2ex ORDER BY id desc limit 10')
    v2ex = db.cursor.fetchall()
    db.cursor.execute('SELECT * FROM hot_cnbeta ORDER BY id desc limit 10')
    cnbeta = db.cursor.fetchall()
    db.close_db()
    return render_template('index.html', v2ex=v2ex, cnbeta=cnbeta)


@main.route('/update/v2ex')
def getV2ex():
    response = requests.get("http://www.v2ex.com")
    soup = BeautifulSoup(response.text, 'lxml')
    db = Mysql_db()
    try:
        for i in soup.findAll('span', class_='item_title'):
            db.cursor.execute("insert into hot_v2ex(title,url) values(%s,%s)",
                              (i.string, 'https://www.v2ex.com' + i.a['href']))
        db.conn.commit()
    except:
        db.conn.rollback()
    db.close_db()
    return render_template('index.html')


@main.route('/update/cnbeta')
def getCnbeta():
    html = requests.get('http://www.cnbeta.com/')
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    db = Mysql_db()
    try:
        for i in soup.find_all('div', class_='title'):
            db.cursor.execute("insert into hot_cnbeta(title,url) values(%s,%s)",
                              (i.a.string.lstrip('[图][视频][动图]'), 'http://www.cnbeta.com' + i.a['href']))
        db.conn.commit()
    except:
        db.conn.rollback()
        db.close_db()
    return render_template('index.html')
