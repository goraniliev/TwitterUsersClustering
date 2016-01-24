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


def get_followers():
    db = get_connection()
    cursor = db.cursor()

    followers = {}

    sql = """select * from follower"""

    cursor.execute(sql)

    for (iduser, idfollower) in cursor:
        followers.setdefault(iduser, set())
        followers[iduser].add(idfollower)

    cursor.close()
    db.close()

    return followers
