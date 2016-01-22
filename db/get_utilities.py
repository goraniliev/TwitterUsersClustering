# -*- coding: utf-8 -*-
from db.Insert_users import get_connection

__author__ = 'goran'

def get_friends():
    db = get_connection()
    cursor = db.cursor()

    friends = {}

    sql = """select * from friend"""

    cursor.execute(sql)

    for (iduser, idfriend) in cursor:
        friends.setdefault(iduser, set())
        friends[iduser].add(idfriend)

    cursor.close()
    db.close()

    return friends