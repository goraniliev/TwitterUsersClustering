# -*- coding: utf-8 -*-
import MySQLdb
import time
from api.API import get_followers, get_friends
from crawl.Time import get_top_user_names, get_top_users

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


def insert_users_from_time_to_db(api, top_fol_start_page=1, top_fol_end_page=15):
    db = get_connection()
    cursor = db.cursor()

    # del_sql = """DELETE FROM friend where iduser > 0;"""
    # cursor.execute(del_sql)
    # db.commit()
    #
    # del_sql = """DELETE FROM follower where iduser > 0;"""
    # cursor.execute(del_sql)
    # db.commit()
    #
    # del_sql = """DELETE FROM user where iduser > 0;"""
    # cursor.execute(del_sql)
    # db.commit()
    users_done = 0
    for i in xrange(top_fol_start_page, top_fol_end_page + 1):
        start = time.time()
        user_names = get_top_user_names(i)
        unfinished = True
        count = 0
        while unfinished:
            try:
                users = list(set(get_top_users(api, user_names)))
                unfinished = False
                users_done += len(users)
            except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                print 'stuck users'
                print user_names
                time.sleep(15 * 60)

        print '%d users crawled' % users_done
        # cursor.execute(del_sql)
        cursor.executemany("""insert into user(iduser, screenname, name) values( %s,%s,%s)""", users)
        db.commit()
        print '%d users inserted' % users_done

        for u in users:
            unfinished = True
            while unfinished:
                try:
                    friends = get_friends(api, u[0])
                    unfinished = False
                except Exception as ex:
                    template = "An exception of type {0} occured. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print message
                    print 'stuck friends'
                    time.sleep(15 * 60)

            unfinished = True
            while unfinished:
                try:
                    followers = list(get_followers(api, u[0]))
                    unfinished = False
                except:
                    print 'stuck followers'
                    time.sleep(15 * 60)
            cursor.executemany("""insert into follower(iduser, idfollower) values( %s,%s)""", followers)
            db.commit()

            cursor.executemany("""insert into friend(iduser, idfriend) values(%s,%s)""", friends)
            db.commit()
        print '%d users processed' % users_done

        end = time.time()
        exec_time = end - start
        cursor.execute("""insert into insertion_time(start_page, end_page, total_time) values(%s,%s,%s)""",
                       (i, i, exec_time))
        db.commit()

    cursor.close()
    db.close()


def set_auto_increment_keys_for_already_inserted_users(api, top_fol_start_page=1, top_fol_end_page=11):
    user_names = []
    for i in xrange(top_fol_start_page, top_fol_end_page + 1):
        user_names += get_top_user_names(i)
    db = get_connection()
    cursor = db.cursor()
    for i in xrange(len(user_names)):
        try:
            cursor.execute("""update user set id_time=%s where screenname=%s""", ((i + 1), user_names[i]))
            db.commit()
        except Exception as ex:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message
            print user_names[i]

    cursor.close()
    db.close()
