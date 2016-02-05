# -*- coding: utf-8 -*-
import time
from api import API
from api.API import get_followers, get_friends, get_users_by_ids, get_user_by_id
from crawl.Time import get_top_user_names, get_top_users
from db.connection import get_connection
from db.get_utilities import get_all_friends, get_all_followers, get_all_users, get_inv_friends, get_inv_followers

__author__ = 'goran'


def insert_users_from_time_to_db(api, top_fol_start_page=1, top_fol_end_page=15):
    db = get_connection()
    cursor = db.cursor()

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


def is_macedonian_user(api, iduser, all_users, max_followers=70000, threshold_followers=0.01, threshold_friends=0.01):
    user = api.get_user(id=iduser)

    # We already have the users with most followers, so if there is someone with more followers, then he is not macedonian
    if user.followers_count > max_followers or user.friends_count > max_followers:
        return False, set(), set()

    friends = API.get_friends_ids(api, iduser)
    followers = API.get_followers_ids(api, iduser)

    macedonian_friends = len(friends & all_users)
    macedonian_followers = len(followers & all_users)

    # If greater part of friends and followers are macedonians, then this user is probably also macedonian
    print user.screen_name
    return 1.0 * macedonian_friends / (1 + len(friends)) > threshold_friends and \
           1.0 * macedonian_followers / (1 + len(followers)) > threshold_followers, \
           [(iduser, f) for f in friends], [(iduser, f) for f in followers]


def insert_more_users_to_db(api):
    db = get_connection()
    cursor = db.cursor()

    all_friends = get_all_friends()
    all_followers = get_all_followers()
    all_users = get_all_users()

    # new_macedonian_users = set(all_friends)
    cnt = 0
    for friend in all_friends:
        try:
            is_macedonian, friends, followers = is_macedonian_user(api, friend, all_users)
            print 'Friend', friend
            if is_macedonian and friend not in all_users:
                print 'YEEEEEEES'
                # new_macedonian_users.add(friend)
                all_users.add(friend)
                new_user = get_user_by_id(api, friend)
                print new_user
                cursor.execute("""insert into user(iduser, screenname, name) values(%s,%s,%s)""", new_user)
                cursor.executemany("""insert into friend(iduser, idfriend) values(%s,%s)""", friends)
                db.commit()
        except:
            continue
        cnt += 1
        print 'Count', cnt

    cnt = 0

    for follower in all_followers:
        try:
            is_macedonian, friends, followers = is_macedonian_user(api, follower, all_users)
            print 'Follower', follower
            if follower not in all_users and is_macedonian:
                print 'YEEEEEEES'
                # new_macedonian_users.add(follower)
                new_user = get_user_by_id(api, friend)
                all_users.add(follower)
                cursor.execute("""insert into user(iduser, screenname, name) values(%s,%s,%s)""", new_user)
                cursor.executemany("""insert into follower(iduser, idfollower) values( %s,%s)""", followers)
                db.commit()
        except:
            continue
        cnt += 1
        print 'Count', cnt
    cursor.close()
    db.close()


def find_new_users_to_insert(api, min_friends=1, min_followers=5):
    inv_user_friends = get_inv_friends()
    inv_user_followers = get_inv_followers()

    users = []

    for u, cnt in inv_user_friends.iteritems():
        if cnt > min_friends and inv_user_followers.get(u, 0) > min_followers:
            users.append(u)

    return users


def insert_more_users_without_unnecessary_api_calls(api, min_friends=2, min_followers=10, max_friends=50000, max_followers=50000):
    users = find_new_users_to_insert(api, min_friends, min_followers)

    db = get_connection()
    cursor = db.cursor()

    for u in users:
        user, friends_count, followers_count = get_user_by_id(api, u)

        # if he is macedonian, he would already be on Twitter
        if followers_count > max_followers or friends_count > max_friends: continue

        cursor.execute("""insert into user(iduser, screenname, name) values(%s,%s,%s)""", user)

        try:
            friends = get_friends(api, u)
            followers = get_followers(api, u)
        except:
            print 'waiting for API'
            time.sleep(61)

        cursor.executemany("""insert into friend(iduser, idfriend) values(%s,%s)""", friends)

        cursor.executemany("""insert into follower(iduser, idfollower) values( %s,%s)""", followers)

        db.commit()

        print user[1].decode('utf-8'), " inserted"





