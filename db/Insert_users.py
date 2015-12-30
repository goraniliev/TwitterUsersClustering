# -*- coding: utf-8 -*-
import MySQLdb
from bs4 import BeautifulSoup
import urllib2
from api.API import get_api_instance, get_id_and_name_by_screen_name
from models.User import User

__author__ = 'goran'


def get_connection():
    '''
    Returns connection to database (here is encapsulated the connection string).
    :return:
    '''
    db = MySQLdb.connect(host="localhost",    # your host
                     user="root",         # your username
                     passwd="goranpass",  # your password
                     db="twitter")
    # cur = db.cursor()
    # cur.close()
    return db


def insert_users_to_db():
    users = get_top_users(1)

    db = get_connection()
    cursor = db.cursor()
    del_sql = """DELETE FROM user where iduser > 0;"""
    cursor.execute(del_sql)
    cursor.executemany("""insert into user(iduser, screenname, name) values(%s, %s, %s)""", users)
    db.commit()
    cursor.close()
    db.close()


def get_top_users(num=1, url='http://www.time.mk/twitter/topfoll/'):
    page = urllib2.urlopen(url + str(num))
    soup = BeautifulSoup(page)

    users = []
    api = get_api_instance()

    for link in soup.find_all('a'):
        href = link.get('href')
        if href is not None and href.startswith('twitter/user/'):
            screen_name = href[13:]
            idx, name = get_id_and_name_by_screen_name(api, screen_name)
            users.append((int(idx), screen_name, name))
    return users


def get_top_users_from_p_pages(p=100):
    users = []
    p += 1
    for i in xrange(1, p):
        users += get_top_users(num=p)

    return users
