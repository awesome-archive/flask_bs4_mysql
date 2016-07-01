from . import main
from flask import render_template, redirect, url_for, flash
from bs4 import BeautifulSoup
import MySQLdb
import MySQLdb.cursors
import requests
import datetime


class Mysql_db(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'web', 'webpass', 'hotweb', use_unicode=True, charset="utf8",
                                    cursorclass=MySQLdb.cursors.DictCursor)
        self.cursor = self.conn.cursor()

    def close_db(self):
        self.cursor.close()
        self.conn.close()


def sqlV2ex(db, soup):
    db.cursor.execute("truncate table hot_v2ex")
    db.conn.commit()
    db.cursor.execute("insert into hot_site(web,refresh_time) values(%s,%s)", ("v2ex", str(datetime.datetime.now())))
    for i in soup.findAll('span', class_='item_title'):
        db.cursor.execute("insert into hot_v2ex(title,url) values(%s,%s)",
                          (i.string, 'https://www.v2ex.com' + i.a['href']))
    db.conn.commit()


def sqlCnbeta(db, soup):
    db.cursor.execute("truncate table hot_cnbeta")
    db.conn.commit()
    db.cursor.execute("insert into hot_site(web,refresh_time) values(%s,%s)", ("cnbeta", str(datetime.datetime.now())))
    for i in soup.find_all('div', class_='title'):
        db.cursor.execute("insert into hot_cnbeta(title,url) values(%s,%s)",
                          (i.a.string.lstrip('[多图][表热][图][视频][多图]'), 'http://www.cnbeta.com' + i.a['href']))
    db.conn.commit()


@main.route('/')
def index():
    db = Mysql_db()
    db.cursor.execute('SELECT * FROM hot_v2ex limit 10')
    v2ex = db.cursor.fetchall()
    db.cursor.execute('SELECT * FROM hot_cnbeta limit 10')
    cnbeta = db.cursor.fetchall()
    db.close_db()
    return render_template('index.html', v2ex=v2ex, cnbeta=cnbeta)


@main.route('/update/v2ex')
def getV2ex():
    response = requests.get("http://www.v2ex.com")
    soup = BeautifulSoup(response.text, 'lxml')
    db = Mysql_db()
    db.cursor.execute(
        "select * from hot_site where web = 'v2ex' order by refresh_time desc limit 1")
    data = db.cursor.fetchone()
    try:
        if data is not None:
            overtime = (datetime.datetime.now() - data['refresh_time'])
            if overtime.seconds > 7200:
                sqlV2ex(db, soup)
                return 'success'
            else:
                return 'time_no'
        else:
            sqlV2ex(db, soup)
            return 'init'
    except BaseException as e:
        return '错误'
    finally:
        db.close_db()


@main.route('/update/cnbeta')
def getCnbeta():
    html = requests.get('http://www.cnbeta.com/')
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    db = Mysql_db()
    db.cursor.execute(
        "select * from hot_site where web = 'cnbeta' order by refresh_time desc limit 1")
    data = db.cursor.fetchone()
    try:
        if data is not None:
            overtime = (datetime.datetime.now() - data['refresh_time'])
            if overtime.seconds > 7200:
                sqlCnbeta(db, soup)
                return 'success'
            else:
                return 'time_no'
        else:
            sqlCnbeta(db, soup)
            return 'init'
    except BaseException as e:
        return '错误'
    finally:
        db.close_db()
