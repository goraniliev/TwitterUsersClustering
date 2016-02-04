# -*- coding: utf-8 -*-
from collections import OrderedDict
from db.connection import get_connection

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


def get_clusters_from_db():
    db = get_connection()
    cursor = db.cursor()

    sql = """select screenname, cluster from user"""

    cursor.execute(sql)

    clusters = {}

    for (screen_name, cluster) in cursor:
        clusters.setdefault(cluster, [])
        clusters[cluster].append(screen_name)

    idx = 1
    ordered_clusters = OrderedDict()
    for cluster, users in clusters.iteritems():
        ordered_clusters['Cluster ' + str(idx)] = users
        idx += 1

    return ordered_clusters


def get_all_users():
    db = get_connection()
    cursor = db.cursor()
    sql = """select iduser from user"""
    cursor.execute(sql)

    users = [u[0] for u in cursor]

    return set(users)


def get_all_friends():
    db = get_connection()
    cursor = db.cursor()
    sql = """select distinct idfriend from friend"""
    cursor.execute(sql)

    users = [u[0] for u in cursor]

    return set(users)


def get_all_followers():
    db = get_connection()
    cursor = db.cursor()
    sql = """select distinct idfollower from follower"""
    cursor.execute(sql)

    users = [u[0] for u in cursor]

    return set(users)


def get_inv_friends():
    all_users = get_all_users()
    db = get_connection()
    cursor = db.cursor()

    users_friends_count = {}

    sql = """select f.idfriend, count(*) from friend f group by f.idfriend"""

    cursor.execute(sql)

    for record in cursor:
        if record[0] not in all_users:
            users_friends_count[record[0]] = int(record[1])

    return users_friends_count


def get_inv_followers():
    all_users = get_all_users()
    db = get_connection()
    cursor = db.cursor()

    user_followers_count = {}

    sql = """select f.idfollower, count(*) from follower f group by f.idfollower"""

    cursor.execute(sql)

    for record in cursor:
        if record[0] not in all_users:
            user_followers_count[record[0]] = int(record[1])

    return user_followers_count


