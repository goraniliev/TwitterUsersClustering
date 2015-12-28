# -*- coding: utf-8 -*-
import MySQLdb
from bs4 import BeautifulSoup
import urllib2

__author__ = 'goran'

def get_connection():
    db = MySQLdb.connect(host="localhost",    # your host
                     user="root",         # your username
                     passwd="goranpass",  # your password
                     db="twitter")
    # cur = db.cursor()
    # cur.close()
    return db


def insert_users_to_db():
    user_names = get_top_users(1)
    # print user_names
    # print ','.join(['(%s)' % u for u in user_names])

    db = get_connection()
    cursor = db.cursor()
    del_sql = """DELETE FROM user where iduser > 0;"""
    cursor.execute(del_sql)
    cursor.executemany("""insert into user(username) values(%s)""", user_names)
    db.commit()
    cursor.close()
    db.close()


def get_top_users(num=1, url='http://www.time.mk/twitter/topfoll/'):
    page = urllib2.urlopen(url + str(num))
    soup = BeautifulSoup(page)

    user_names = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and href.startswith('twitter/user/'):
            user_names.append(href[13:])
    return user_names


def get_top_users_from_p_pages(p=100):
    user_names = []
    p += 1
    for i in xrange(1, p):
        user_names += get_top_users(num=p)

    return user_names
