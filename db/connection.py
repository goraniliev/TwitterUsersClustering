# -*- coding: utf-8 -*-
import MySQLdb

__author__ = 'goran'

def get_connection():
    '''
    Returns connection to database (here is encapsulated the connection string).
    :return:
    '''
    db = MySQLdb.connect(host="localhost",  # your host
                         user="root",  # your username
                         passwd="goranpass",  # your password
                         db="twitter")
    # cur = db.cursor()
    # cur.close()
    return db