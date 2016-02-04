# -*- coding: utf-8 -*-
import time
import tweepy
from common.common import is_inserted

__author__ = 'goran'

def get_api_instance(consumer_key='8wiTu4VA2HQ8IacbcOcxG5N6e',
                     consumer_secret='5btRjpbp1K7rHRtxJqWVeaeMnCEOZK5Ypp6D2i1kp9h0cmPlNR',
                     access_token='241699249-2zZJjh8Lgkh80WHh5Gvj1MLqSNHJqS1LOSvcnmsN',
                     access_token_secret='blkvpDNPadb2iTcLyG1iURLH12kxidkq0zELvmJj4xDrT'):
    '''
    Returns tweepy.api.API object, which gives authorized access to the Twitter API.
    It is obligatory to have access tokens to access Twitter API.
    :param consumer_key:
    :param consumer_secret:
    :param access_token:
    :param access_token_secret:
    :return:
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    """
    @type api: tweepy.api.API
    """
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


def get_followers(api, id_user):
    f = []
    try:
        for foll_idx in tweepy.Cursor(api.followers_ids, id=id_user).items():
            f.append((id_user, foll_idx))
    except:
        return set()
    return set(f)


def get_friends(api, id_user):
    f = []
    try:
        for friend_idx in tweepy.Cursor(api.friends_ids, id=id_user).items():
            f.append((id_user, friend_idx))
            # print friend_idx
    except:
        time.sleep(15 * 60)
    return set(f)


def get_followers_ids(api, id_user):
    f = []
    try:
        for foll_idx in tweepy.Cursor(api.followers_ids, id=id_user).items():
            f.append(foll_idx)
    except:
        time.sleep(15 * 60)
    return set(f)


def get_friends_ids(api, id_user):
    f = []
    try:
        for friend_idx in tweepy.Cursor(api.friends_ids, id=id_user).items():
            f.append(friend_idx)
            # print friend_idx
    except:
        return set()
    return set(f)


def get_users_by_ids(api, id_users):
    return [(u.id, u.screen_name, u.name.encode('utf-8'))
            for u in api.lookup_users(id=id_users) if not is_inserted(u.id)]


def get_user_by_id(api, id_user):
    user = api.get_user(id=id_user)
    return user.id, user.screen_name.encode('utf-8'), user.name.encode('utf-8')

